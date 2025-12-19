import os
import json
import urllib.parse

# ================= 配置区域 =================
# 图标根目录
ROOT_ICON_DIR = "icon"

# ✅ 测试输出文件 (生成到根目录的 test.json)
OUTPUT_FILE = "test.json"

# 你的仓库 Raw 地址
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"
# ===========================================

def generate_test_json():
    print(f"🚀 正在生成测试文件: {OUTPUT_FILE}")
    
    final_list = []
    
    if not os.path.exists(ROOT_ICON_DIR):
        print(f"❌ 错误: 找不到目录 {ROOT_ICON_DIR}")
        return

    # --- 1. 获取分类文件夹并排序 (01, 02...) ---
    # 排除 emby 和 隐藏文件
    subfolders = sorted([
        f for f in os.listdir(ROOT_ICON_DIR) 
        if os.path.isdir(os.path.join(ROOT_ICON_DIR, f)) 
        and f != 'emby' 
        and not f.startswith('.')
    ])

    print(f"📋 识别到的分类顺序: {subfolders}")

    # --- 2. 遍历文件夹 ---
    for folder in subfolders:
        folder_path = os.path.join(ROOT_ICON_DIR, folder)
        
        # 获取图片
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))]
        
        # --- 3. 内部按文件名 A-Z 排序 ---
        images.sort(key=lambda x: x.lower())
        
        if not images:
            continue
            
        print(f"   📂 分类 [{folder}]: {len(images)} 个图标")

        # 加入列表
        for filename in images:
            name = os.path.splitext(filename)[0]
            # 路径: icon/01Country/xxx.png
            full_url = f"{BASE_URL}icon/{folder}/{urllib.parse.quote(filename)}"
            
            final_list.append({
                "name": name,
                "url": full_url
            })

    # --- 4. (可选) 扫描根目录散图，排在最后 ---
    root_images = sorted([
        f for f in os.listdir(ROOT_ICON_DIR) 
        if os.path.isfile(os.path.join(ROOT_ICON_DIR, f)) 
        and f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))
    ])
    
    if root_images:
        print(f"   📂 根目录散图: {len(root_images)} 个")
        for filename in root_images:
            name = os.path.splitext(filename)[0]
            full_url = f"{BASE_URL}icon/{urllib.parse.quote(filename)}"
            final_list.append({"name": name, "url": full_url})

    # --- 5. 写入 test.json ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"✅ 测试文件生成完毕: {OUTPUT_FILE} (共 {len(final_list)} 个)")

if __name__ == "__main__":
    generate_test_json()
