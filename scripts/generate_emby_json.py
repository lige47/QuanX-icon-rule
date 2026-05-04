import os
import json
import urllib.parse
from datetime import datetime, timedelta

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
EMBY_DIR = "icon/emby"
OUTPUT_FILE = "lige-emby-icon.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 固定顺序列表 (这些图标可能被你移动到了某个子文件夹里)
FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "senplayer","NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]
# ===========================================

def find_icon_url(icon_name):
    """
    全自动寻找图标：
    1. 先看根目录有没有
    2. 再遍历所有子文件夹 (01, 02...) 寻找
    """
    filename = f"{icon_name}.png"
    
    # 1. 检查根目录 (兼容旧习惯)
    root_path = os.path.join(ROOT_ICON_DIR, filename)
    if os.path.exists(root_path):
        encoded_name = urllib.parse.quote(filename, safe='()')
        return f"{BASE_URL}icon/{encoded_name}"
    
    # 2. 检查所有子文件夹
    if os.path.exists(ROOT_ICON_DIR):
        # 获取所有文件夹
        subfolders = [
            d for d in os.listdir(ROOT_ICON_DIR) 
            if os.path.isdir(os.path.join(ROOT_ICON_DIR, d)) 
        ]
        
        for folder in subfolders:
            # 拼接路径检查是否存在
            full_path = os.path.join(ROOT_ICON_DIR, folder, filename)
            if os.path.exists(full_path):
                # 找到了！生成带子文件夹的 URL
                encoded_folder = urllib.parse.quote(folder)
                encoded_name = urllib.parse.quote(filename, safe='()')
                return f"{BASE_URL}icon/{encoded_folder}/{encoded_name}"

    return None

def generate_emby():
    print(f"🚀 正在生成 Emby 专用文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # --- 1. 添加固定图标 (自动搜索位置) ---
    print(f"🔍 正在全目录搜索固定图标...")
    for name in FIXED_ICONS:
        url = find_icon_url(name)
        if url:
            final_list.append({"name": name, "url": url})
        else:
            print(f"⚠️ 警告: 找不到固定图标 {name}.png，已跳过")

    # --- 2. 扫描 icon/emby 文件夹 (Emby 内部图标) ---
    if os.path.exists(EMBY_DIR):
        files = [f for f in os.listdir(EMBY_DIR) if f.lower().endswith('.png')]
        # 按首字母排序
        files.sort(key=lambda x: x.lower())
        
        for filename in files:
            name = os.path.splitext(filename)[0]
            # 排重：如果在固定列表里就跳过
            if name in FIXED_ICONS:
                continue
            
            encoded_name = urllib.parse.quote(filename, safe='()')
            final_list.append({"name": name, "url": f"{BASE_URL}icon/emby/{encoded_name}"})

    # --- 3. 计算日期版本号 ---
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    version_date = now_beijing.strftime('%y%m%d')
    
    description_text = f"无偿求更，图标更新请关注TG频道：@ligeicon ，您当前版本日期为{version_date}"

    # --- 4. 构建 JSON ---
    data = {
        "name": "离歌Emby专用",
        "description": description_text,
        "icons": final_list
    }
    
    # --- 5. 写入文件 ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # --- 6. 斜杠转义 (QuanX) ---
    with open(OUTPUT_FILE, 'r+', encoding='utf-8') as f:
        content = f.read().replace("/", "\\/")
        f.seek(0); f.write(content); f.truncate()
        
    print(f"✅ 完成！(版本 {version_date}, 共 {len(final_list)} 个)")

if __name__ == "__main__":
    generate_emby()
