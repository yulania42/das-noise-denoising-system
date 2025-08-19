# main.py
import os
import sys
import config2
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot

from gui.step1_file_selection import FileSelectionWidget
from gui.step2_noise_params import NoiseParametersWidget
from gui.step3_denoising_method import DenoisingMethodWidget
from gui.step4_image_display import ImageDisplayWidget

from data_loader.data_loader_factory import DataLoaderFactory
from noise_generator.noise_factory import NoiseGeneratorFactory
from denoising.denoising_factory import DenoisingFactory
from metrics.metrics_factory import MetricsFactory
from visualization.visualization_factory import VisualizationFactory



class MainController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DAS 数据加噪与降噪一体化处理系统")
        self.setGeometry(100, 100, 1200, 800)

        # 当前步骤标志
        self.current_step = 0

        # 初始化各个步骤组件
        self.step1_widget = FileSelectionWidget()
        self.step2_widget = NoiseParametersWidget()
        self.step3_widget = DenoisingMethodWidget()
        self.step4_widget = ImageDisplayWidget()

        # 初始化堆叠窗口组件
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.step1_widget)
        self.stacked_widget.addWidget(self.step2_widget)
        self.stacked_widget.addWidget(self.step3_widget)
        self.stacked_widget.addWidget(self.step4_widget)

        # 设置主窗口中央组件为堆叠窗口
        self.setCentralWidget(self.stacked_widget)

        # 连接步骤间的信号和槽
        self.step1_widget.file_selected.connect(self.on_file_selected)
        self.step2_widget.parameters_changed.connect(self.on_noise_params_set)
        self.step3_widget.parameters_changed.connect(self.on_denoiser_set)
        self.step4_widget.save_requested.connect(self.save_results)

        # 用于暂存数据流
        self.file_path = None
        self.variable_name = None
        self.original_data = None
        self.noisy_data = None
        self.denoised_data = None
        self.metadata = {}

    @pyqtSlot(str, str)
    def on_file_selected(self, file_path, variable_name):
        self.file_path = file_path
        self.variable_name = variable_name

        # 加载 mat 文件
        loader = DataLoaderFactory.create_loader("matlab", file_path=file_path, variable_name=variable_name)
        self.original_data, self.metadata = loader.load_data()

        # 切换到步骤2
        self.current_step = 1
        self.stacked_widget.setCurrentIndex(self.current_step)

    @pyqtSlot()
    def on_noise_params_set(self):
        params = self.step2_widget.get_noise_parameters()
        self.generate_noisy_data(params)

        # 切换到步骤3
        self.current_step = 2
        self.stacked_widget.setCurrentIndex(self.current_step)

    def generate_noisy_data(self, params):
        noisy_data = self.original_data.copy()
        generators = []

        if params['gaussian']['enabled']:
            snr_db = params['gaussian']['snr_db']
            gaussian_gen = NoiseGeneratorFactory.create_generator("gaussian", snr_db=snr_db)
            noisy_data = gaussian_gen.add_noise(noisy_data)

        if params['impulse']['enabled']:
            noise_ratio = params['impulse']['noise_ratio']
            salt_ratio = params['impulse']['salt_ratio']
            impulse_gen = NoiseGeneratorFactory.create_generator("impulse", noise_ratio=noise_ratio, salt_ratio=salt_ratio)
            noisy_data = impulse_gen.add_noise(noisy_data)

        self.noisy_data = noisy_data

    @pyqtSlot()
    def on_denoiser_set(self):
        denoise_params = self.step3_widget.get_denoising_parameters()
        self.perform_denoising(denoise_params)

        # 计算指标
        metrics = self.calculate_metrics()

        # 传递显示所需内容
        data_dict = {
            'original': self.original_data,
            'noisy': self.noisy_data,
            'denoised': self.denoised_data
        }
        param_info = {
            'file_path': self.file_path,
            'variable_name': self.variable_name,
            'noise_params': self.step2_widget.get_noise_parameters(),
            'denoising_params': denoise_params,
        }

        self.step4_widget.update_display(data_dict, param_info, metrics)

        # 切换到第4步
        self.current_step = 3
        self.stacked_widget.setCurrentIndex(self.current_step)

    def perform_denoising(self, params):
        denoiser_type = params['method']
        denoiser_kwargs = params['params']
        denoiser = DenoisingFactory.create_denoiser(denoiser_type, **denoiser_kwargs)
        self.denoised_data = denoiser.denoise(self.noisy_data)

    def calculate_metrics(self):
        metrics = {}
        psnr_calc = MetricsFactory.create_calculator("psnr")
        ssim_calc = MetricsFactory.create_calculator("ssim")
        r_error_calc = MetricsFactory.create_calculator("relative_error")

        metrics['psnr'] = psnr_calc.calculate(self.original_data, self.denoised_data)
        metrics['ssim'] = ssim_calc.calculate(self.original_data, self.denoised_data)
        metrics['relative_error'] = r_error_calc.calculate(self.original_data, self.denoised_data)
        return metrics

    def save_results(self):
        # 后续可扩展保存操作（图像、指标、参数等）
        print("保存结果...（功能待实现）")


def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
