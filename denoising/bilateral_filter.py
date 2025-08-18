# denoising/bilateral_filter.py
import numpy as np
from scipy import ndimage
from scipy.spatial.distance import cdist


class BilateralFilter:
    """
    双边滤波器
    用于DAS数据的边缘保持平滑降噪
    在平滑噪声的同时保持数据的重要特征（如边缘）
    """

    def __init__(self, spatial_sigma=1.0, intensity_sigma=10.0, window_size=5):
        """
        初始化双边滤波器

        Args:
            spatial_sigma (float): 空间域标准差，控制空间邻近度权重
            intensity_sigma (float): 强度域标准差，控制强度相似度权重
            window_size (int): 滤波窗口大小
        """
        self.spatial_sigma = spatial_sigma
        self.intensity_sigma = intensity_sigma
        self.window_size = window_size

    def denoise(self, data, spatial_sigma=None, intensity_sigma=None, window_size=None):
        """
        对数据进行双边滤波降噪

        Args:
            data (np.ndarray): 输入数据 (1D或2D数组)
            spatial_sigma (float): 空间域标准差
            intensity_sigma (float): 强度域标准差
            window_size (int): 滤波窗口大小

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 使用参数或初始化值
        spatial_sigma = spatial_sigma if spatial_sigma is not None else self.spatial_sigma
        intensity_sigma = intensity_sigma if intensity_sigma is not None else self.intensity_sigma
        window_size = window_size if window_size is not None else self.window_size

        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 根据数据维度选择处理方法
        if data.ndim == 1:
            denoised_data = self._bilateral_filter_1d(
                data, spatial_sigma, intensity_sigma, window_size
            )
        elif data.ndim == 2:
            denoised_data = self._bilateral_filter_2d(
                data, spatial_sigma, intensity_sigma, window_size
            )
        else:
            raise ValueError("不支持的数据维度，仅支持1D和2D数据")

        return denoised_data

    def _bilateral_filter_1d(self, data, spatial_sigma, intensity_sigma, window_size):
        """
        1D双边滤波

        Args:
            data (np.ndarray): 1D输入数据
            spatial_sigma (float): 空间域标准差
            intensity_sigma (float): 强度域标准差
            window_size (int): 滤波窗口大小

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 确保窗口大小为奇数
        if window_size % 2 == 0:
            window_size += 1

        half_window = window_size // 2
        filtered_data = np.zeros_like(data)

        # 预计算空间权重
        spatial_weights = self._compute_spatial_weights_1d(window_size, spatial_sigma)

        # 对每个像素进行双边滤波
        for i in range(len(data)):
            # 确定窗口范围
            start_idx = max(0, i - half_window)
            end_idx = min(len(data), i + half_window + 1)

            # 提取窗口数据
            window_data = data[start_idx:end_idx]
            center_value = data[i]

            # 计算强度差异
            intensity_diff = window_data - center_value
            intensity_weights = np.exp(-0.5 * (intensity_diff / intensity_sigma) ** 2)

            # 计算总权重
            window_spatial_weights = spatial_weights[
                                     (half_window - (i - start_idx)):(half_window + (end_idx - i))
                                     ]
            total_weights = window_spatial_weights * intensity_weights

            # 归一化权重并计算加权平均
            if np.sum(total_weights) > 0:
                normalized_weights = total_weights / np.sum(total_weights)
                filtered_data[i] = np.sum(window_data * normalized_weights)
            else:
                filtered_data[i] = center_value

        return filtered_data

    def _bilateral_filter_2d(self, data, spatial_sigma, intensity_sigma, window_size):
        """
        2D双边滤波

        Args:
            data (np.ndarray): 2D输入数据
            spatial_sigma (float): 空间域标准差
            intensity_sigma (float): 强度域标准差
            window_size (int): 滤波窗口大小

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 确保窗口大小为奇数
        if window_size % 2 == 0:
            window_size += 1

        half_window = window_size // 2
        filtered_data = np.zeros_like(data)

        # 预计算空间权重
        spatial_weights = self._compute_spatial_weights_2d(window_size, spatial_sigma)

        # 对每个像素进行双边滤波
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                # 确定窗口范围
                row_start = max(0, i - half_window)
                row_end = min(data.shape[0], i + half_window + 1)
                col_start = max(0, j - half_window)
                col_end = min(data.shape[1], j + half_window + 1)

                # 提取窗口数据
                window_data = data[row_start:row_end, col_start:col_end]
                center_value = data[i, j]

                # 计算强度差异
                intensity_diff = window_data - center_value
                intensity_weights = np.exp(-0.5 * (intensity_diff / intensity_sigma) ** 2)

                # 计算空间权重
                window_spatial_weights = spatial_weights[
                                         (half_window - (i - row_start)):(half_window + (row_end - i)),
                                         (half_window - (j - col_start)):(half_window + (col_end - j))
                                         ]

                # 计算总权重
                total_weights = window_spatial_weights * intensity_weights

                # 归一化权重并计算加权平均
                if np.sum(total_weights) > 0:
                    normalized_weights = total_weights / np.sum(total_weights)
                    filtered_data[i, j] = np.sum(window_data * normalized_weights)
                else:
                    filtered_data[i, j] = center_value

        return filtered_data

    def _compute_spatial_weights_1d(self, window_size, spatial_sigma):
        """
        计算1D空间权重

        Args:
            window_size (int): 窗口大小
            spatial_sigma (float): 空间域标准差

        Returns:
            np.ndarray: 空间权重数组
        """
        half_window = window_size // 2
        distances = np.arange(-half_window, half_window + 1)
        spatial_weights = np.exp(-0.5 * (distances / spatial_sigma) ** 2)
        return spatial_weights

    def _compute_spatial_weights_2d(self, window_size, spatial_sigma):
        """
        计算2D空间权重

        Args:
            window_size (int): 窗口大小
            spatial_sigma (float): 空间域标准差

        Returns:
            np.ndarray: 空间权重数组
        """
        half_window = window_size // 2
        y, x = np.ogrid[-half_window:half_window + 1, -half_window:half_window + 1]
        distances_squared = x ** 2 + y ** 2
        spatial_weights = np.exp(-0.5 * distances_squared / (spatial_sigma ** 2))
        return spatial_weights

    def apply_fast_bilateral_filter(self, data, spatial_sigma=None, intensity_sigma=None):
        """
        应用快速双边滤波（简化版，使用scipy的高斯滤波近似）

        Args:
            data (np.ndarray): 输入数据
            spatial_sigma (float): 空间域标准差
            intensity_sigma (float): 强度域标准差

        Returns:
            np.ndarray: 降噪后的数据
        """
        spatial_sigma = spatial_sigma if spatial_sigma is not None else self.spatial_sigma
        intensity_sigma = intensity_sigma if intensity_sigma is not None else self.intensity_sigma

        data = np.asarray(data, dtype=np.float64)

        # 使用高斯滤波作为双边滤波的近似
        # 这是一种简化的实现方式
        denoised_data = ndimage.gaussian_filter(data, sigma=spatial_sigma)

        return denoised_data

    def apply_separable_bilateral_filter(self, data, spatial_sigma=None, intensity_sigma=None):
        """
        应用可分离双边滤波（分别对行和列进行1D双边滤波）

        Args:
            data (np.ndarray): 输入数据
            spatial_sigma (float): 空间域标准差
            intensity_sigma (float): 强度域标准差

        Returns:
            np.ndarray: 降噪后的数据
        """
        spatial_sigma = spatial_sigma if spatial_sigma is not None else self.spatial_sigma
        intensity_sigma = intensity_sigma if intensity_sigma is not None else self.intensity_sigma

        data = np.asarray(data, dtype=np.float64)

        # 先对行进行双边滤波
        temp_data = np.zeros_like(data)
        for i in range(data.shape[0]):
            temp_data[i, :] = self._bilateral_filter_1d(
                data[i, :], spatial_sigma, intensity_sigma, self.window_size
            )

        # 再对列进行双边滤波
        filtered_data = np.zeros_like(temp_data)
        for j in range(temp_data.shape[1]):
            filtered_data[:, j] = self._bilateral_filter_1d(
                temp_data[:, j], spatial_sigma, intensity_sigma, self.window_size
            )

        return filtered_data
