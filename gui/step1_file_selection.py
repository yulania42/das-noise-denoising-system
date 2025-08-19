# 文件位置：gui/step1_file_selection.py

import config
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QPushButton, QLabel, QComboBox, QFileDialog)
from PyQt5.QtCore import pyqtSignal
import numpy as np


class FileSelectionWidget(QWidget):
    # 定义信号，用于通知主窗口文件已选择
    file_selected = pyqtSignal(str, str)  # (file_path, variable_name)

    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.variable_name = "DAS_data"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 文件选择区域
        file_group = QGroupBox("选择.mat数据文件")
        file_layout = QVBoxLayout()

        # 文件选择按钮和路径显示
        file_select_layout = QHBoxLayout()
        self.btn_select_file = QPushButton("浏览文件")
        self.btn_select_file.clicked.connect(self.select_file)
        self.lbl_file_path = QLabel("未选择文件")
        self.lbl_file_path.setWordWrap(True)
        file_select_layout.addWidget(self.btn_select_file)
        file_select_layout.addWidget(self.lbl_file_path)

        # 变量名选择
        variable_layout = QHBoxLayout()
        self.lbl_variable = QLabel("数据变量名:")
        self.combo_variable = QComboBox()
        self.combo_variable.addItem("DAS_data")
        self.combo_variable.addItem("data")
        self.combo_variable.addItem("signal")
        self.combo_variable.setEnabled(False)  # 初始禁用，选择文件后启用
        variable_layout.addWidget(self.lbl_variable)
        variable_layout.addWidget(self.combo_variable)

        file_layout.addLayout(file_select_layout)
        file_layout.addLayout(variable_layout)
        file_group.setLayout(file_layout)

        # 文件信息显示区域
        self.file_info_group = QGroupBox("文件信息")
        self.file_info_layout = QVBoxLayout()
        self.lbl_file_info = QLabel("请先选择.mat文件")
        self.file_info_layout.addWidget(self.lbl_file_info)
        self.file_info_group.setLayout(self.file_info_layout)

        layout.addWidget(file_group)
        layout.addWidget(self.file_info_group)
        layout.addStretch()

    def select_file(self):
        """选择.mat文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择DAS数据文件",
            "",
            "MATLAB Files (*.mat);;All Files (*)"
        )

        if file_path:
            self.file_path = file_path
            self.lbl_file_path.setText(file_path)
            self.combo_variable.setEnabled(True)

            # 这里应该加载文件并分析内容
            self.load_file_info(file_path)

            # 发送信号通知主窗口
            variable_name = self.combo_variable.currentText()
            self.file_selected.emit(file_path, variable_name)

    def load_file_info(self, file_path):
        """加载并显示文件信息"""
        try:
            import scipy.io as sio
            mat_contents = sio.loadmat(file_path)

            # 清除旧的文件信息
            for i in reversed(range(self.file_info_layout.count())):
                self.file_info_layout.itemAt(i).widget().setParent(None)

            # 显示文件基本信息
            info_text = f"文件路径: {file_path}\n\n"
            info_text += "文件包含的变量:\n"

            variables = []
            for key in mat_contents.keys():
                if not key.startswith('__'):  # 排除matlab内部变量
                    variables.append(key)
                    var_data = mat_contents[key]
                    if isinstance(var_data, np.ndarray):
                        info_text += f"  {key}: {var_data.shape} ({var_data.dtype})\n"
                    else:
                        info_text += f"  {key}: {type(var_data)}\n"

            # 更新变量名下拉框
            self.combo_variable.clear()
            self.combo_variable.addItems(variables)
            if "DAS_data" in variables:
                self.combo_variable.setCurrentText("DAS_data")

            # 显示信息
            info_label = QLabel(info_text)
            info_label.setWordWrap(True)
            self.file_info_layout.addWidget(info_label)

        except Exception as e:
            self.lbl_file_info.setText(f"读取文件出错: {str(e)}")



