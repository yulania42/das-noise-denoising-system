# config2.py
import os
import sys


def setup_qt_environment():
    """设置Qt环境变量"""
    # 获取当前脚本的绝对路径所在目录（项目根目录）
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"[DEBUG] 项目根目录: {project_root}")

    # 拼接实际的虚拟环境目录路径
    venv_dir = os.path.join(project_root, ".venv")

    # 构建完整的平台插件路径
    platforms_path = os.path.join(
        venv_dir,
        "Lib",
        "site-packages",
        "PyQt5",
        "Qt5",
        "plugins",
        "platforms"
    )

    # 构建 bin 目录路径
    bin_path = os.path.join(venv_dir, "Lib", "site-packages", "PyQt5", "Qt5", "bin")

    # 确保路径存在
    if not os.path.exists(platforms_path):
        # 尝试备用拼法
        alternate_path = platforms_path.replace("Lib\\site-packages", "Lib\\site-packages")
        if not os.path.exists(alternate_path):
            msg = (f"❌ 无法找到 Qt platforms 路径。请检查:\n"
                   f"当前计算路径: {platforms_path}\n"
                   f"备用计算路径: {alternate_path}\n"
                   f"实际路径: {os.path.join(venv_dir, 'Lib', 'site-packages', ...)}\n"
                   f"__file__ = {os.path.abspath(__file__)}")
            raise RuntimeError(msg)
        platforms_path = alternate_path

    print(f"[DEBUG] Qt platform plugin path: {platforms_path}")

    # 设置环境变量
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = platforms_path
    print(f"[SUCCESS] 设置 QT_QPA_PLATFORM_PLUGIN_PATH = {platforms_path}")

    # 确保 DLL 路径
    if os.path.exists(bin_path):
        os.environ['PATH'] = f"{bin_path};{os.environ['PATH']}"
        print(f"[SUCCESS] 添加 PATH: {bin_path}")

    # 额外调试信息
    print(f"[INFO] PATH 环境变量:\n{os.environ['PATH']}")
    print(f"[INFO] __file__ = {os.path.abspath(__file__)}")


# 程序启动时自动设置
setup_qt_environment()
