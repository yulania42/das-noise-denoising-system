# 文件位置：gui/step4_image_display.py

import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QGroupBox, QLabel, QPushButton, QScrollArea, QTextEdit)
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ImageDisplayWidget(QWidget):
    """
    详细规范:
    组件: Step4 - 图像显示与控制界面
    功能: 显示原始图像、添加噪声后图像、降噪后图像，以及参数和指标信息
    主要职责:
    1. 显示三幅图像（原始、噪声、降噪）
    2. 显示噪声参数和降噪参数
    3. 显示PSNR、SSIM和相对误差指标
    4. 提供保存结果功能
    界面元素:
    - 图像显示区域 (matplotlib figure)
    - 控制面板 (保存按钮等)
    - 参数显示区域 (QTextEdit)
    - 指标显示区域 (QTextEdit)
    信号定义:
    - save_requested: 当用户点击保存按钮时发出
    数据结构:
    update_display方法接收的参数格式:
    - data_dict: {
        "original": numpy数组,
        "noisy": numpy数组,
        "denoised": numpy数组
      }
    - params: {
        "noise_params": dict,
        "denoise_params": dict
      }
    - metrics: {
        "psnr": float,
        "ssim": float,
        "relative_error": float
      }
    依赖关系:
    - PyQt5.QtWidgets, PyQt5.QtCore
    - matplotlib.backends.backend_qt5agg, matplotlib.figure
    - numpy
    """
    # 定义信号
    save_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        # 创建标题
        title = QLabel("结果展示与分析")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        main_layout.addWidget(title)
        # 创建主显示区域
        display_layout = QHBoxLayout()
        # 图像显示区域
        self.setup_image_display_area()
        display_layout.addWidget(self.image_group, 70)  # 占70%宽度
        # 右侧信息区域
        info_layout = QVBoxLayout()
        # 参数显示区域
        self.setup_parameter_display()
        info_layout.addWidget(self.param_group, 40)  # 占40%高度
        # 指标显示区域
        self.setup_metrics_display()
        info_layout.addWidget(self.metrics_group, 30)  # 占30%高度
        # 控制面板
        self.setup_control_panel()
        info_layout.addWidget(self.control_group, 30)  # 占30%高度
        display_layout.addLayout(info_layout, 30)  # 占30%宽度
        main_layout.addLayout(display_layout)

    def setup_image_display_area(self):
        """设置图像显示区域"""
        self.image_group = QGroupBox("图像对比")
        image_layout = QVBoxLayout()
        # 创建matplotlib图形
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        # 创建三个子图
        self.ax_original = self.figure.add_subplot(131)
        self.ax_noisy = self.figure.add_subplot(132)
        self.ax_denoised = self.figure.add_subplot(133)
        # 设置初始状态
        self.ax_original.set_title("原始图像")
        self.ax_noisy.set_title("添加噪声后")
        self.ax_denoised.set_title("降噪后")
        image_layout.addWidget(self.canvas)
        self.image_group.setLayout(image_layout)

    def setup_control_panel(self):
        """设置控制面板区域"""
        self.control_group = QGroupBox("控制面板")
        control_layout = QHBoxLayout()
        self.btn_save = QPushButton("保存结果")
        self.btn_save.clicked.connect(self.save_requested)
        control_layout.addWidget(self.btn_save)
        control_layout.addStretch()
        self.control_group.setLayout(control_layout)

    def setup_parameter_display(self):
        """设置参数显示区域"""
        self.param_group = QGroupBox("参数信息")
        param_layout = QVBoxLayout()
        self.param_display = QTextEdit()
        self.param_display.setReadOnly(True)
        param_layout.addWidget(self.param_display)
        self.param_group.setLayout(param_layout)

    def setup_metrics_display(self):
        """设置指标显示区域"""
        self.metrics_group = QGroupBox("评估指标")
        metrics_layout = QVBoxLayout()
        self.metrics_display = QTextEdit()
        self.metrics_display.setReadOnly(True)
        metrics_layout.addWidget(self.metrics_display)
        self.metrics_group.setLayout(metrics_layout)

    def update_display(self, data_dict, params, metrics):
        """更新所有显示内容"""
        # 更新图像显示
        self.update_images(
            data_dict.get("original"),
            data_dict.get("noisy"),
            data_dict.get("denoised")
        )
        # 更新参数显示
        self.update_parameters(params)
        # 更新指标显示
        self.update_metrics(metrics)

    def update_images(self, original, noisy, denoised):
        """更新三幅图像显示"""
        # 清除之前的图像
        self.ax_original.clear()
        self.ax_noisy.clear()
        self.ax_denoised.clear()
        # 清除可能存在的colorbar
        for ax in [self.ax_original, self.ax_noisy, self.ax_denoised]:
            # 移除旧的colorbar
            for child in ax.get_children():
                if hasattr(child, 'colorbar') and child.colorbar:
                    child.colorbar.remove()
        # 显示图像
        if original is not None:
            im1 = self.ax_original.imshow(original, cmap='viridis', aspect='auto')
            self.ax_original.set_title("原始图像")
            self.figure.colorbar(im1, ax=self.ax_original, shrink=0.8)
        if noisy is not None:
            im2 = self.ax_noisy.imshow(noisy, cmap='viridis', aspect='auto')
            self.ax_noisy.set_title("添加噪声后")
            self.figure.colorbar(im2, ax=self.ax_noisy, shrink=0.8)
        if denoised is not None:
            im3 = self.ax_denoised.imshow(denoised, cmap='viridis', aspect='auto')
            self.ax_denoised.set_title("降噪后")
            self.figure.colorbar(im3, ax=self.ax_denoised, shrink=0.8)
        # 调整子图间距
        self.figure.subplots_adjust(wspace=0.3)

        # 刷新画布
        self.canvas.draw()

    def update_parameters(self, params):
        """更新参数显示"""
        if not params:
            self.param_display.setPlainText("暂无参数信息")
            return
        param_text = "=== 噪声参数 ===\n"
        # 高斯噪声参数
        gaussian_params = params.get("noise_params", {}).get("gaussian", {})
        if gaussian_params.get("enabled", False):
            param_text += f"高斯噪声 - 信噪比: {gaussian_params.get('snr_db', 'N/A')} dB\n"
        else:
            param_text += "高斯噪声: 未启用\n"
        # 脉冲噪声参数
        impulse_params = params.get("noise_params", {}).get("impulse", {})
        if impulse_params.get("enabled", False):
            param_text += f"脉冲噪声 - 噪声比例: {impulse_params.get('noise_ratio', 'N/A')}, "
            param_text += f"盐噪声比例: {impulse_params.get('salt_ratio', 'N/A')}\n"
        else:
            param_text += "脉冲噪声: 未启用\n"
        param_text += "\n=== 降噪参数 ===\n"
        # 降噪参数
        denoise_params = params.get("denoise_params", {})
        method = denoise_params.get("method", "N/A")
        parameters = denoise_params.get("parameters", {})
        method_names = {
            "gaussian_filter": "高斯滤波",
            "moving_average_filter": "移动平均滤波",
            "median_filter": "中值滤波",
            "wavelet_denoising": "小波降噪",
            "bilateral_filter": "双边滤波"
        }
        param_text += f"方法: {method_names.get(method, method)}\n"
        if method == "gaussian_filter":
            param_text += f"Sigma: {parameters.get('sigma', 'N/A')}\n"
        elif method == "moving_average_filter":
            param_text += f"窗口大小: {parameters.get('window_size', 'N/A')}\n"
        elif method == "median_filter":
            param_text += f"滤波器大小: {parameters.get('size', 'N/A')}\n"
        elif method == "wavelet_denoising":
            param_text += f"小波基函数: {parameters.get('wavelet', 'N/A')}, "
            param_text += f"分解层数: {parameters.get('level', 'N/A')}, "
            param_text += f"阈值模式: {parameters.get('threshold_mode', 'N/A')}\n"
        elif method == "bilateral_filter":
            param_text += f"空间Sigma: {parameters.get('spatial_sigma', 'N/A')}, "
            param_text += f"强度Sigma: {parameters.get('intensity_sigma', 'N/A')}, "
            param_text += f"窗口大小: {parameters.get('window_size', 'N/A')}\n"
        self.param_display.setPlainText(param_text)

    def update_metrics(self, metrics):
        """更新指标显示"""
        if not metrics:
            self.metrics_display.setPlainText("暂无评估指标")
            return
        metrics_text = "=== 图像质量评估指标 ===\n"
        metrics_text += f"PSNR: {metrics.get('psnr', 'N/A'):.2f} dB\n"
        metrics_text += f"SSIM: {metrics.get('ssim', 'N/A'):.4f}\n"
        metrics_text += f"相对误差: {metrics.get('relative_error', 'N/A'):.6f}\n"
        self.metrics_display.setPlainText(metrics_text)

    def save_results(self):
        """保存结果图像和数据"""
        self.save_requested.emit()


# 测试代码 - 可以删除
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageDisplayWidget()
    window.show()
    # 模拟数据更新
    test_data = {
        "original": np.random.rand(100, 100),
        "noisy": np.random.rand(100, 100),
        "denoised": np.random.rand(100, 100)
    }
    test_params = {
        "noise_params": {
            "gaussian": {"enabled": True, "snr_db": 20.0},
            "impulse": {"enabled": False, "noise_ratio": 0.05, "salt_ratio": 0.5}
        },
        "denoise_params": {
            "method": "wavelet_denoising",
            "parameters": {
                "wavelet": "db4",
                "level": 3,
                "threshold_mode": "soft"
            }
        }
    }
    test_metrics = {
        "psnr": 25.67,
        "ssim": 0.8234,
        "relative_error": 0.001245
    }
    window.update_display(test_data, test_params, test_metrics)
    sys.exit(app.exec_())
