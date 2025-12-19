import os
import json
import urllib.parse

# ================= 配置区域 =================
ROOT_ICON_DIR = "icon"
OUTPUT_FILE = "test.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 1. 想要固定在第一个的图标名称 (不需要写后缀)
TOP_ICON_NAME = "lige"

# 2. 指定要扫描的文件夹 (脚本会按列表顺序依次扫描)
# 你可以在这里填入 ["01Country", "02Proxysoft", "03App"]
TARGET_FOLDERS = [
    "01Country",
    "02Proxysoft"  # 假设你已经有了02，没有的话删掉这行
]
# ===========================================

def generate_test_json():
    print(f"🚀 正在生成测试文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # --- 第一步：强制添加 lige 图标 (排在第 1 位) ---
    # 假设 lige.png 在 icon/ 根目录下
    top_icon_path = os.path.join(ROOT_ICON_DIR, f"{TOP_ICON_NAME}.png")
    
    if os.path.exists(top_icon_path):
        print(f"👑 添加置顶图标: {TOP_ICON_NAME}")
        final_list.append({
            "name": TOP_ICON_NAME,
            "url": f"{BASE_URL}icon/{TOP_ICON_NAME}.png"
        })
    else:
        print(f"⚠️ 警告: 在根目录没找到 {TOP_ICON_NAME}.png，跳过置顶。")

    # --- 第二步：扫描指定的分类文件夹 (01, 02...) ---
    if not os.path.exists(ROOT_ICON_DIR):
        print(f"❌ 错误: 找不到根目录 {ROOT_ICON_DIR}")
        return

    for folder in TARGET_FOLDERS:
        folder_path = os.path.join(ROOT_ICON_DIR, folder)
        
        # 1. 检查文件夹
        if not os.path.exists(folder_path):
            print(f"⚠️ 警告: 找不到文件夹 {folder}，跳过...")
            continue
            
        # 2. 获取图片
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))]
        
        # 3. 排序 (A-Z)
        images.sort(key=lambda x: x.lower())
        
        if not images:
            continue
            
        print(f"   📂 处理分类 [{folder}]: {len(images)} 个图标")

        # 4. 加入列表
        for filename in images:
            name = os.path.splitext(filename)[0]
            
            # 防重判断：如果分类文件夹里也放了个 lige.png，跳过它，防止重复
            if name == TOP_ICON_NAME:
                continue

            full_url = f"{BASE_URL}icon/{folder}/{urllib.parse.quote(filename)}"
            
            final_list.append({
                "name": name,
                "url": full_url
            })

    # --- 第三步：写入 JSON ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"✅ 生成完毕: {OUTPUT_FILE} (共 {len(final_list)} 个)")

if __name__ == "__main__":
    generate_test_json()
