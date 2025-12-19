import os
import re
from datetime import datetime, timedelta

# 配置图标根目录
ROOT_DIR = "icon"

def run():
    # 1. 扫描硬盘统计真实数量
    count = 0
    if os.path.exists(ROOT_DIR):
        for root, dirs, files in os.walk(ROOT_DIR):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico')):
                    count += 1
    
    print(f"📊 统计到图标总数: {count}")

    # 2. 获取时间
    time_str = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

    # 3. 更新 README.md
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # --- 核心修改区 START ---
        
        # 动作 A：删除【旧格式】(截图里上面那行纯日期的)
        # 匹配逻辑：日期 + (共计 数字 个图标)
        content = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \(共计 \d+ 个图标\)\n*", "", content)

        # 动作 B：删除【新格式】(避免重复自己)
        # 匹配逻辑：🕒 + 任意文字 + 换行
        content = re.sub(r"🕒 本项目最近更新于：.*?\n*", "", content)
        
        # 动作 C：清理可能产生的多余空行 (超过3个换行变成2个)
        content = re.sub(r"\n{3,}", "\n\n", content)

        # --- 核心修改区 END ---
        
        # 插入新的一行
        new_line = f"\n\n🕒 本项目最近更新于：{time_str} (共计 {count} 个图标)\n\n"
        
        if "### 项目简介：" in content:
            content = content.replace("### 项目简介：", f"{new_line}### 项目简介：", 1)
        elif "项目简介" in content:
            content = content.replace("项目简介", f"{new_line}项目简介", 1)
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ README 更新完成 (已自动清理旧格式时间)")
    else:
        print("⚠️ 未找到 README.md")

if __name__ == "__main__":
    run()
