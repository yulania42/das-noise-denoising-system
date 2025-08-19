from utils.file_utils import generate_directory_tree, print_directory_tree
if __name__ == '__main__':
    project_root1 = r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5"
    project_root2 = r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5-5.15.11.dist-info"
    project_root3 = r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5_Qt5-5.15.2.dist-info"
    project_root4 = r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5_sip-12.17.0.dist-info"
    project_root5 = r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5"
    # 当前工作目录（即项目根目录）
    print("📁 当前项目结构如下：")
    print_directory_tree(project_root1)
    # print_directory_tree(project_root2)
    # print_directory_tree(project_root3)
    # print_directory_tree(project_root4)
    # print_directory_tree(project_root5)
