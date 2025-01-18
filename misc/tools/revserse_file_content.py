def reverse_binary_file():
    input_file_path = input("请输入要读取的二进制文件路径: ")
    try:
        with open(input_file_path, 'rb') as input_file:
            # 读取整个二进制文件内容到字节数组
            content = input_file.read()
            reversed_content = content[::-1]
            with open('flag.data', 'wb') as output_file:
                output_file.write(reversed_content)
        print("已成功将逆序后的内容写入到flag.data文件中。")
    except FileNotFoundError:
        print("输入的文件不存在，请检查文件路径是否正确。")


if __name__ == "__main__":
    reverse_binary_file()
