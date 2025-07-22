import os

def list_files_in_directory(directory):
    # 获取指定目录下的所有文件和文件夹
    files = os.listdir(directory)
    
    # 过滤出文件（排除文件夹）
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    
    return files

def save_filenames_to_file(filenames, output_file):
    # 将文件名写入到指定的输出文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        for filename in filenames:
            f.write(filename + '\n')

if __name__ == "__main__":
    # 指定目标路径
    target_directory = r'D:\\Code\\xkwautosolve'  # 使用原始字符串（raw string）避免转义问题
    
    # 检查路径是否存在
    if not os.path.exists(target_directory):
        print(f"路径 {target_directory} 不存在！")
        exit()
    
    # 列出目标文件夹中的所有文件
    files = list_files_in_directory(target_directory)
    
    # 输出文件名到文件
    output_file = os.path.join(target_directory, 'file_list.txt')  # 输出文件保存到目标路径
    save_filenames_to_file(files, output_file)
    
    print(f"文件名已保存到 {output_file}")