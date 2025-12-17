import os
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

# === 配置区 ===
ROOT_ICON_DIR = "icon"
EMBY_ICON_DIR = "icon/emby"
BASE_URL = "https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/"
JSON_FILE = "lige-emby-icon.json"

FIXED_ICONS = [
    "emby", "chinamobilemcloud", "189", "chinaunicomcloud", "123", "115", 
    "quark", "alicloud", "alidrive", "baidunetdisk", "baidunetdisk(1)", 
    "pikpak", "pCloud", "jianguoyun", "OneDrive", "OneDrive(1)", 
    "alist", "alist(1)", "OpenList", "clouddrive2", "jellyfin", 
    "xiaohuanRodelPlayer", "NAS", "NAS(1)", "NAS(2)", "qunhuiguanjia"
]

def update_all():
    # --- 1. 统计逻辑：递归扫描全目录 (只为了算总数) ---
    total_count = 0
    for root, dirs, files in os.walk(ROOT_ICON_DIR):
        for file in files:
            if file.lower().endswith(".png"):
                total_count += 1
    
    print(f"📊 全站图标统计完成：{total_count}")

    # --- 2. JSON 生成逻辑：固定 + icon/emby ---
    final_icons = []
    
    # A. 固定图标
    for name in FIXED_ICONS:
        final_icons.append({"name": name, "url": f"{BASE_URL}icon/{name}.png"})

    # B. Emby 目录图标
    if os.path.exists(EMBY_ICON_DIR):
        emby_files = [f for f in os.listdir(EMBY_ICON_DIR) if f.lower().endswith('.png')]
        emby_files.sort(key=lambda x: x.lower())
        for file in emby_files:
            name = os.path.splitext(file)[0]
            if name not in FIXED_ICONS:
                final_icons.append({"name": name, "url": f"{BASE_URL}icon/emby/{file}"})

    # 计算时间
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    time_std = now_beijing.strftime('%Y-%m-%d %H:%M:%S')
    time_cn = now_beijing.strftime('%Y年%m月%d日 %H:%M:%S')
    date_short = now_beijing.strftime('%y%m%d')

    # C. 写入 JSON (名字恢复为"离歌emby专用"，简介保持单行连贯)
    data = {
        "name": "离歌emby专用",
        "description": f"无偿求更，图标更新请关注TG频道：@ligeicon ，您当前版本日期为{date_short}",
        "icons": final_icons
    }
    
    with open(JSON_FILE, 'w', encoding='utf-8') as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)
    
    # 处理转义斜杠
    with open(JSON_FILE, 'r+', encoding='utf-8') as jf:
        content = jf.read().replace("/", "\\/")
        jf.seek(0); jf.write(content); jf.truncate()
        
    print(f"✅ JSON 生成完成，name='离歌emby专用'，description已补全。")

    # --- 3. 修改 README.md (强制双换行实现“单独一行”) ---
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        
        # 清理旧行
        readme = re.sub(r"🕒 本项目最近更新于：.*?\n?", "", readme)
        readme = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \(共计 \d+ 个图标\)\n?", "", readme)
        
        # 构造新行 (前后双换行)
        new_time_line = f"\n\n🕒 本项目最近更新于：{time_std} (共计 {total_count} 个图标)\n\n"
        
        # 插入
        if "### 项目简介：" in readme:
            readme = readme.replace("### 项目简介：", f"{new_time_line}### 项目简介：", 1)
        elif "项目简介" in readme:
            readme = readme.replace("项目简介", f"{new_time_line}项目简介", 1)
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
        print("✅ README 更新完成")

    # --- 4. 更新 TG 消息 ---
    token = os.environ.get('TG_BOT_TOKEN')
    if token:
        tg_template = """<b>为了减少更新日志每次消息的内容篇幅，以后更新日志只写更新的内容，图标链接等会在该消息提供。该消息会长期置顶。</b>

图标排序为：国旗  代理软件logo  国内可直连软件图标  外网软件图标  无分类的图标 机场logo

复制以下图标库链接导入即可( 此图标包不包含Emby服图标，Emby图标请导入下面的那个)
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json

<a href="https://quantumult.app/x/open-app/ui?module=gallery&type=icon&action=add&content=%5B%22https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json%22%5D">QuantumultX一键导入</a>
<a href="https://www.nsloon.com/openloon/import?iconset=https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json">Loon一键导入</a>

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
<a href="https://lc.189sd.cn/index?k=WFpJYmVSWnFjTFk9">189卡业</a>  <a href="https://h5.gantanhao.com/url?value=pVC7v1759672595456">卡业联盟</a>
有任何流量卡问题联系： @lige0407_bot"""

        final_text = tg_template.format(time_cn=time_cn, total_count=total_count)
        try:
            url = f"https://api.telegram.org/bot{token}/editMessageText"
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
            print("✅ TG 消息更新完成")
        except Exception as e:
            print(f"❌ TG 失败: {e}")

if __name__ == "__main__":
    update_all()
