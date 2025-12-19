import os
import json
import urllib.parse

# === 配置区 ===
ROOT_ICON_DIR = "icon"
EMBY_ICON_DIR = "icon/emby"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# ✅ 修正：改回你原来的文件名
MAIN_JSON_FILE = "ligeicon.json"       
EMBY_JSON_FILE = "lige-emby-icon.json"

FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def generate_main_json():
    print(f"🚀 [1/2] 正在更新主文件: {MAIN_JSON_FILE} ...")
    all_icons_data = []
    
    if not os.path.exists(ROOT_ICON_DIR):
        print(f"❌ 错误: 找不到目录 {ROOT_ICON_DIR}")
        return

    # --- A. 扫描子文件夹 (01Country, 02Proxysoft...) ---
    subfolders = sorted([
        f for f in os.listdir(ROOT_ICON_DIR) 
        if os.path.isdir(os.path.join(ROOT_ICON_DIR, f)) 
        and not f.startswith('.') 
        and f != 'emby' 
    ])

    for folder in subfolders:
        folder_path = os.path.join(ROOT_ICON_DIR, folder)
        images = sorted([
            f for f in os.listdir(folder_path) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))
        ])
        
        if not images: continue
        print(f"   📂 扫描分类: {folder} ({len(images)} 个)")

        for filename in images:
            name = os.path.splitext(filename)[0]
            relative_path = f"{ROOT_ICON_DIR}/{folder}/{filename}"
            encoded_path = urllib.parse.quote(relative_path)
            all_icons_data.append({"name": name, "url": BASE_URL + encoded_path})

    # --- B. 扫描根目录下的散乱图片 ---
    root_images = sorted([
        f for f in os.listdir(ROOT_ICON_DIR) 
        if os.path.isfile(os.path.join(ROOT_ICON_DIR, f)) 
        and f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))
    ])
    
    if root_images:
        print(f"   📂 扫描根目录散乱图标 ({len(root_images)} 个)")
        for filename in root_images:
            name = os.path.splitext(filename)[0]
            relative_path = f"{ROOT_ICON_DIR}/{filename}"
            encoded_path = urllib.parse.quote(relative_path)
            all_icons_data.append({"name": name, "url": BASE_URL + encoded_path})

    with open(MAIN_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_icons_data, f, indent=2, ensure_ascii=False)
    print(f"✅ {MAIN_JSON_FILE} 更新完毕，包含 {len(all_icons_data)} 个图标。")

def generate_emby_json():
    print(f"🚀 [2/2] 正在更新 Emby 文件: {EMBY_JSON_FILE} ...")
    final_icons = []
    
    # 1. 固定图标
    for name in FIXED_ICONS:
        final_icons.append({"name": name, "url": f"{BASE_URL}icon/{name}.png"})

    # 2. Emby 目录图标
    if os.path.exists(EMBY_ICON_DIR):
        emby_files = sorted([f for f in os.listdir(EMBY_ICON_DIR) if f.lower().endswith('.png')], key=lambda x: x.lower())
        for file in emby_files:
            name = os.path.splitext(file)[0]
            if name not in FIXED_ICONS:
                encoded_file = urllib.parse.quote(file)
                final_icons.append({"name": name, "url": f"{BASE_URL}icon/emby/{encoded_file}"})

    data = {
        "name": "离歌emby专用",
        "description": "无偿求更，图标更新请关注TG频道：@ligeicon",
        "icons": final_icons
    }
    
    with open(EMBY_JSON_FILE, 'w', encoding='utf-8') as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)
    
    # 修正斜杠
    with open(EMBY_JSON_FILE, 'r+', encoding='utf-8') as jf:
        content = jf.read().replace("/", "\\/")
        jf.seek(0); jf.write(content); jf.truncate()
        
    print(f"✅ {EMBY_JSON_FILE} 更新完毕。")

if __name__ == "__main__":
    generate_main_json()
    generate_emby_json()
