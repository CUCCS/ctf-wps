import zipfile
import os


def remove_fake_encryption(zip_file_path):
    """
    去除ZIP文件的伪加密设置，使其变为不加密状态
    :param zip_file_path: 要处理的ZIP文件路径
    """
    temp_file_path = zip_file_path + '.temp'
    with zipfile.ZipFile(zip_file_path, 'r') as existing_zip:
        with zipfile.ZipFile(temp_file_path, 'w') as new_zip:
            for item in existing_zip.infolist():
                # 将加密标志位清除，模拟去除加密设置
                item.flag_bits &= ~0x1
                new_zip.writestr(item, existing_zip.read(item.filename))

    print(f"已成功将 {zip_file_path} 的伪加密设置去除，变为不加密状态。")


if __name__ == "__main__":
    zip_file_path = input("请输入伪加密的ZIP文件的路径: ")
    remove_fake_encryption(zip_file_path)
