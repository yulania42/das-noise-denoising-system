# 文件位置：gui/step2_noise_params.py

import config
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QGroupBox, QLabel, QCheckBox, QDoubleSpinBox, QSpinBox,
                             QComboBox, QLineEdit)
from PyQt5.QtCore import pyqtSignal


class NoiseParametersWidget(QWidget):
    """
    详细规范:
    组件: Step2 - 噪声参数设计界面
    功能: 设计高斯噪声和脉冲噪声的参数配置
    主要职责:
    1. 提供高斯噪声参数设置（信噪比）
    2. 提供脉冲噪声参数设置（噪声比例、盐噪声比例）
    3. 验证参数输入的有效性
    4. 通过信号通知参数变化

    信号定义:
    - parameters_changed: 当参数发生变化时发出

    界面元素:
    - 高斯噪声使能复选框 (chk_enable_gaussian)
    - 高斯噪声信噪比设置 (spin_snr_db)
    - 脉冲噪声使能复选框 (chk_enable_impulse)
    - 脉冲噪声比例设置 (spin_noise_ratio)
    - 盐噪声比例设置 (spin_salt_ratio)

    数据结构:
    返回参数字典格式:
    {
        "gaussian": {
            "enabled": bool,
            "snr_db": float
        },
        "impulse": {
            "enabled": bool,
            "noise_ratio": float,
            "salt_ratio": float
        }
    }

    依赖关系:
    - PyQt5.QtWidgets, PyQt5.QtCore
    """

    # 定义信号，用于通知参数已更改
    parameters_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 创建标题
        title = QLabel("噪声参数设置")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        # 高斯噪声参数区域
        self.setup_gaussian_noise_section()
        layout.addWidget(self.gaussian_group)

        # 脉冲噪声参数区域
        self.setup_impulse_noise_section()
        layout.addWidget(self.impulse_group)

        layout.addStretch()

    def setup_gaussian_noise_section(self):
        """设置高斯噪声参数区域"""
        self.gaussian_group = QGroupBox("高斯噪声参数")
        gaussian_layout = QVBoxLayout()

        # 使能复选框
        self.chk_enable_gaussian = QCheckBox("添加高斯噪声")
        self.chk_enable_gaussian.setChecked(True)
        self.chk_enable_gaussian.stateChanged.connect(self.parameters_changed)

        # 信噪比设置
        snr_layout = QHBoxLayout()
        self.lbl_snr = QLabel("信噪比 (dB):")
        self.spin_snr_db = QDoubleSpinBox()
        self.spin_snr_db.setRange(0.1, 100.0)
        self.spin_snr_db.setValue(20.0)
        self.spin_snr_db.setSingleStep(1.0)
        self.spin_snr_db.valueChanged.connect(self.parameters_changed)

        snr_layout.addWidget(self.lbl_snr)
        snr_layout.addWidget(self.spin_snr_db)
        snr_layout.addStretch()

        gaussian_layout.addWidget(self.chk_enable_gaussian)
        gaussian_layout.addLayout(snr_layout)

        self.gaussian_group.setLayout(gaussian_layout)

    def setup_impulse_noise_section(self):
        """设置脉冲噪声参数区域"""
        self.impulse_group = QGroupBox("脉冲噪声参数")
        impulse_layout = QVBoxLayout()

        # 使能复选框
        self.chk_enable_impulse = QCheckBox("添加脉冲噪声")
        self.chk_enable_impulse.setChecked(False)
        self.chk_enable_impulse.stateChanged.connect(self.parameters_changed)

        # 参数设置布局
        params_layout = QFormLayout()

        # 噪声比例
        self.spin_noise_ratio = QDoubleSpinBox()
        self.spin_noise_ratio.setRange(0.0, 1.0)
        self.spin_noise_ratio.setValue(0.05)
        self.spin_noise_ratio.setSingleStep(0.01)
        self.spin_noise_ratio.valueChanged.connect(self.parameters_changed)
        params_layout.addRow("噪声比例:", self.spin_noise_ratio)

        # 盐噪声比例
        self.spin_salt_ratio = QDoubleSpinBox()
        self.spin_salt_ratio.setRange(0.0, 1.0)
        self.spin_salt_ratio.setValue(0.5)
        self.spin_salt_ratio.setSingleStep(0.1)
        self.spin_salt_ratio.valueChanged.connect(self.parameters_changed)
        params_layout.addRow("盐噪声比例:", self.spin_salt_ratio)

        impulse_layout.addWidget(self.chk_enable_impulse)
        impulse_layout.addLayout(params_layout)

        self.impulse_group.setLayout(impulse_layout)

    def get_noise_parameters(self):
        """获取噪声参数配置"""
        return {
            "gaussian": {
                "enabled": self.chk_enable_gaussian.isChecked(),
                "snr_db": self.spin_snr_db.value()
            },
            "impulse": {
                "enabled": self.chk_enable_impulse.isChecked(),
                "noise_ratio": self.spin_noise_ratio.value(),
                "salt_ratio": self.spin_salt_ratio.value()
            }
        }

    def validate_parameters(self):
        """验证参数输入是否有效"""
        # 检查至少启用一种噪声
        if not self.chk_enable_gaussian.isChecked() and not self.chk_enable_impulse.isChecked():
            return False, "请至少启用一种噪声类型"

        # 检查高斯噪声参数
        if self.chk_enable_gaussian.isChecked():
            if self.spin_snr_db.value() <= 0:
                return False, "高斯噪声信噪比必须大于0"

        # 检查脉冲噪声参数
        if self.chk_enable_impulse.isChecked():
            if self.spin_noise_ratio.value() <= 0:
                return False, "脉冲噪声比例必须大于0"
            if not (0 <= self.spin_salt_ratio.value() <= 1):
                return False, "盐噪声比例必须在0-1之间"

        return True, "参数验证通过"
