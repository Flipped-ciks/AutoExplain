import os

# 支持的代码文件类型
code_extensions = {'.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.rb', '.go'}

def count_lines_in_file(file_path):
    """统计单个文件的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except (UnicodeDecodeError, IOError):
        # 跳过不能读取的文件
        return 0

def count_lines_in_directory(directory, exclude_file):
    """递归统计目录中的代码行数"""
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in code_extensions:
                file_path = os.path.join(root, file)
                # 排除自身
                if os.path.abspath(file_path) != os.path.abspath(exclude_file):
                    total_lines += count_lines_in_file(file_path)
    return total_lines

if __name__ == "__main__":
    current_directory = "xkwautosolve"
    this_file = __file__  # 当前脚本文件
    total_lines = count_lines_in_directory(current_directory, "xkwautosolve\count.py")
    print(f"当前目录 '{current_directory}' 下共有代码行数（不含此脚本）: {total_lines}")
