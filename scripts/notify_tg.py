import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

# 配置图标根目录 (用于统计数量)
ROOT_DIR = "icon"

def run():
    token = os.environ.get('TG_BOT_TOKEN')
    if not token:
        print("⚠️ 无 Token，跳过 TG 通知")
        return

    # 1. 扫描硬盘统计真实数量
    count = 0
    if os.path.exists(ROOT_DIR):
        for root, dirs, files in os.walk(ROOT_DIR):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico')):
                    count += 1
    
    print(f"📊 统计数量: {count}")

    # 2. 准备时间
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    time_cn = now_beijing.strftime('%Y年%m月%d日 %H:%M:%S')
    
    # 3. 准备文案 (HTML 格式)
    # 注意：f""" ... """ 里的 {time_cn} 和 {count} 会自动替换为变量值
    text = f"""<b>为了减少更新日志每次消息的内容篇幅，以后更新日志只写更新的内容，图标链接等会在该消息提供。该消息会长期置顶。</b>

图标排序为：国旗  代理软件logo  国内可直连软件图标  外网软件图标  无分类的图标 机场logo

<b>复制以下图标库链接导入即可( 此图标库不包含Emby服图标，Emby图标请导入下面的那个)</b>
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json

<a href="https://quantumult.app/x/open-app/ui?module=gallery&type=icon&action=add&content=%5B%22https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json%22%5D">QuantumultX一键导入</a>
<a href="https://www.nsloon.com/openloon/import?iconset=https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json">Loon一键导入</a>

<b>Emby图标库（只有Emby图标，建议 Senplayer Fileball Yamby Hills Forward 小幻影视等软件使用）</b>
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/lige-emby-icon.json

<a href="https://lige47.github.io/QuanX-icon-rule/scripts/import.html?iconset=https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/lige-emby-icon.json">Senplayer一键导入</a>

本频道链接：https://t.me/ligeicon    群组：https://t.me/ligeicon_group
需要适配图标群内反馈即可。无偿适配！！！

一些小的新增可能不会发频道，可以关注这个最近一次更新时间，来判断自己是不是最新的库。
Github地址：
https://github.com/lige47/QuanX-icon-rule
<b>最近一次更新时间为：{time_cn}  目前图标数为{count}个！</b>

自营正规流量卡：
<a href="https://lc.189sd.cn/index?k=WFpJYmVSWnFjTFk9">189卡业</a>  <a href="https://h5.gantanhao.com/url?value=pVC7v1759672595456">卡业联盟</a>
有任何流量卡问题联系： @lige0407_bot"""

    # 4. 发送请求
    try:
        url = f"https://api.telegram.org/bot{token}/editMessageText"
        data = {
            "chat_id": "@ligeicon", 
            "message_id": "91",  # 确保这个消息ID是你频道那条置顶消息的ID
            "text": text, 
            "parse_mode": "HTML", 
            "disable_web_page_preview": "true"
        }
        params = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url, data=params)
        urllib.request.urlopen(req)
        print("✅ TG 发送成功")
    except Exception as e:
        print(f"❌ TG 发送失败: {e}")

if __name__ == "__main__":
    run()
