import os
import json
import urllib.parse
from datetime import datetime, timedelta

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
OUTPUT_FILE = "test.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 1. 置顶图标
TOP_ICON_NAME = "lige"

# 2. 指定要扫描的文件夹
TARGET_FOLDERS = [
    "01Country"
]
# ===========================================

def generate_test_json():
    print(f"🚀 正在生成测试文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # --- 1. 添加置顶图标 (lige) ---
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
                # 防重：跳过和置顶同名的
                if name == TOP_ICON_NAME: continue
                
                full_url = f"{BASE_URL}icon/{folder}/{urllib.parse.quote(filename)}"
                final_list.append({"name": name, "url": full_url})

    # --- 3. 生成头部信息 (日期) ---
    # 获取北京时间
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    # 格式化日期 (例如 251220)
    version_date = now_beijing.strftime('%y%m%d')
    
    description_text = f"无偿求更，图标更新请关注TG频道：@ligeicon ，您当前版本日期为{version_date}"

    # --- 4. 组装最终 JSON 结构 ---
    data = {
        "name": "离歌图标包",
        "description": description_text,
        "icons": final_list
    }

    # --- 5. 写入文件 ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ 生成完毕: {OUTPUT_FILE} (版本 {version_date}, 共 {len(final_list)} 个图标)")

if __name__ == "__main__":
    generate_test_json()
