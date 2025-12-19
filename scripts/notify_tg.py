import os
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

MAIN_JSON_FILE = "QuanX-icon-rule.json"

def send_tg_notify():
    print("📡 正在准备发送 TG 通知...")
    token = os.environ.get('TG_BOT_TOKEN')
    if not token:
        print("⚠️ 未找到 TG_BOT_TOKEN，跳过通知。")
        return

    # 1. 读取 JSON 获取准确数量
    total_count = 0
    if os.path.exists(MAIN_JSON_FILE):
        with open(MAIN_JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_count = len(data)

    # 2. 准备时间
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    time_cn = now_beijing.strftime('%Y年%m月%d日 %H:%M:%S')

    # 3. 构造文案
    tg_template = """<b>为了减少更新日志每次消息的内容篇幅，以后更新日志只写更新的内容，图标链接等会在该消息提供。该消息会长期置顶。</b>

图标排序为：国旗  代理软件logo  国内可直连软件图标  外网软件图标  无分类的图标 机场logo

复制以下图标库链接导入即可( 此图标包不包含Emby服图标，Emby图标请导入下面的那个)
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/QuanX-icon-rule.json

<a href="https://quantumult.app/x/open-app/ui?module=gallery&type=icon&action=add&content=%5B%22https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/QuanX-icon-rule.json%22%5D">QuantumultX一键导入</a>
<a href="https://www.nsloon.com/openloon/import?iconset=https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/QuanX-icon-rule.json">Loon一键导入</a>

Surge图标库链接：
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon-surge.json

Emby图标库（只有Emby图标，建议 Fileball Senplayer Yamby Hills Forward 小幻影视 使用）
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/lige-emby-icon.json

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

    # 4. 发送请求
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
        print("✅ TG 消息更新成功")
    except Exception as e:
        print(f"❌ TG 发送失败: {e}")

if __name__ == "__main__":
    send_tg_notify()
