import os
import re
import json

# 获取脚本所在的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 切换当前工作目录到脚本所在路径
os.chdir(script_dir)

def categorize_txt_files(root_folder):
    game_categories = ["gridphysics", "2player", "contphysics", "gameDesign"]
    res = {
        game_cat: {} for game_cat in game_categories
    }
    
    games = {
        game_cat: [] for game_cat in game_categories
    }
    
    for game_cat in game_categories:
        for game in os.listdir(os.path.join(root_folder, game_cat)):
            if game.endswith(".txt"):
                games[game_cat].append(game)
    
    for game_cat in game_categories:
        for file_name in games[game_cat]:
            if "_" in file_name:
                continue
            # match = re.match(r'(\w*).txt', file_name)
            # if match:
                # game_name = match.groups()[0]
            rematch = re.search(r"_lvl[0-9]+.txt", file_name)
            if rematch: 
                continue
            game_name = file_name[:-4]
            match_level = game_name + r"_lvl[0-9]+.txt"
            res[game_cat][game_name] = []
            for file_name in games[game_cat]:
                match = re.search(match_level, file_name)
                if match:
                    level_file = match.group()
                    res[game_cat][game_name].append(level_file)
            
            if len(res[game_cat][game_name]) == 0:
                del res[game_cat][game_name]
                    
    return res

def write_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    games_folder = "games"  # 修改为你的games文件夹路径
    output_json_file = "config.json"  # 修改为你想要输出的JSON文件名

    categorized_files = categorize_txt_files(games_folder)
    write_to_json(categorized_files, output_json_file)

    print(f"TXT文件已分类并写入到 {output_json_file}")
