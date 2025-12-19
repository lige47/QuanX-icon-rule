import os
import re
from datetime import datetime, timedelta

def run():
    # 1. 统计真实数量 (递归扫描 icon 目录下所有图片)
    count = 0
    for root, dirs, files in os.walk("icon"):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico')):
                count += 1
    
    print(f"统计到图标总数: {count}")

    # 2. 获取时间
    time_str = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

    # 3. 更新 README
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 删除旧时间行
        content = re.sub(r"🕒 本项目最近更新于：.*?\n?", "", content)
        
        # 插入新时间行
        new_line = f"\n\n🕒 本项目最近更新于：{time_str} (共计 {count} 个图标)\n\n"
        
        if "### 项目简介：" in content:
            content = content.replace("### 项目简介：", f"{new_line}### 项目简介：", 1)
        elif "项目简介" in content:
            content = content.replace("项目简介", f"{new_line}项目简介", 1)
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    run()
