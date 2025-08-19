# 文件位置: gui/__init__.py

"""
GUI模块初始化文件
此文件负责导出所有GUI组件，方便其他模块导入使用
"""

# 导入所有GUI组件
from .step1_file_selection import FileSelectionWidget
from .step2_noise_params import NoiseParametersWidget
from .step3_denoising_method import DenoisingMethodWidget
from .step4_image_display import ImageDisplayWidget
from .widget_factory import create_widget

# 定义公共接口
__all__ = [
    'FileSelectionWidget',
    'NoiseParametersWidget',
    'DenoisingMethodWidget',
    'ImageDisplayWidget',
    'create_widget'
]
