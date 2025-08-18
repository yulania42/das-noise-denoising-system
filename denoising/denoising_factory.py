# denoising/denoising_factory.py
from .gaussian_filter import GaussianFilter
from .moving_average_filter import MovingAverageFilter
from .median_filter import MedianFilter
from .wavelet_denoising import WaveletDenoising


class DenoisingFactory:
    """
    降噪器工厂
    根据降噪类型创建相应的降噪器
    """

    @staticmethod
    def create_denoiser(denoiser_type, **kwargs):
        """
        创建降噪器工厂方法

        Args:
            denoiser_type (str): 降噪器类型
                'gaussian': 高斯滤波
                'moving_average': 移动平均滤波
                'median': 中值滤波
                'wavelet': 小波降噪
            **kwargs: 传递给降噪器的参数

        Returns:
            Denoiser: 降噪器实例

        Raises:
            ValueError: 不支持的降噪器类型
        """
        denoiser_type = denoiser_type.lower()

        if denoiser_type == 'gaussian':
            return GaussianFilter(**kwargs)
        elif denoiser_type == 'moving_average' or denoiser_type == 'uniform':
            return MovingAverageFilter(**kwargs)
        elif denoiser_type == 'median':
            return MedianFilter(**kwargs)
        elif denoiser_type == 'wavelet':
            return WaveletDenoising(**kwargs)
        else:
            available_types = ['gaussian', 'moving_average', 'median']
            raise ValueError(f"不支持的降噪器类型: {denoiser_type}. 可用类型: {available_types}")

# 使用示例：
# gaussian_denoiser = DenoisingFactory.create_denoiser('gaussian', sigma=1.5)
# moving_avg_denoiser = DenoisingFactory.create_denoiser('moving_average', window_size=5)
# median_denoiser = DenoisingFactory.create_denoiser('median', size=3)
