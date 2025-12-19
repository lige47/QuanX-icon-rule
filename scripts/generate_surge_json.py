import os
import json
import urllib.parse
from datetime import datetime, timedelta

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
# ✅ Surge 专用输出文件名
OUTPUT_FILE = "ligeicon-surge.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 1. 置顶图标
TOP_ICON_NAME = "lige"

# 2. 排除的文件夹 (保持和主脚本一致)
EXCLUDE_FOLDERS = ["emby", ".git", ".github"]
# ===========================================

def generate_surge_json():
    print(f"🚀 正在生成 Surge 专用文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # --- 1. 添加置顶图标 (lige) ---
    top_icon_found = False
    if os.path.exists(os.path.join(ROOT_ICON_DIR, f"{TOP_ICON_NAME}.png")):
         final_list.append({"name": TOP_ICON_NAME, "url": f"{BASE_URL}icon/{TOP_ICON_NAME}.png"})
         top_icon_found = True
         print(f"👑 添加置顶: {TOP_ICON_NAME}")

    # --- 2. 扫描所有分类文件夹 ---
    if os.path.exists(ROOT_ICON_DIR):
        # 获取文件夹并排序
        subfolders = sorted([
            f for f in os.listdir(ROOT_ICON_DIR) 
            if os.path.isdir(os.path.join(ROOT_ICON_DIR, f)) 
            and f not in EXCLUDE_FOLDERS
            and not f.startswith('.')
        ])

        for folder in subfolders:
            folder_path = os.path.join(ROOT_ICON_DIR, folder)
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))]
            images.sort(key=lambda x: x.lower())
            
            if not images: continue
            print(f"   📂 扫描 [{folder}]: {len(images)} 个")

            for filename in images:
                name = os.path.splitext(filename)[0]
                
                # 防重逻辑
                if name == TOP_ICON_NAME:
                    if not top_icon_found:
                        encoded_name = urllib.parse.quote(filename, safe='()')
                        final_list.insert(0, {
                            "name": name, 
                            "url": f"{BASE_URL}icon/{folder}/{encoded_name}"
                        })
                        top_icon_found = True
                    continue

                # URL 编码
                encoded_name = urllib.parse.quote(filename, safe='()')
                full_url = f"{BASE_URL}icon/{folder}/{encoded_name}"
                
                final_list.append({"name": name, "url": full_url})

    # --- 3. 生成 Surge 专用头部 ---
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    version_date = now_beijing.strftime('%y%m%d')
    
    # 按照你的要求：Name 带版本号，且没有 description
    surge_name = f"TG频道@ligeicon 版本{version_date}"

    data = {
        "name": surge_name,
        "icons": final_list
    }

    # --- 4. 写入文件 ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    # --- 5. 斜杠转义 (保持一致性) ---
    with open(OUTPUT_FILE, 'r+', encoding='utf-8') as f:
        content = f.read().replace("/", "\\/")
        f.seek(0); f.write(content); f.truncate()
        
    print(f"✅ Surge 文件生成完毕: {OUTPUT_FILE} (版本 {version_date})")

if __name__ == "__main__":
    generate_surge_json()
