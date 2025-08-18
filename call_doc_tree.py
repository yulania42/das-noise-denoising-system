from utils.file_utils import generate_directory_tree, print_directory_tree
if __name__ == '__main__':
    project_root = "."  # 当前工作目录（即项目根目录）
    print("📁 当前项目结构如下：")
    print_directory_tree(project_root)
