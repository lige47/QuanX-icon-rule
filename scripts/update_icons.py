import os
import json
from datetime import datetime

# 路径配置（注意：这里是相对于仓库根目录的路径）
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/icon/emby/"
ICON_DIR = "icon/emby"
JSON_FILE = "lige-emby-icon.json"

# 你图片中确认的 26 个固定图标顺序
FIXED_ORDER = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def update_json():
    if not os.path.exists(ICON_DIR):
        print(f"错误: 找不到目录 {ICON_DIR}")
        return

    # 1. 读取所有图片名
    files = [f for f in os.listdir(ICON_DIR) if f.lower().endswith('.png')]
    all_names_map = {os.path.splitext(f)[0]: f for f in files}

    final_icons = []
    
    # 2. 逻辑 A：填充固定部分
    for name in FIXED_ORDER:
        if name in all_names_map:
            final_icons.append({
                "name": name,
                "url": f"{BASE_URL}{all_names_map[name]}"
            })
            del all_names_map[name]

    # 3. 逻辑 B：剩余部分首字母排序
    remaining_icons = []
    for name, filename in all_names_map.items():
        remaining_icons.append({
            "name": name,
            "url": f"{BASE_URL}{filename}"
        })
    remaining_icons.sort(key=lambda x: x['name'].lower())
    
    final_icons.extend(remaining_icons)

    # 4. 组装 JSON (匹配你提供的图片格式)
    today_str = datetime.now().strftime("%y%m%d")
    data = {
        "name": "离歌emby专用",
        "description": f"无偿求更，图标包更新请关注TG频道：@ligeicon 您当前版本日期为{today_str}",
        "icons": final_icons
    }

    # 5. 写入并处理转义斜杠
    with open(JSON_FILE, 'w', encoding='utf-8') as jf:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        content = content.replace("/", "\\/")
        jf.write(content)

    print(f"成功更新 {JSON_FILE}，总图标数：{len(final_icons)}")

if __name__ == "__main__":
    update_json()
