const entities = {
    "PlayerCharacter": "MovingAvatar",
    "WallTiles": "Immovable"
}

const rules = [
    {
        "source": "PlayerCharacter",
        "target": "WallTiles",
        "effect": "wallStop",
        "explain": "When the player character sprite comes in contact with a grey Square object representing wall tiles, the 'stop' function will prevent any further movement of the sprite to simulate running into a wall, which aligns with the game rule of avoiding these tiles and losing one life upon contact."
    },
    {
        "source": "PlayerCharacter",
        "target": "WallTiles",
        "effect": "wallBounce: Friction effect; direction towards opposite edge if moving out off bounds",
        "explain": "This rule dictates that when the player character sprite tries to move beyond the grid boundaries, it will bounce back onto the nearest edge, maintaining interaction with wall tiles within game mechanics."
    },
    {
        "source": "PlayerCharacter",
        "target": "WallTiles",
        "effect": "killIfFrontal",
        "explain": "The 'killIfFrontal' effect will result in the immediate removal of the player character sprite if it moves diagonally as opposed to directly upwards or downwards, simulating a collision with wall tiles when not moving horizontally."
    }
]

const terminations = [
    {
        "termination": "Timeout",
        "target": null,
        "value": "Reaches time limit",
        "explain": "The game terminates when the player fails to reach the exit before the imposed time limit is reached. As this condition directly relates to a predeteinability and cannot be influenced by the player's actions like avoiding wall tiles or reaching goals, it fits as an appropriate termination rule."
    }
]

function process({ entities, rules, terminations }) {
    const level_mapping = Object.keys(entities).reduce((acc, key) => {
        acc[key] = key[0];
        return acc;
    }, {});

    const SpriteSetStr = Object.keys(entities).map((name) => `\t\t${name} > ${entities[name]}`).join("\n")
    const LevelMappingStr = Object.keys(level_mapping).map((name) => `\t\t${level_mapping[name]} > ${name}`).join("\n")
    const InteractionSetStr = rules.map((effect) => `\t\t${effect.source} ${effect.target} > ${effect.effect}`).join("\n")
    const TerminationSetStr = terminations.map((term) => `\t\t${term.termination}  win=False`).join("\n")
    return `
BasicGame
    SpriteSet
${SpriteSetStr}
    LevelMapping
${LevelMappingStr}
    InteractionSet
${InteractionSetStr}
    TerminationSet
${TerminationSetStr}
`
}

console.log(process({ entities, rules, terminations }))

