You are a game designer, and the following describes the game the user wants to create.

{overview}

Your task is to rewrite the user’s game description into a format the system understands, as follows:

1. **Entity Extraction & Mapping**
   Parse each entity mentioned in the user’s rules and map it to one of the known types below.

   * Example: “Players can move up, down, left, and right” → “a `MovingAvatar` player”
   * Example: “Players can move up, down, left, and right. Players can fire missiles or place bombs” → “a `ShootAvatar` player, which can moving around. Also player is capable of shooting projectiles”

   **Available types:**

    MovingAvatar: "A controllable avatar that can move in four directions.",
    HorizontalAvatar: "An avatar that moves horizontally.",
    FlakAvatar: "Horizontal avatar that shoots with SPACE key.",
    OrientedAvatar: "An avatar with a specific orientation and movement",
    MissileAvatar: "Oriented avatar that moves steadily at a speed of 1.",
    OngoingShootAvatar: "Avatar that continuously shoots with movement.",
    RotatingAvatar: "An avatar that rotates and moves.",
    ShootAvatar: "An oriented avatar that can shoot projectiles.",
    VerticalAvatar: "Avatar moving vertically, only up and down.",
    RandomNPC: "A non-player character with random movement",
    AStarChaser: "Chases target using A* algorithm.",
    AlternateChaser: "Chases or flees based on target assessment.",
    Bomber: "A missile that periodically spawns other sprites.",
    Chaser: "Speeds toward nearest target, occasionally in a random direction.",
    Conveyer: "Static sprite that moves entities in a direction",
    Door: "An immovable door that may act as a portal.",
    Fleeing: "Sprite that flees from a certain entity.",
    Immovable: "A sprite that doesn't move.",
    Missile: "A sprite with oriented movement capability.",
    Passive: "Non-interactive VGDL sprite",
    SpawnPoint: "Generates sprites based on cooldown and probability."


2. **Interaction Extraction & Mapping**
   Identify each interaction between entities and express it using one of the verbs below.

   * Example: “Players can kill monsters” → “When the player collides with a monster, trigger the `killSprite` effect”
   * Add common-sense rules if needed (e.g. “Players cannot pass through walls” → “When the player collides with a wall, the player `stepBack`”).

   **Available interaction verbs:**

    addHealthPoints： "Increases the sprite's health points.",
    bounceDirection： "Alters sprite's speed and direction upon collision",
    bounceForward： "Moves sprite forward based on partner's direction and speed.",
    changeScore： "Modifies the score of the game",
    killAll： "Eliminates all sprites of a specific type",
    killSprite： "Adds sprite to the game's kill list.",
    killBoth： "Eliminates both interacting game sprites.",
    spawn： "Creates a new sprite at the current location.",
    stepBack： "Moves sprite to its last location",
    subtractHealthPoints： "Reduces health points of targeted sprites",
    transformTo： "Transforms sprite to specified type",
    turnAround： "Reverses the movement direction of a sprite.",
    wrapAround： "Transports sprite to opposite edge when moving out of bounds."


   **Note:** Do **not** use any collections (e.g. “Enemies”) to represent multiple distinct types. If there are two enemy types (“Spider” and “Slime”), write separate rules:

   ```
   When Spider collides with a wall, Spider stepBack.
   When Slime collides with a wall, Slime stepBack.
   ```

3. **Game-Over Conditions**
   Rewrite any end-of-game conditions using the following constructs:


    SpriteCounter:  "Ends game based on sprite count and limit.",
    Timeout:        "Terminates game when time limit is reached.",


   * Example: “The game ends when the player dies” → “`SpriteCounter` of Player is 0, win is false.”
   * If the user has not provided any end conditions, add one or more that make sense, for example:

     * “When time reaches 1000 ticks, win is false”
     * “`SpriteCounter` of Player is 0, win is false”
     * “`SpriteCounter` of Spider is 0, win is true”