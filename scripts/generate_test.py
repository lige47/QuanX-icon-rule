import os
import json
import urllib.parse

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
OUTPUT_FILE = "test.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# ✅ 重点：只扫描列表里指定的文件夹
# 你想测哪个，就写哪个，注意大小写要和文件夹名完全一致
TARGET_FOLDERS = [
    "01Country"
]
# ===========================================

def generate_test_json():
    print(f"🚀 正在生成测试文件: {OUTPUT_FILE}")
    print(f"🎯 指定扫描目录: {TARGET_FOLDERS}")
    
    final_list = []
    
    if not os.path.exists(ROOT_ICON_DIR):
        print(f"❌ 错误: 找不到根目录 {ROOT_ICON_DIR}")
        return

    # --- 遍历你指定的文件夹 ---
    for folder in TARGET_FOLDERS:
        folder_path = os.path.join(ROOT_ICON_DIR, folder)
        
        # 1. 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"⚠️ 警告: 找不到文件夹 {folder}，跳过...")
            continue
            
        # 2. 获取图片
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))]
        
        # 3. 按文件名 A-Z 排序
        images.sort(key=lambda x: x.lower())
        
        if not images:
            print(f"⚠️ 警告: 文件夹 {folder} 是空的")
            continue
            
        print(f"   📂 处理分类 [{folder}]: 包含 {len(images)} 个图标")

        # 4. 加入列表
        for filename in images:
            name = os.path.splitext(filename)[0]
            # 路径: icon/01Country/xxx.png
            full_url = f"{BASE_URL}icon/{folder}/{urllib.parse.quote(filename)}"
            
            final_list.append({
                "name": name,
                "url": full_url
            })

    # --- 写入 test.json ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"✅ 测试文件生成完毕: {OUTPUT_FILE} (共 {len(final_list)} 个)")

if __name__ == "__main__":
    generate_test_json()
