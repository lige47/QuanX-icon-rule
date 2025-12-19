import os
import json
import re
from datetime import datetime, timedelta

MAIN_JSON_FILE = "QuanX-icon-rule.json"

def update_readme():
    print("📝 正在更新 README...")
    
    # 1. 读取 JSON 获取准确数量
    total_count = 0
    if os.path.exists(MAIN_JSON_FILE):
        with open(MAIN_JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_count = len(data)
    
    # 2. 获取时间
    now_beijing = datetime.utcnow() + timedelta(hours=8)
    time_std = now_beijing.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 修改 README
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        
        # 清理旧的时间行
        readme = re.sub(r"🕒 本项目最近更新于：.*?\n?", "", readme)
        
        # 构造新行
        new_time_line = f"\n\n🕒 本项目最近更新于：{time_std} (共计 {total_count} 个图标)\n\n"
        
        # 插入内容
        if "### 项目简介：" in readme:
            readme = readme.replace("### 项目简介：", f"{new_time_line}### 项目简介：", 1)
        elif "项目简介" in readme:
            readme = readme.replace("项目简介", f"{new_time_line}项目简介", 1)
            
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
        print(f"✅ README 更新成功: {time_std}, count={total_count}")
    else:
        print("⚠️ 未找到 README.md，跳过更新。")

if __name__ == "__main__":
    update_readme()
