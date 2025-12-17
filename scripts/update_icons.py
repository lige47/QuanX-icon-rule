import os
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

# === 配置区 ===
ROOT_ICON_DIR = "icon"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"
JSON_FILE = "lige-emby-icon.json"

# 固定 26 个图标
FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def update_all():
    # --- 1. 递归扫描所有图标并计算总数 ---
    all_png_map = {}
    total_count = 0
    for root, dirs, files in os.walk(ROOT_ICON_DIR):
        for file in files:
            if file.lower().endswith(".png"):
                total_count += 1
                name = os.path.splitext(file)[0]
                rel_path = os.path.join(root, file).replace("\\", "/")
                all_png_map[name] = rel_path

    # --- 2. 生成 JSON ---
    final_icons = []
    temp_map = all_png_map.copy()
    for name in FIXED_ICONS:
        path = temp_map.pop(name, f"icon/{name}.png")
        final_icons.append({"name": name, "url": f"{BASE_URL}{path}"})
    
    remaining = sorted(temp_map.keys(), key=lambda x: x.lower())
    for name in remaining:
        final_icons.append({"name": name, "url": f"{BASE_URL}{temp_map[name]}"})

    today_beijing = datetime.utcnow() + timedelta(hours=8)
    time_std = today_beijing.strftime('%Y-%m-%d %H:%M:%S')
    time_cn = today_beijing.strftime('%Y年%m月%d日 %H:%M:%S')

    data = {"name": "离歌emby专用", "icons": final_icons}
    with open(JSON_FILE, 'w', encoding='utf-8') as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)
    # 强制处理转义斜杠
    with open(JSON_FILE, 'r+', encoding='utf-8') as jf:
        c = jf.read().replace("/", "\\/")
        jf.seek(0); jf.write(c); jf.truncate()

    # --- 3. 修改 README.md (精准替换) ---
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        # 彻底清理所有旧的时间行
        readme = re.sub(r"🕒 本项目最近更新于：.*?\n", "", readme)
        # 插入新行
        new_time_line = f"🕒 本项目最近更新于：{time_std} (共计 {total_count} 个图标)\n"
        readme = readme.replace("项目简介", f"{new_time_line}项目简介", 1)
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
        print(f"✅ README 更新完成，图标数：{total_count}")

    # --- 4. 更新 TG 消息 (加入 <b> 标签实现加粗) ---
    token = os.environ.get('TG_BOT_TOKEN')
    if token:
        # 使用 <b> 标签包裹你需要加粗的内容
        tg_template = """<b>为了减少更新日志每次消息的内容篇幅，以后更新日志只写更新的内容，图标链接等会在该消息提供。该消息会长期置顶。</b>

图标排序为：国旗  代理软件logo  国内可直连软件图标  外网软件图标  无分类的图标 机场logo

复制以下图标库链接导入即可( 此图标包不包含Emby服图标，Emby图标请导入下面的那个)
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json

QuantumultX一键导入 (https://quantumult.app/x/open-app/ui?module=gallery&type=icon&action=add&content=%5B%22https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json%22%5D)
Loon一键导入 (https://www.nsloon.com/openloon/import?iconset=https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json)

Surge图标库链接：
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon-surge.json

Emby图标库（只有Emby图标，建议 Fileball Senplayer Yamby Hills Forward 小幻影视 使用）
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/refs/heads/main/lige-emby-icon.json

本频道链接：https://t.me/ligeicon    群组：https://t.me/ligeicon_group
需要适配图标群内反馈即可。无偿适配！！！

一些小的新增可能不会发频道，可以关注这个最近一次更新时间，来判断自己是不是最新的库。
Github地址：
https://github.com/lige47/QuanX-icon-rule
<b>最近一次更新时间为：{time_cn}  目前图标数为{total_count}个！</b>

自营正规流量卡：
189卡业 (https://lc.189sd.cn/index?k=WFpJYmVSWnFjTFk9)  卡业联盟 (https://h5.gantanhao.com/url?value=pVC7v1759672595456)
有任何流量卡问题联系： @lige0407_bot"""

        final_text = tg_template.format(time_cn=time_cn, total_count=total_count)
        try:
            url = f"https://api.telegram.org/bot{token}/editMessageText"
            # 必须传 parse_mode=HTML
            data_dict = {
                "chat_id": "@ligeicon",
                "message_id": "91",
                "text": final_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": "true"
            }
            params = urllib.parse.urlencode(data_dict).encode("utf-8")
            req = urllib.request.Request(url, data=params)
            urllib.request.urlopen(req)
            print("✅ TG 消息加粗更新成功")
        except Exception as e:
            print(f"❌ TG 失败: {e}")

if __name__ == "__main__":
    update_all()
