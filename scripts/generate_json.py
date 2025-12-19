import os
import json
import urllib.parse

# === 配置区 ===
ROOT_ICON_DIR = "icon"
EMBY_ICON_DIR = "icon/emby"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

MAIN_JSON_FILE = "QuanX-icon-rule.json"
EMBY_JSON_FILE = "lige-emby-icon.json"

FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def generate_main_json():
    print("🚀 [1/2] 正在生成主 JSON (自动扫描)...")
    all_icons_data = []
    
    if not os.path.exists(ROOT_ICON_DIR):
        print(f"❌ 错误: 找不到目录 {ROOT_ICON_DIR}")
        return

    # 扫描一级目录并排序
    subfolders = sorted([
        f for f in os.listdir(ROOT_ICON_DIR) 
        if os.path.isdir(os.path.join(ROOT_ICON_DIR, f)) and not f.startswith('.')
    ])

    for folder in subfolders:
        folder_path = os.path.join(ROOT_ICON_DIR, folder)
        images = sorted([
            f for f in os.listdir(folder_path) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))
        ])
        
        if not images: continue
        print(f"   📂 扫描: {folder} ({len(images)} 个)")

        for filename in images:
            name = os.path.splitext(filename)[0]
            relative_path = f"{ROOT_ICON_DIR}/{folder}/{filename}"
            encoded_path = urllib.parse.quote(relative_path)
            
            all_icons_data.append({
                "name": name,
                "url": BASE_URL + encoded_path
            })

    with open(MAIN_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_icons_data, f, indent=2, ensure_ascii=False)
    print(f"✅ 主 JSON 生成完毕，共 {len(all_icons_data)} 个。")

def generate_emby_json():
    print("🚀 [2/2] 正在生成 Emby JSON...")
    final_icons = []
    
    # 固定图标
    for name in FIXED_ICONS:
        final_icons.append({"name": name, "url": f"{BASE_URL}icon/{name}.png"})

    # Emby 目录图标
    if os.path.exists(EMBY_ICON_DIR):
        emby_files = sorted([f for f in os.listdir(EMBY_ICON_DIR) if f.lower().endswith('.png')], key=lambda x: x.lower())
        for file in emby_files:
            name = os.path.splitext(file)[0]
            if name not in FIXED_ICONS:
                encoded_file = urllib.parse.quote(file)
                final_icons.append({"name": name, "url": f"{BASE_URL}icon/emby/{encoded_file}"})

    data = {
        "name": "离歌emby专用",
        "description": "无偿求更，图标更新请关注TG频道：@ligeicon", # 日期在 TG 脚本里体现即可，或者保持静态
        "icons": final_icons
    }
    
    with open(EMBY_JSON_FILE, 'w', encoding='utf-8') as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)
    
    # 修正斜杠
    with open(EMBY_JSON_FILE, 'r+', encoding='utf-8') as jf:
        content = jf.read().replace("/", "\\/")
        jf.seek(0); jf.write(content); jf.truncate()
        
    print("✅ Emby JSON 生成完毕。")

if __name__ == "__main__":
    generate_main_json()
    generate_emby_json()
