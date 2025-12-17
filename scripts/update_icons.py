import os
import json
from datetime import datetime

# === 配置区 ===
# 1. 文件夹路径
ROOT_ICON_DIR = "icon"       # 存放固定 26 个图标的根目录
EMBY_ICON_DIR = "icon/emby"  # 存放新增图标的子目录

# 2. 基础 URL
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"
JSON_FILE = "lige-emby-icon.json"

# === 核心：绝对固定的 26 个图标数据 ===
# 脚本会直接在 JSON 开头生成这些条目，链接指向 icon 根目录
FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def update_json():
    final_icons = []
    
    # 1. 强制生成 26 个固定列表条目（路径指向 icon/）
    for name in FIXED_ICONS:
        final_icons.append({
            "name": name,
            "url": f"{BASE_URL}{ROOT_ICON_DIR}/{name}.png"
        })

    # 2. 仅扫描 icon/emby 文件夹，寻找“额外”需要排序的图标
    if os.path.exists(EMBY_ICON_DIR):
        # 获取 emby 子文件夹下所有 png 文件名（不带后缀）
        extra_files = [os.path.splitext(f)[0] for f in os.listdir(EMBY_ICON_DIR) if f.lower().endswith('.png')]
        
        # 3. 对额外图标进行首字母 A-Z 排序（忽略大小写）
        extra_files.sort(key=lambda x: x.lower())
        
        # 4. 将排序后的额外图标添加到列表末尾（路径指向 icon/emby/）
        for name in extra_files:
            # 排除掉可能在固定名单中已经存在的文件名，防止重复显示
            if name not in FIXED_ICONS:
                final_icons.append({
                    "name": name,
                    "url": f"{BASE_URL}{EMBY_ICON_DIR}/{name}.png"
                })

    # 5. 构造符合你要求的 JSON 对象结构
    today_str = datetime.now().strftime("%y%m%d")
    data = {
        "name": "离歌emby专用",
        "description": f"无偿求更，图标包更新请关注TG频道：@ligeicon 您当前版本日期为{today_str}",
        "icons": final_icons
    }

    # 6. 写入文件并处理转义斜杠 \/
    with open(JSON_FILE, 'w', encoding='utf-8') as jf:
        # 使用 json.dumps 保证格式对齐
        content = json.dumps(data, indent=2, ensure_ascii=False)
        # 将所有普通斜杠替换为转义斜杠
        content = content.replace("/", "\\/")
        jf.write(content)

    print(f"✅ 处理完成！")
    print(f"📌 固定图标：{len(FIXED_ICONS)} 个（来源：{ROOT_ICON_DIR}/）")
    print(f"📌 额外图标：{len(final_icons) - len(FIXED_ICONS)} 个（来源：{EMBY_ICON_DIR}/）")

if __name__ == "__main__":
    update_json()
