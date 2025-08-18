# denoising/moving_average_filter.py
import numpy as np
from scipy import ndimage


class MovingAverageFilter:
    """
    移动平均滤波器
    用于DAS数据的简单平滑降噪
    """

    def __init__(self, window_size=3, axis=None, mode='reflect'):
        """
        初始化移动平均滤波器

        Args:
            window_size (int or tuple): 滑动窗口大小
            axis (int or None): 应用滤波的轴，None表示所有轴
            mode (str): 边界处理模式 ('reflect', 'constant', 'nearest', 'mirror', 'wrap')
        """
        self.window_size = window_size
        self.axis = axis
        self.mode = mode

    def denoise(self, data, window_size=None, axis=None):
        """
        对数据进行移动平均滤波降噪

        Args:
            data (np.ndarray): 输入数据
            window_size (int or tuple): 窗口大小，如果提供则覆盖初始化值
            axis (int or None): 应用滤波的轴

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 使用参数或初始化值
        window_size = window_size if window_size is not None else self.window_size
        axis = axis if axis is not None else self.axis

        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 应用移动平均滤波
        if isinstance(window_size, (int, float)):
            # 统一窗口大小
            if axis is None:
                # 对所有轴应用相同大小的滤波器
                denoised_data = ndimage.uniform_filter(
                    data,
                    size=window_size,
                    mode=self.mode
                )
            else:
                # 仅对指定轴应用滤波器
                denoised_data = ndimage.uniform_filter1d(
                    data,
                    size=int(window_size),
                    axis=axis,
                    mode=self.mode
                )
        else:
            # 不同轴使用不同窗口大小
            denoised_data = ndimage.uniform_filter(
                data,
                size=window_size,
                mode=self.mode
            )

        return denoised_data

    def apply_directional_filter(self, data, time_window=5, distance_window=3):
        """
        分别对时间和距离方向应用不同窗口大小的移动平均滤波

        Args:
            data (np.ndarray): 输入数据 (2D数组)
            time_window (int): 时间方向窗口大小
            distance_window (int): 距离方向窗口大小

        Returns:
            np.ndarray: 降噪后的数据
        """
        data = np.asarray(data, dtype=np.float64)

        # 先对距离方向滤波
        temp_data = ndimage.uniform_filter1d(
            data,
            size=distance_window,
            axis=1,  # 距离方向
            mode=self.mode
        )

        # 再对时间方向滤波
        denoised_data = ndimage.uniform_filter1d(
            temp_data,
            size=time_window,
            axis=0,  # 时间方向
            mode=self.mode
        )

        return denoised_data

    def apply_weighted_moving_average(self, data, weights):
        """
        应用加权移动平均滤波

        Args:
            data (np.ndarray): 输入数据
            weights (np.ndarray): 权重数组

        Returns:
            np.ndarray: 降噪后的数据
        """
        data = np.asarray(data, dtype=np.float64)
        weights = np.asarray(weights, dtype=np.float64)

        # 归一化权重
        weights = weights / np.sum(weights)

        # 应用卷积
        denoised_data = ndimage.convolve(
            data,
            weights.reshape(-1, 1),  # 转换为2D卷积核
            mode=self.mode
        )

        return denoised_data
