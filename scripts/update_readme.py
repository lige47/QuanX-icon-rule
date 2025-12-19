import os
import re
from datetime import datetime, timedelta

# 配置图标根目录
ROOT_DIR = "icon"

def run():
    # 1. 直接扫描硬盘统计真实数量
    count = 0
    if os.path.exists(ROOT_DIR):
        for root, dirs, files in os.walk(ROOT_DIR):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico')):
                    count += 1
    
    print(f"📊 统计到图标总数: {count}")

    # 2. 获取北京时间
    time_str = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

    # 3. 更新 README.md
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 删除旧的时间行
        content = re.sub(r"🕒 本项目最近更新于：.*?\n?", "", content)
        
        # 插入新时间行
        new_line = f"\n\n🕒 本项目最近更新于：{time_str} (共计 {count} 个图标)\n\n"
        
        # 在"项目简介"前插入
        if "### 项目简介：" in content:
            content = content.replace("### 项目简介：", f"{new_line}### 项目简介：", 1)
        elif "项目简介" in content:
            content = content.replace("项目简介", f"{new_line}项目简介", 1)
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ README 更新完成")
    else:
        print("⚠️ 未找到 README.md")

if __name__ == "__main__":
    run()
