# denoising/median_filter.py
import numpy as np
from scipy import ndimage


class MedianFilter:
    """
    中值滤波器
    用于DAS数据的椒盐噪声去除和边缘保持平滑
    """

    def __init__(self, size=3, mode='reflect'):
        """
        初始化中值滤波器

        Args:
            size (int or tuple): 滤波器窗口大小
            mode (str): 边界处理模式 ('reflect', 'constant', 'nearest', 'mirror', 'wrap')
        """
        self.size = size
        self.mode = mode

    def denoise(self, data, size=None):
        """
        对数据进行中值滤波降噪

        Args:
            data (np.ndarray): 输入数据
            size (int or tuple): 滤波器窗口大小，如果提供则覆盖初始化值

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 使用参数或初始化值
        size = size if size is not None else self.size

        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 应用中值滤波
        denoised_data = ndimage.median_filter(
            data,
            size=size,
            mode=self.mode
        )

        return denoised_data

    def apply_adaptive_median_filter(self, data, max_size=7):
        """
        应用自适应中值滤波（简化版）

        Args:
            data (np.ndarray): 输入数据
            max_size (int): 最大窗口大小

        Returns:
            np.ndarray: 降噪后的数据
        """
        data = np.asarray(data, dtype=np.float64)

        # 对于自适应中值滤波，这里使用固定大小的中值滤波
        # 实际的自适应中值滤波需要更复杂的逻辑
        denoised_data = ndimage.median_filter(
            data,
            size=min(max_size, 3),  # 使用较小的窗口作为简化
            mode=self.mode
        )

        return denoised_data

    def apply_directional_median_filter(self, data, size_time=3, size_distance=3):
        """
        分别对时间和距离方向应用中值滤波

        Args:
            data (np.ndarray): 输入数据
            size_time (int): 时间方向窗口大小
            size_distance (int): 距离方向窗口大小

        Returns:
            np.ndarray: 降噪后的数据
        """
        data = np.asarray(data, dtype=np.float64)

        # 先对距离方向滤波
        temp_data = ndimage.median_filter(
            data,
            size=(1, size_distance),  # 仅距离方向
            mode=self.mode
        )

        # 再对时间方向滤波
        denoised_data = ndimage.median_filter(
            temp_data,
            size=(size_time, 1),  # 仅时间方向
            mode=self.mode
        )

        return denoised_data

    def remove_impulse_noise(self, data, size=None, threshold=None):
        """
        专门用于去除脉冲噪声的中值滤波

        Args:
            data (np.ndarray): 输入数据
            size (int or tuple): 滤波器窗口大小
            threshold (float): 噪声检测阈值（可选）

        Returns:
            np.ndarray: 去除脉冲噪声后的数据
        """
        # 使用参数或初始化值
        size = size if size is not None else self.size

        data = np.asarray(data, dtype=np.float64)

        # 应用中值滤波去除脉冲噪声
        denoised_data = ndimage.median_filter(
            data,
            size=size,
            mode=self.mode
        )

        return denoised_data
