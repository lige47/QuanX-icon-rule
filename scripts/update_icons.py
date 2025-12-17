import os
import json
from datetime import datetime

# 1. 配置基础信息
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/icon/emby/"
ICON_DIR = "icon/emby"
JSON_FILE = "lige-emby-icon.json"

# 2. 定义前 26 个必须固定的图标名称 (严格匹配图片顺序)
FIXED_ORDER = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def update_json():
    # 获取文件夹内所有 png 图片
    if not os.path.exists(ICON_DIR):
        return

    files = [f for f in os.listdir(ICON_DIR) if f.lower().endswith('.png')]
    all_names_map = {os.path.splitext(f)[0]: f for f in files}

    final_icons = []
    
    # --- 逻辑 A：处理固定顺序部分 ---
    for name in FIXED_ORDER:
        if name in all_names_map:
            final_icons.append({
                "name": name,
                "url": f"{BASE_URL}{all_names_map[name]}"
            })
            del all_names_map[name] # 处理完后从 map 中移除

    # --- 逻辑 B：处理剩余部分（首字母排序） ---
    remaining_icons = []
    for name, filename in all_names_map.items():
        remaining_icons.append({
            "name": name,
            "url": f"{BASE_URL}{filename}"
        })
    # 按 name 字段忽略大小写排序
    remaining_icons.sort(key=lambda x: x['name'].lower())
    
    # 合并两部分
    final_icons.extend(remaining_icons)

    # 3. 构造最终的 JSON 对象结构
    today_str = datetime.now().strftime("%y%m%d")
    data = {
        "name": "离歌emby专用",
        "description": f"无偿求更，图标包更新请关注TG频道：@ligeicon 您当前版本日期为{today_str}",
        "icons": final_icons
    }

    # 4. 写入文件并处理转义斜杠 \/
    with open(JSON_FILE, 'w', encoding='utf-8') as jf:
        # 生成带缩进的 JSON 字符串
        content = json.dumps(data, indent=2, ensure_ascii=False)
        # 将所有 / 替换为 \/ 以符合你的格式要求
        content = content.replace("/", "\\/")
        jf.write(content)

    print(f"成功更新 {JSON_FILE}，当前总图标数：{len(final_icons)}")

if __name__ == "__main__":
    update_json()
