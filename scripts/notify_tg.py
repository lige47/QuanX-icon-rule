import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

def run():
    token = os.environ.get('TG_BOT_TOKEN')
    if not token:
        print("无 Token，跳过")
        return

    # 1. 统计数量
    count = 0
    for root, dirs, files in os.walk("icon"):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico')):
                count += 1

    # 2. 准备文案
    time_cn = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y年%m月%d日 %H:%M:%S')
    
    # 注意：这里的链接已经全部改回你的 ligeicon.json
    text = f"""<b>为了减少更新日志每次消息的内容篇幅，以后更新日志只写更新的内容，图标链接等会在该消息提供。该消息会长期置顶。</b>

图标排序为：国旗  代理软件logo  国内可直连软件图标  外网软件图标  无分类的图标 机场logo

复制以下图标库链接导入即可( 此图标包不包含Emby服图标，Emby图标请导入下面的那个)
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json

<a href="https://quantumult.app/x/open-app/ui?module=gallery&type=icon&action=add&content=%5B%22https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json%22%5D">QuantumultX一键导入</a>
<a href="https://www.nsloon.com/openloon/import?iconset=https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon.json">Loon一键导入</a>

Surge图标库链接：
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/ligeicon-surge.json

Emby图标库（只有Emby图标，建议 Fileball Senplayer Yamby Hills Forward 小幻影视 使用）
https://raw.githubusercontent.com/lige47/QuanX-icon-rule/main/lige-emby-icon.json

本频道链接：https://t.me/ligeicon    群组：https://t.me/ligeicon_group
需要适配图标群内反馈即可。无偿适配！！！

一些小的新增可能不会发频道，可以关注这个最近一次更新时间，来判断自己是不是最新的库。
Github地址：
https://github.com/lige47/QuanX-icon-rule
<b>最近一次更新时间为：{time_cn}  目前图标数为{count}个！</b>

自营正规流量卡：
<a href="https://lc.189sd.cn/index?k=WFpJYmVSWnFjTFk9">189卡业</a>  <a href="https://h5.gantanhao.com/url?value=pVC7v1759672595456">卡业联盟</a>
有任何流量卡问题联系： @lige0407_bot"""

    # 3. 发送
    try:
        url = f"https://api.telegram.org/bot{token}/editMessageText"
        data = {
            "chat_id": "@ligeicon", 
            "message_id": "91", 
            "text": text, 
            "parse_mode": "HTML", 
            "disable_web_page_preview": "true"
        }
        params = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url, data=params)
        urllib.request.urlopen(req)
        print("TG 发送成功")
    except Exception as e:
        print(f"TG 发送失败: {e}")

if __name__ == "__main__":
    run()
