```javascript
class HealthBar {
  constructor(scene, x, y, width, height) {
    this.bar = new Phaser.GameObjects.Graphics(scene);
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.p = 1.0;
    scene.add.existing(this.bar);
    this.draw();
  }
  setPercentage(value) {
    this.p = Phaser.Math.Clamp(value, 0, 1);
    this.draw();
  }
  updatePosition(x, y) {
    this.x = x;
    this.y = y;
    this.draw();
  }
  draw() {
    this.bar.clear();
    this.bar.fillStyle(0x000000);
    this.bar.fillRect(this.x - this.width / 2, this.y, this.width, this.height);
    this.bar.fillStyle(
      this.p < 0.3 ? 0xff0000 : this.p < 0.6 ? 0xffff00 : 0x00ff00
    );
    this.bar.fillRect(
      this.x - this.width / 2,
      this.y,
      Math.floor(this.p * this.width),
      this.height
    );
    this.bar.lineStyle(2, 0xffffff);
    this.bar.strokeRect(
      this.x - this.width / 2,
      this.y,
      this.width,
      this.height
    );
  }
  destroy() {
    this.bar.destroy();
  }
}

class Entity extends Phaser.GameObjects.Sprite {
  constructor(scene, x, y, texture, frame) {
    super(scene, x, y, texture, frame);
    scene.add.existing(this);
    this.team = null;
    this.isSelected = false;
    this.selectionCircle = scene.add.graphics();
    this.hp = 100;
    this.maxHp = 100;
    this.healthBar = new HealthBar(scene, x, y - this.height, 50, 6);
    this.setInteractive();
    this.on("pointerdown", (pointer) => {
      if (pointer.leftButtonDown()) this.scene.selectEntity(this);
    });
  }
  setSelected(isSelected) {
    this.isSelected = isSelected;
    this.updateSelectionCircle();
  }
  updateSelectionCircle() {
    this.selectionCircle.clear();
    if (this.isSelected) {
      this.selectionCircle.lineStyle(1, 0x00ff00, 1);
      this.selectionCircle.strokeCircle(this.x, this.y, this.width * 0.7);
    }
  }
  takeDamage(amount) {
    this.hp -= amount;
    if (this.hp < 0) this.hp = 0;
    this.healthBar.setPercentage(this.hp / this.maxHp);
    if (this.hp <= 0) this.die();
  }
  die() {
    if (this.isSelected) this.scene.deselectAll();
    this.healthBar.destroy();
    this.selectionCircle.destroy();
    this.destroy();
  }
  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    this.healthBar.updatePosition(this.x, this.y - this.height * 0.8);
    if (this.isSelected) this.updateSelectionCircle();
  }
}

class Resource extends Entity {
  constructor(scene, x, y) {
    super(scene, x, y, "resource");
    this.hp = 1000;
    this.maxHp = 1000;
    this.healthBar.setPercentage(1);
    this.team = "neutral";
  }
  deplete(amount) {
    this.hp -= amount;
    if (this.hp < 0) this.hp = 0;
    this.healthBar.setPercentage(this.hp / this.maxHp);
    if (this.hp <= 0) this.die();
  }
  takeDamage(amount) {
    /* Resource can not be attack */
  }
}

// --- Movable Unit ---
class Unit extends Entity {
  constructor(scene, x, y, texture, frame) {
    super(scene, x, y, texture, frame);
    scene.physics.add.existing(this);
    this.destination = null;
    this.speed = 100;
  }
  moveTo(x, y) {
    this.target = null;
    this.gatherTarget = null;
    this.destination = new Phaser.Math.Vector2(x, y);
    this.scene.physics.moveTo(this, x, y, this.speed);
  }
  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    if (this.body.speed > 0 && this.destination) {
      if (
        Phaser.Math.Distance.Between(
          this.x,
          this.y,
          this.destination.x,
          this.destination.y
        ) < 5
      ) {
        this.body.reset(this.x, this.y);
        this.destination = null;
      }
    }
  }
}

// --- Soldier Class ---
class SoldierUnit extends Unit {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.target = null;
    this.attackCooldown = 1000;
    this.lastAttackTime = 0;
    // Defined by subclasses
    this.attackRange = 50;
    this.damage = 10;
  }
  setAttackTarget(target) {
    this.target = target;
    this.destination = null;
  }
  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    if (this.target && this.target.active) {
      const distance = Phaser.Math.Distance.Between(
        this.x,
        this.y,
        this.target.x,
        this.target.y
      );
      if (distance <= this.attackRange) {
        this.body.setVelocity(0, 0);
        if (time > this.lastAttackTime + this.attackCooldown) {
          this.target.takeDamage(this.damage);
          this.lastAttackTime = time;
          this.scene.tweens.add({
            targets: this,
            scaleX: 1.1,
            scaleY: 1.1,
            yoyo: true,
            duration: 50,
          });
        }
      } else {
        this.scene.physics.moveToObject(this, this.target, this.speed);
      }
    }
  }
}

class LightSoldierUnit extends SoldierUnit {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.speed = 130;
    this.attackRange = 50;
    this.damage = 8;
    this.hp = 80;
    this.maxHp = 80;
    this.healthBar.setPercentage(1);
  }
}
class RangedSoldierUnit extends SoldierUnit {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.speed = 100;
    this.attackRange = 150;
    this.damage = 7;
    this.hp = 60;
    this.maxHp = 60;
    this.healthBar.setPercentage(1);
  }
}
class HeavySoldierUnit extends SoldierUnit {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.speed = 70;
    this.attackRange = 60;
    this.damage = 15;
    this.hp = 150;
    this.maxHp = 150;
    this.healthBar.setPercentage(1);
  }
}

class WorkerUnit extends Unit {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.gatherTarget = null;
    this.gatherRange = 50;
    this.gatherCooldown = 1500;
    this.lastGatherTime = 0;
    this.gatherAmount = 5;
  }
  setGatherTarget(target) {
    this.gatherTarget = target;
    this.destination = null;
  }
  preUpdate(time, delta) {
    super.preUpdate(time, delta);
    if (this.gatherTarget && this.gatherTarget.active) {
      const distance = Phaser.Math.Distance.Between(
        this.x,
        this.y,
        this.gatherTarget.x,
        this.gatherTarget.y
      );
      if (distance <= this.gatherRange) {
        this.body.setVelocity(0, 0);
        if (time > this.lastGatherTime + this.gatherCooldown) {
          this.gatherTarget.deplete(this.gatherAmount);
          this.scene.addResources(this.gatherAmount);
          this.lastGatherTime = time;
          this.scene.tweens.add({
            targets: this,
            scaleX: 1.1,
            scaleY: 1.1,
            yoyo: true,
            duration: 50,
          });
        }
      } else {
        this.scene.physics.moveToObject(this, this.gatherTarget, 100);
      }
    }
  }
}

class BaseBuilding extends Entity {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.hp = 500;
    this.maxHp = 500;
    this.healthBar.setPercentage(1);
    this.on("pointerdown", (pointer) => {
      if (pointer.leftButtonDown() && this.team === "player")
        this.scene.trySpawnUnit("worker", this);
    });
  }
}
class Barracks extends Entity {
  constructor(scene, x, y, texture) {
    super(scene, x, y, texture);
    this.hp = 350;
    this.maxHp = 350;
    this.healthBar.setPercentage(1);
  }
}

class GameScene extends Phaser.Scene {
  constructor() {
    super("GameScene");
    this.selectedEntities = [];
    this.resources = 200;
    this.unitCosts = { worker: 25, light: 35, ranged: 45, heavy: 60 };
  }

  preload() {
    // Worker
    this.make
      .graphics({ fillStyle: { color: 0x00ff00 } })
      .fillRect(0, 0, 18, 18)
      .generateTexture("worker", 18, 18);
    // Light Soldier
    this.make
      .graphics({ fillStyle: { color: 0xadd8e6 } })
      .fillRect(0, 0, 18, 18)
      .generateTexture("player_light", 18, 18);
    this.make
      .graphics({ fillStyle: { color: 0xffc0cb } })
      .fillRect(0, 0, 18, 18)
      .generateTexture("enemy_light", 18, 18);
    // Remote Solider
    this.make
      .graphics({ fillStyle: { color: 0x0000ff } })
      .fillCircle(10, 10, 10)
      .generateTexture("player_ranged", 20, 20);
    this.make
      .graphics({ fillStyle: { color: 0xff0000 } })
      .fillCircle(10, 10, 10)
      .generateTexture("enemy_ranged", 20, 20);
    // Heavy Soldier
    this.make
      .graphics({ fillStyle: { color: 0x00008b } })
      .fillRect(0, 0, 24, 24)
      .generateTexture("player_heavy", 24, 24);
    this.make
      .graphics({ fillStyle: { color: 0x8b0000 } })
      .fillRect(0, 0, 24, 24)
      .generateTexture("enemy_heavy", 24, 24);
    // Building and Resource
    this.make
      .graphics({ fillStyle: { color: 0x808080 } })
      .fillRect(0, 0, 80, 80)
      .generateTexture("base", 80, 80);
    this.make
      .graphics({ fillStyle: { color: 0x8b4513 } })
      .fillRect(0, 0, 70, 60)
      .generateTexture("barracks", 70, 60);
    this.make
      .graphics({ fillStyle: { color: 0xffff00 } })
      .fillCircle(20, 20, 20)
      .generateTexture("resource", 40, 40);
    this.resourceText = this.add.text(10, 10, "", {
      font: "20px Arial",
      fill: "#ffffff",
    });
  }

  create() {
    this.units = this.physics.add.group({ runChildUpdate: true });
    this.buildings = this.add.group({ runChildUpdate: true });
    this.resourcesGroup = this.add.group({
      classType: Resource,
      runChildUpdate: true,
    });

    this.spawnBuilding("base", 150, 400, "player");
    this.spawnBuilding("barracks", 250, 400, "player");
    this.spawnBuilding("base", 650, 200, "enemy");
    this.spawnBuilding("barracks", 550, 200, "enemy");

    this.spawnUnit("ranged", 600, 100, "enemy");
    this.spawnUnit("heavy", 600, 300, "enemy");
    this.spawnUnit("worker", 200, 300, "player");

    this.spawnResource(400, 100);
    this.spawnResource(500, 500);
    this.spawnResource(300, 500);

    this.createBuildPanel(); // create Build UI

    this.input.on("pointerdown", (pointer) => this.handlePointerDown(pointer));
    this.input.mouse.disableContextMenu();
    this.updateResourceText();
  }

  handlePointerDown(pointer) {
    const allEntities = [
      ...this.units.getChildren(),
      ...this.buildings.getChildren(),
      ...this.resourcesGroup.getChildren(),
    ];
    const clickedObjects = this.input.manager.hitTest(
      pointer,
      allEntities,
      this.cameras.main
    );
    const targetEntity = clickedObjects.length > 0 ? clickedObjects[0] : null;

    if (pointer.leftButtonDown()) {
      if (!targetEntity) this.deselectAll();
    }
    if (pointer.rightButtonDown()) {
      if (this.selectedEntities.length === 0) return;
      this.selectedEntities.forEach((unit) => {
        if (!(unit instanceof Unit)) return;
        if (targetEntity) {
          if (unit instanceof WorkerUnit && targetEntity instanceof Resource)
            unit.setGatherTarget(targetEntity);
          else if (
            unit instanceof SoldierUnit &&
            targetEntity.team &&
            targetEntity.team !== unit.team
          )
            unit.setAttackTarget(targetEntity);
          else unit.moveTo(pointer.worldX, pointer.worldY);
        } else {
          unit.moveTo(pointer.worldX, pointer.worldY);
        }
      });
    }
  }

  spawnUnit(unitType, x, y, team) {
    let unit;
    const texture = `${team}_${unitType}`;
    switch (unitType) {
      case "worker":
        unit = new WorkerUnit(this, x, y, "worker");
        break;
      case "light":
        unit = new LightSoldierUnit(this, x, y, texture);
        break;
      case "ranged":
        unit = new RangedSoldierUnit(this, x, y, texture);
        break;
      case "heavy":
        unit = new HeavySoldierUnit(this, x, y, texture);
        break;
      default:
        return null;
    }
    unit.team = team;
    this.units.add(unit);
    return unit;
  }

  spawnBuilding(buildingType, x, y, team) {
    let building;
    if (buildingType === "base")
      building = new BaseBuilding(this, x, y, "base");
    else if (buildingType === "barracks")
      building = new Barracks(this, x, y, "barracks");
    if (!building) return null;
    building.team = team;
    if (team === "player")
      building.setTint(buildingType === "base" ? 0xaaaaee : 0xdeb887);
    else building.setTint(buildingType === "base" ? 0xeeaaaa : 0xc04040);
    this.buildings.add(building);
    return building;
  }

  spawnResource(x, y) {
    const resource = new Resource(this, x, y);
    this.resourcesGroup.add(resource);
    return resource;
  }

  trySpawnUnit(unitType, spawningBuilding) {
    const cost = this.unitCosts[unitType];
    if (this.resources >= cost) {
      this.resources -= cost;
      this.updateResourceText();
      const spawnX = spawningBuilding.x;
      const spawnY = spawningBuilding.y + spawningBuilding.height / 2 + 20;
      this.spawnUnit(unitType, spawnX, spawnY, "player");
    } else {
      let noMoneyText = this.add
        .text(spawningBuilding.x, spawningBuilding.y - 60, "Resource is not enough!", {
          font: "16px Arial",
          fill: "#ff0000",
          align: "center",
        })
        .setOrigin(0.5);
      this.time.delayedCall(1000, () => noMoneyText.destroy());
    }
  }

  addResources(amount) {
    this.resources += amount;
    this.updateResourceText();
  }

  selectEntity(entity) {
    if (
      !this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT).isDown
    )
      this.deselectAll();
    if (!this.selectedEntities.includes(entity)) {
      this.selectedEntities.push(entity);
      entity.setSelected(true);
    }
    // Show Spawn UI for Barracks
    if (entity instanceof Barracks && entity.team === "player") {
      this.buildPanel.setVisible(true);
      this.buildPanel.setData("owner", entity);
    }
  }

  deselectAll() {
    this.selectedEntities.forEach((entity) => entity.setSelected(false));
    this.selectedEntities = [];
    this.buildPanel.setVisible(false); // Hide Spawn UI
    this.buildPanel.setData("owner", null);
  }

  updateResourceText() {
    this.resourceText.setText(`Resource: ${this.resources}`);
    this.resourceText.setDepth(100);
  }

  createBuildPanel() {
    this.buildPanel = this.add
      .container(this.cameras.main.width / 2, this.cameras.main.height - 50)
      .setDepth(101)
      .setVisible(false);
    const panelBG = this.add
      .graphics()
      .fillStyle(0x000000, 0.5)
      .fillRect(-155, -25, 310, 50);
    this.buildPanel.add(panelBG);

    const unitTypes = ["light", "ranged", "heavy"];
    unitTypes.forEach((type, index) => {
      const button = this.add
        .text(
          -120 + index * 100,
          0,
          `Train for ${type}\n(${this.unitCosts[type]})`,
          {
            font: "12px Arial",
            fill: "#fff",
            backgroundColor: "#555",
            padding: { x: 5, y: 5 },
            align: "center",
          }
        )
        .setOrigin(0.5)
        .setInteractive();
      button.on("pointerdown", () => {
        const owner = this.buildPanel.getData("owner");
        if (owner) this.trySpawnUnit(type, owner);
      });
      this.buildPanel.add(button);
    });
  }

  update(time, delta) {}
}

// --- Game Config ---
var config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: "game-container",
  backgroundColor: "#5DACD8",
  physics: { default: "arcade", arcade: { debug: false } },
  scene: GameScene,
};

var game = new Phaser.Game(config);
```
