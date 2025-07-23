import json

files = [
# "avatar_explanation.json",
# "condition_explanation.json",
"effect_explanation.json",
# "physics_explanation.json",
# "resource_explanation.json",
# "sprite_explanation.json",
# "termination_explanation.json",
]


for file in files:
    with open(file) as f:
        data = f.read()
        data:dict[str, str] = json.loads(data)
        new_data = {}
        for k, v in data.items():
            try:
                if "```json" in v:
                    new_data[k] = json.loads(v.split("```json")[1].split("```")[0])
                else:
                    new_data[k] = json.loads(v)
            except Exception as e:
                print("Error on")
                print(v)
        json.dump(new_data, open(f"2enhanced_{file}", "w"))