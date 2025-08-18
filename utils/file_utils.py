# utils/file_utils.py
import os


def check_file_exists(file_path):
    """
    检查文件是否存在

    Args:
        file_path (str): 文件路径

    Returns:
        bool: 文件是否存在
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)


def get_file_extension(file_path):
    """
    获取文件扩展名

    Args:
        file_path (str): 文件路径

    Returns:
        str: 文件扩展名
    """
    return os.path.splitext(file_path)[1].lower()


# utils/file_utils.py

import os


def generate_directory_tree(startpath, indent="", ignore_patterns=None):
    """
    递归生成并返回指定目录的文件夹结构树（字符串形式），可过滤指定文件/文件夹

    参数:
        startpath (str): 起始目录路径
        indent (str): 当前层级的缩进字符
        ignore_patterns (set): 需要忽略的文件/文件夹名称集合

    返回:
        str: 树状结构字符串
    """
    # 默认忽略的文件和文件夹
    if ignore_patterns is None:
        ignore_patterns = {
            '.git', '__pycache__', '.idea', '.vscode', '.pytest_cache',
            '.DS_Store', 'venv', 'env', '.venv', 'node_modules',
            '*.pyc', '*.pyo', '*.pyd', '__pycache__', '.gitignore',
            'Thumbs.db', '.vs', '.vscode-test'
        }

    tree_str = ""
    if not os.path.exists(startpath):
        return "路径不存在"

    try:
        # 获取当前目录下的所有项目，并过滤掉忽略的内容
        items = sorted([
            item for item in os.listdir(startpath)
            if not any(pattern == item or item.endswith(pattern.lstrip('*'))
                       for pattern in ignore_patterns)
        ])
    except PermissionError:
        return indent + "❌ 权限不足\n"

    for i, item in enumerate(items):
        path = os.path.join(startpath, item)
        is_last = (i == len(items) - 1)
        tree_str += indent + ("└── " + item if is_last else "├── " + item) + "\n"
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            tree_str += generate_directory_tree(path, indent + extension, ignore_patterns)
    return tree_str


def print_directory_tree(startpath, indent="", ignore_patterns=None):
    """
    直接打印目录树结构

    参数:
        startpath (str): 起始目录路径
        indent (str): 当前层级的缩进字符
        ignore_patterns (set): 需要忽略的文件/文件夹名称集合
    """
    print(generate_directory_tree(startpath, indent, ignore_patterns))
