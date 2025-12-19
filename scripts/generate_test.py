import os
import json
import urllib.parse
from datetime import datetime, timedelta

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
OUTPUT_FILE = "test.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 1. 置顶图标 (文件名，无后缀)
TOP_ICON_NAME = "lige"

# 2. 指定要扫描的文件夹
TARGET_FOLDERS = [
    "01Country",
    "02ProxySoftLogo",
    "03CNSoft",
    "04ProxySoft"
]
# ===========================================

def generate_test_json():
    print(f"🚀 正在生成测试文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # --- 1. 添加置顶图标 ---
    top_icon_path = os.path.join(ROOT_ICON_DIR, f"{TOP_ICON_NAME}.png")
    if os.path.exists(top_icon_path):
        print(f"👑 添加置顶: {TOP_ICON_NAME}")
        final_list.append({
            "name": TOP_ICON_NAME,
            "url": f"{BASE_URL}icon/{TOP_ICON_NAME}.png"
        })

    # --- 2. 扫描指定文件夹 ---
    if os.path.exists(ROOT_ICON_DIR):
        for folder in TARGET_FOLDERS:
            folder_path = os.path.join(ROOT_ICON_DIR, folder)
            
            if not os.path.exists(folder_path):
                print(f"⚠️ 跳过不存在的文件夹: {folder}")
                continue
                
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))]
            images.sort(key=lambda x: x.lower())
            
            print(f"   📂 扫描 [{folder}]: {len(images)} 个")

            for filename in images:
                name = os.path.splitext(filename)[0]
                # 防重
                if name == TOP_ICON_NAME: continue
                
                # ✅✅✅ 核心修复：safe='()' 
                # 意思是：编码时，忽略括号，保持 (1) 原样
                # Argentina(1).png -> Argentina(1).png
                # Argentina (1).png -> Argentina%20(1).png (只转义空格)
                encoded_name = urllib.parse.quote(filename, safe='()')
                
                full_url = f"{BASE_URL}icon/{folder}/{encoded_name}"
                final_list.append({"name": name, "url": full_url})

    # --- 3. 生成头部信息 ---
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    version_date = now_beijing.strftime('%y%m%d')
    
    description_text = f"无偿求更，图标更新请关注TG频道：@ligeicon ，您当前版本日期为{version_date}"

    data = {
        "name": "离歌图标包",
        "description": description_text,
        "icons": final_list
    }

    # --- 4. 写入文件 ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    # --- 5. 处理斜杠转义 (QuanX 必需) ---
    with open(OUTPUT_FILE, 'r+', encoding='utf-8') as f:
        content = f.read().replace("/", "\\/")
        f.seek(0); f.write(content); f.truncate()
        
    print(f"✅ 生成完毕: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_test_json()
