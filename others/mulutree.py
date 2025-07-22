import os

def print_tree(root_path, prefix=""):
    entries = sorted(os.listdir(root_path))
    entries_count = len(entries)

    for idx, entry in enumerate(entries):
        path = os.path.join(root_path, entry)
        connector = "├── " if idx < entries_count - 1 else "└── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "│   " if idx < entries_count - 1 else "    "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    root = os.getcwd()  # 当前目录
    print(f"Directory tree of: {root}")
    print_tree(root)
