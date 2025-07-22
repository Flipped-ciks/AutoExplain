import os
import re

def merge_python_files(output_file="all.py"):
    # 获取当前目录下所有.py文件
    python_files = [f for f in os.listdir('.') if f.endswith('.py') and f != output_file]
    
    # 按文件名排序
    python_files.sort()
    
    # 存储已导入的模块，避免重复导入
    imported_modules = set()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 添加文件头部注释
        outfile.write(f"# 合并文件: {', '.join(python_files)}\n\n")
        
        for filename in python_files:
            # 添加分隔注释
            outfile.write(f"# ==== 开始: {filename} ====\n\n")
            
            with open(filename, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # 处理导入语句，避免重复导入
                    import_match = re.match(r'^\s*(import|from)\s+([\w\.]+)', line)
                    if import_match:
                        module = import_match.group(0).strip()
                        if module not in imported_modules:
                            imported_modules.add(module)
                            outfile.write(line)
                    # 跳过if __name__ == "__main__"部分
                    elif '__name__ == "__main__"' in line:
                        continue
                    else:
                        outfile.write(line)
            
            # 添加文件结束注释
            outfile.write(f"\n# ==== 结束: {filename} ====\n\n")
    
    print(f"已合并 {len(python_files)} 个Python文件到 {output_file}")

if __name__ == "__main__":
    merge_python_files()
    