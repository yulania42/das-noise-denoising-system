# 文件位置：gui/step3_denoising_method.py


import config
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QGroupBox, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,
                             QStackedWidget, QCheckBox)
from PyQt5.QtCore import pyqtSignal


class DenoisingMethodWidget(QWidget):
    """
    详细规范:
    组件: Step3 - 降噪方式选择界面
    功能: 选择降噪方法并配置相应的参数
    主要职责:
    1. 提供降噪方法选择下拉框
    2. 根据选择的降噪方法显示相应的参数设置控件
    3. 验证参数输入的有效性
    4. 通过信号通知降噪方法变化

    支持的降噪方法:
    - 高斯滤波 (gaussian_filter)
    - 移动平均滤波 (moving_average_filter)
    - 中值滤波 (median_filter)
    - 小波降噪 (wavelet_denoising)
    - 双边滤波 (bilateral_filter)

    信号定义:
    - method_changed: 当降噪方法发生变化时发出，参数为方法名称

    界面元素:
    - 降噪方法选择下拉框 (combo_method)
    - 参数设置区域堆叠控件 (stacked_parameters)
    - 各降噪方法对应的参数控件

    数据结构:
    返回参数字典格式:
    {
        "method": str,  # 降噪方法名称
        "parameters": dict  # 该方法对应的参数
    }

    各方法参数格式:
    - gaussian_filter: {"sigma": float}
    - moving_average_filter: {"window_size": int}
    - median_filter: {"size": int}
    - wavelet_denoising: {"wavelet": str, "level": int, "threshold_mode": str}
    - bilateral_filter: {"spatial_sigma": float, "intensity_sigma": float, "window_size": int}

    依赖关系:
    - PyQt5.QtWidgets, PyQt5.QtCore
    """

    # 定义信号
    method_changed = pyqtSignal(str)  # 当方法变化时触发
    parameters_changed = pyqtSignal()  # 当参数配置有效且发生改变时触发

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 创建标题
        title = QLabel("降噪方法选择")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        # 降噪方法选择区域
        self.setup_denoising_methods()
        layout.addWidget(self.method_group)

        # 参数设置区域
        self.setup_parameter_widgets()
        layout.addWidget(self.stacked_parameters)

        layout.addStretch()

    def setup_denoising_methods(self):
        """设置降噪方法选择区域"""
        self.method_group = QGroupBox("选择降噪方法")
        method_layout = QHBoxLayout()

        self.lbl_method = QLabel("降噪方法:")
        self.combo_method = QComboBox()
        # 添加支持的降噪方法
        self.combo_method.addItem("高斯滤波", "gaussian_filter")
        self.combo_method.addItem("移动平均滤波", "moving_average_filter")
        self.combo_method.addItem("中值滤波", "median_filter")
        self.combo_method.addItem("小波降噪", "wavelet_denoising")
        self.combo_method.addItem("双边滤波", "bilateral_filter")

        self.combo_method.currentIndexChanged.connect(self.on_method_changed)

        method_layout.addWidget(self.lbl_method)
        method_layout.addWidget(self.combo_method)
        method_layout.addStretch()

        self.method_group.setLayout(method_layout)

    def setup_parameter_widgets(self):
        """设置各降噪方法的参数控件"""
        self.stacked_parameters = QStackedWidget()

        # 高斯滤波参数
        self.setup_gaussian_filter_params()
        self.stacked_parameters.addWidget(self.gaussian_params_widget)

        # 移动平均滤波参数
        self.setup_moving_average_filter_params()
        self.stacked_parameters.addWidget(self.moving_avg_params_widget)

        # 中值滤波参数
        self.setup_median_filter_params()
        self.stacked_parameters.addWidget(self.median_params_widget)

        # 小波降噪参数
        self.setup_wavelet_denoising_params()
        self.stacked_parameters.addWidget(self.wavelet_params_widget)

        # 双边滤波参数
        self.setup_bilateral_filter_params()
        self.stacked_parameters.addWidget(self.bilateral_params_widget)

        # 默认显示第一个方法的参数
        self.stacked_parameters.setCurrentIndex(0)

    def setup_gaussian_filter_params(self):
        """设置高斯滤波参数控件"""
        self.gaussian_params_widget = QWidget()
        layout = QFormLayout(self.gaussian_params_widget)

        self.spin_gaussian_sigma = QDoubleSpinBox()
        self.spin_gaussian_sigma.setRange(0.1, 10.0)
        self.spin_gaussian_sigma.setValue(1.0)
        self.spin_gaussian_sigma.setSingleStep(0.1)
        layout.addRow("Sigma值:", self.spin_gaussian_sigma)

    def setup_moving_average_filter_params(self):
        """设置移动平均滤波参数控件"""
        self.moving_avg_params_widget = QWidget()
        layout = QFormLayout(self.moving_avg_params_widget)

        self.spin_moving_avg_window = QSpinBox()
        self.spin_moving_avg_window.setRange(1, 100)
        self.spin_moving_avg_window.setValue(5)
        self.spin_moving_avg_window.setSingleStep(1)
        layout.addRow("窗口大小:", self.spin_moving_avg_window)

    def setup_median_filter_params(self):
        """设置中值滤波参数控件"""
        self.median_params_widget = QWidget()
        layout = QFormLayout(self.median_params_widget)

        self.spin_median_size = QSpinBox()
        self.spin_median_size.setRange(1, 50)
        self.spin_median_size.setValue(3)
        self.spin_median_size.setSingleStep(1)
        layout.addRow("滤波器大小:", self.spin_median_size)

    def setup_wavelet_denoising_params(self):
        """设置小波降噪参数控件"""
        self.wavelet_params_widget = QWidget()
        layout = QFormLayout(self.wavelet_params_widget)

        self.combo_wavelet = QComboBox()
        self.combo_wavelet.addItems(["db4", "haar", "coif1", "sym4"])
        layout.addRow("小波基函数:", self.combo_wavelet)

        self.spin_wavelet_level = QSpinBox()
        self.spin_wavelet_level.setRange(1, 10)
        self.spin_wavelet_level.setValue(3)
        layout.addRow("分解层数:", self.spin_wavelet_level)

        self.combo_threshold_mode = QComboBox()
        self.combo_threshold_mode.addItems(["soft", "hard"])
        layout.addRow("阈值模式:", self.combo_threshold_mode)

    def setup_bilateral_filter_params(self):
        """设置双边滤波参数控件"""
        self.bilateral_params_widget = QWidget()
        layout = QFormLayout(self.bilateral_params_widget)

        self.spin_bilateral_spatial = QDoubleSpinBox()
        self.spin_bilateral_spatial.setRange(0.1, 100.0)
        self.spin_bilateral_spatial.setValue(10.0)
        self.spin_bilateral_spatial.setSingleStep(1.0)
        layout.addRow("空间Sigma:", self.spin_bilateral_spatial)

        self.spin_bilateral_intensity = QDoubleSpinBox()
        self.spin_bilateral_intensity.setRange(0.1, 100.0)
        self.spin_bilateral_intensity.setValue(20.0)
        self.spin_bilateral_intensity.setSingleStep(1.0)
        layout.addRow("强度Sigma:", self.spin_bilateral_intensity)

        self.spin_bilateral_window = QSpinBox()
        self.spin_bilateral_window.setRange(1, 50)
        self.spin_bilateral_window.setValue(10)
        layout.addRow("窗口大小:", self.spin_bilateral_window)

    def on_method_changed(self, index):
        """处理降噪方法改变事件"""
        self.stacked_parameters.setCurrentIndex(index)
        method = self.combo_method.currentData()
        self.method_changed.emit(method)
        self.parameters_changed.emit()  # 新增这一行

    def get_denoising_parameters(self):
        """获取当前选择的降噪参数配置"""
        method = self.combo_method.currentData()
        parameters = {}

        if method == "gaussian_filter":
            parameters = {
                "sigma": self.spin_gaussian_sigma.value()
            }
        elif method == "moving_average_filter":
            parameters = {
                "window_size": self.spin_moving_avg_window.value()
            }
        elif method == "median_filter":
            parameters = {
                "size": self.spin_median_size.value()
            }
        elif method == "wavelet_denoising":
            parameters = {
                "wavelet": self.combo_wavelet.currentText(),
                "level": self.spin_wavelet_level.value(),
                "threshold_mode": self.combo_threshold_mode.currentText()
            }
        elif method == "bilateral_filter":
            parameters = {
                "spatial_sigma": self.spin_bilateral_spatial.value(),
                "intensity_sigma": self.spin_bilateral_intensity.value(),
                "window_size": self.spin_bilateral_window.value()
            }

        return {
            "method": method,
            "parameters": parameters
        }

    def validate_parameters(self):
        """验证参数输入是否有效"""
        method = self.combo_method.currentData()

        if method == "gaussian_filter":
            if self.spin_gaussian_sigma.value() <= 0:
                return False, "高斯滤波Sigma值必须大于0"
        elif method == "moving_average_filter":
            if self.spin_moving_avg_window.value() < 1:
                return False, "移动平均窗口大小必须大于等于1"
        elif method == "median_filter":
            if self.spin_median_size.value() < 1:
                return False, "中值滤波器大小必须大于等于1"
        elif method == "wavelet_denoising":
            if self.spin_wavelet_level.value() < 1:
                return False, "小波分解层数必须大于等于1"
        elif method == "bilateral_filter":
            if self.spin_bilateral_spatial.value() <= 0:
                return False, "双边滤波空间Sigma值必须大于0"
            if self.spin_bilateral_intensity.value() <= 0:
                return False, "双边滤波强度Sigma值必须大于0"
            if self.spin_bilateral_window.value() < 1:
                return False, "双边滤波窗口大小必须大于等于1"

        return True, "参数验证通过"


