import os

# 配置目标目录
TARGET_DIR = "icon"

# 指定要删除的图片格式
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.ico')

def clean_root_images():
    print(f"⚠️ 准备清理 {TARGET_DIR} 根目录下的散乱图片...")
    
    if not os.path.exists(TARGET_DIR):
        print(f"❌ 错误: 找不到目录 {TARGET_DIR}")
        return

    deleted_count = 0

    # 获取 icon 目录下的所有内容
    for filename in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, filename)
        
        # 1. 关键检查：必须是文件 (os.path.isfile)，绝对不能是文件夹
        if os.path.isfile(file_path):
            # 2. 检查后缀名：必须是图片
            if filename.lower().endswith(IMAGE_EXTENSIONS):
                try:
                    os.remove(file_path)
                    print(f"   🗑️ 已删除: {filename}")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ❌ 删除失败 {filename}: {e}")
        
        #如果是文件夹 (os.path.isdir)，循环会自动跳过，什么都不做

    print(f"\n✅ 清理完成！共删除了 {deleted_count} 张根目录图片。")
    print(f"   (子文件夹内的图片未受影响)")

if __name__ == "__main__":
    clean_root_images()
