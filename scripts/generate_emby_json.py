import os
import json
import urllib.parse
from datetime import datetime, timedelta

# ================= 配置区域 =================
EMBY_DIR = "icon/emby"
OUTPUT_FILE = "lige-emby-icon.json"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"

# 固定顺序列表
FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]
# ===========================================

def generate_emby():
    print(f"🚀 正在生成 Emby 专用文件: {OUTPUT_FILE}")
    
    final_list = []
    
    # 1. 添加固定图标
    for name in FIXED_ICONS:
        # 假设固定图标在 icon/ 根目录下
        final_list.append({"name": name, "url": f"{BASE_URL}icon/{name}.png"})

    # 2. 扫描文件夹并排序
    if os.path.exists(EMBY_DIR):
        files = [f for f in os.listdir(EMBY_DIR) if f.lower().endswith('.png')]
        # 按首字母排序
        files.sort(key=lambda x: x.lower())
        
        for filename in files:
            name = os.path.splitext(filename)[0]
            # 排重：如果在固定列表里就跳过
            if name in FIXED_ICONS:
                continue
            
            encoded_name = urllib.parse.quote(filename)
            final_list.append({"name": name, "url": f"{BASE_URL}icon/emby/{encoded_name}"})

    # --- 核心修改：计算日期版本号 ---
    # 获取北京时间 (UTC+8)
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    # 格式化为 251220 (年份后两位+月+日)
    version_date = now_beijing.strftime('%y%m%d')
    
    description_text = f"无偿求更，图标更新请关注TG频道：@ligeicon ，您当前版本日期为{version_date}"

    # 3. 构建 JSON
    data = {
        "name": "离歌Emby专用",
        "description": description_text,
        "icons": final_list
    }
    
    # 4. 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 5. 处理斜杠转义 (QuanX 兼容性)
    with open(OUTPUT_FILE, 'r+', encoding='utf-8') as f:
        content = f.read().replace("/", "\\/")
        f.seek(0); f.write(content); f.truncate()
        
    print(f"✅ 完成！版本号: {version_date}, 图标数: {len(final_list)}")

if __name__ == "__main__":
    generate_emby()
