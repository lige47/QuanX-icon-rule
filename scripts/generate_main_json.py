import os
import json
import urllib.parse
from datetime import datetime, timedelta

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
# ✅ 正式版输出文件名
OUTPUT_FILE = "ligeicon.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 1. 置顶图标 (文件名，无后缀)
TOP_ICON_NAME = "lige"

# 2. 不需要扫描的文件夹 (黑名单)
# emby 由另一个脚本管理，所以这里跳过
EXCLUDE_FOLDERS = ["emby", ".git", ".github"]
# ===========================================

def generate_main_json():
    print(f"🚀 正在生成正式版文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # --- 1. 添加置顶图标 (lige) ---
    # 自动去全目录找 lige.png 在哪 (防止你把它移动到了子文件夹)
    top_icon_found = False
    # 先看根目录
    if os.path.exists(os.path.join(ROOT_ICON_DIR, f"{TOP_ICON_NAME}.png")):
         final_list.append({"name": TOP_ICON_NAME, "url": f"{BASE_URL}icon/{TOP_ICON_NAME}.png"})
         top_icon_found = True
         print(f"👑 添加置顶: {TOP_ICON_NAME} (根目录)")
    
    # --- 2. 自动获取并排序所有分类文件夹 ---
    if not os.path.exists(ROOT_ICON_DIR):
        print(f"❌ 错误: 找不到目录 {ROOT_ICON_DIR}")
        return

    # 获取所有文件夹，并过滤掉黑名单
    subfolders = sorted([
        f for f in os.listdir(ROOT_ICON_DIR) 
        if os.path.isdir(os.path.join(ROOT_ICON_DIR, f)) 
        and f not in EXCLUDE_FOLDERS
        and not f.startswith('.')
    ])

    print(f"📋 识别到的分类顺序: {subfolders}")

    # --- 3. 遍历文件夹生成数据 ---
    for folder in subfolders:
        folder_path = os.path.join(ROOT_ICON_DIR, folder)
        
        # 获取图片
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))]
        # 按文件名 A-Z 排序
        images.sort(key=lambda x: x.lower())
        
        if not images: continue
        
        print(f"   📂 扫描 [{folder}]: {len(images)} 个")

        for filename in images:
            name = os.path.splitext(filename)[0]
            
            # 防重：如果之前没找到置顶，且当前图标是置顶图标，则添加并标记
            if name == TOP_ICON_NAME:
                if not top_icon_found:
                    # 如果刚才没在根目录找到，现在找到了，把它插到最前面
                    encoded_name = urllib.parse.quote(filename, safe='()')
                    final_list.insert(0, {
                        "name": name, 
                        "url": f"{BASE_URL}icon/{folder}/{encoded_name}"
                    })
                    top_icon_found = True
                    print(f"👑 添加置顶: {TOP_ICON_NAME} (在 {folder} 中找到)")
                continue # 跳过，防止重复添加

            # URL 编码 (保留括号，转义中文/空格)
            encoded_name = urllib.parse.quote(filename, safe='()')
            full_url = f"{BASE_URL}icon/{folder}/{encoded_name}"
            
            final_list.append({"name": name, "url": full_url})

    # --- 4. 生成头部信息 (日期) ---
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    version_date = now_beijing.strftime('%y%m%d')
    
    description_text = f"无偿求更，图标更新请关注TG频道：@ligeicon ，您当前版本日期为{version_date}"

    data = {
        "name": "离歌图标包",
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
        
    print(f"✅ 正式版生成完毕: {OUTPUT_FILE} (共 {len(final_list)} 个)")

if __name__ == "__main__":
    generate_main_json()
