# test_pyqt5.py
import os
# 设置Qt插件路径 - 解决Windows平台插件加载问题
qt_plugins_path = r'C:\Users\17981\Desktop\科研\optic_code\new_denoise\.venv\Lib\site-packages\PyQt5\Qt5\plugins'
if os.path.exists(qt_plugins_path):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugins_path


# 原有代码继续...

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5测试窗口")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        # 添加标签
        self.label = QLabel("PyQt5 运行正常！")
        self.label.setAlignment(Qt.AlignCenter)

        # 添加按钮
        self.button = QPushButton("点击我")
        self.button.clicked.connect(self.on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText("按钮被点击了！")


def main():
    try:
        app = QApplication(sys.argv)
        window = TestWindow()
        window.show()
        print("PyQt5窗口已显示")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"PyQt5运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
