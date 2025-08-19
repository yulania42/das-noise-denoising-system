# config.py - 添加到项目根目录
import os


def setup_qt_environment():
    """设置Qt环境变量"""
    # Qt插件路径
    qt_plugins_path = r'C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5\Qt5\plugins'
    if os.path.exists(qt_plugins_path):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugins_path

    # Qt根路径
    qt_path = r'C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5\Qt5'
    if os.path.exists(qt_path):
        os.environ['QTDIR'] = qt_path


# 程序启动时自动设置
setup_qt_environment()
