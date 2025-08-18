# noise_generator/noise_factory.py
from .gaussian_noise import GaussianNoiseGenerator
from .impulse_noise import ImpulseNoiseGenerator


class NoiseGeneratorFactory:
    """
    噪声生成器工厂
    根据噪声类型创建相应的噪声生成器
    """

    @staticmethod
    def create_generator(noise_type, **kwargs):
        """
        创建噪声生成器工厂方法

        Args:
            noise_type (str): 噪声类型 ('gaussian', 'impulse', 等)
            **kwargs: 传递给生成器的参数

        Returns:
            NoiseGenerator: 噪声生成器实例

        Raises:
            ValueError: 不支持的噪声类型
        """
        if noise_type.lower() == 'gaussian':
            return GaussianNoiseGenerator(**kwargs)
        elif noise_type.lower() == 'impulse' or noise_type.lower() == 'salt_pepper':
            return ImpulseNoiseGenerator(**kwargs)
        else:
            raise ValueError(f"不支持的噪声类型: {noise_type}")

