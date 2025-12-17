import os
import json
from datetime import datetime

# === 配置区 ===
# 存放额外图片的文件夹
ICON_DIR = "icon" 
# 链接前缀
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/icon/"
JSON_FILE = "lige-emby-icon.json"

# === 核心：绝对固定的 26 个图标数据 ===
# 无论文件夹里有没有，都会按这个顺序出现在 JSON 最前面
FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def update_json():
    # 1. 首先直接生成这 26 个固定的列表
    final_icons = []
    for name in FIXED_ICONS:
        final_icons.append({
            "name": name,
            "url": f"{BASE_URL}{name}.png"
        })

    # 2. 扫描文件夹，寻找“额外”的图标
    if os.path.exists(ICON_DIR):
        # 获取所有 png 文件名（不带后缀）
        all_files = [os.path.splitext(f)[0] for f in os.listdir(ICON_DIR) if f.lower().endswith('.png')]
        
        # 找出不在固定名单里的额外图标
        extra_names = []
        for file_name in all_files:
            if file_name not in FIXED_ICONS:
                extra_names.append(file_name)
        
        # 3. 对额外图标进行首字母 A-Z 排序
        extra_names.sort(key=lambda x: x.lower())
        
        # 4. 将排序后的额外图标添加到列表末尾
        for name in extra_names:
            final_icons.append({
                "name": name,
                "url": f"{BASE_URL}{name}.png"
            })

    # 5. 组装最终 JSON 结构
    today_str = datetime.now().strftime("%y%m%d")
    data = {
        "name": "离歌emby专用",
        "description": f"无偿求更，图标包更新请关注TG频道：@ligeicon 您当前版本日期为{today_str}",
        "icons": final_icons
    }

    # 6. 写入文件并处理转义斜杠 \/
    with open(JSON_FILE, 'w', encoding='utf-8') as jf:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        content = content.replace("/", "\\/")
        jf.write(content)

    print(f"✅ 处理完成！")
    print(f"📌 固定图标：{len(FIXED_ICONS)} 个（强制保留）")
    print(f"📌 额外图标：{len(final_icons) - len(FIXED_ICONS)} 个（自动排序）")

if __name__ == "__main__":
    update_json()
