import os

# 获取当前目录下的所有文件
current_directory = os.getcwd()
for filename in os.listdir(current_directory):
    # 判断文件是否为图片（可以根据扩展名进行判断）
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
        # 删除文件名中的 [ 和 ]，同时将空格替换为 _
        new_filename = filename.replace('[', '').replace(']', '').replace(' ', '_')
        
        # 如果文件名有变化，重命名文件
        if new_filename != filename:
            old_file_path = os.path.join(current_directory, filename)
            new_file_path = os.path.join(current_directory, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {filename} -> {new_filename}')
