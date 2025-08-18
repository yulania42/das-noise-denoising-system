# denoising/gaussian_filter.py
import numpy as np
from scipy import ndimage
from scipy.ndimage import gaussian_filter

class GaussianFilter:
    """
    高斯滤波器
    用于DAS数据的高斯平滑降噪
    """

    def __init__(self,
                 sigma=1.0,
                 mode='reflect',
                 cval=0.0,
                 sigma_raw=None,
                 sigma_col=None,
                 size=None):
        """
        初始化高斯滤波器
        Args:
        sigma (float or tuple): 高斯核的标准差
        mode (str): 边界处理模式 ('reflect', 'constant', 'nearest', 'mirror', 'wrap')
        cval (float): 当mode='constant'时的填充值
        sigma_raw (float): 用于 apply_separable_filter 的行方向默认标准差
        sigma_col (float): 用于 apply_separable_filter 的列方向默认标准差
        size (int): 用于生成高斯核的大小
        """
        self.sigma = sigma
        self.mode = mode
        self.cval = cval
        self.sigma_raw = sigma_raw
        self.sigma_col = sigma_col
        self.size = size

    def denoise(self, data, sigma=None):
        """
        对数据进行高斯滤波降噪

        Args:
            data (np.ndarray): 输入数据 (2D数组，行表示时间，列表示距离)
            sigma (float or tuple): 高斯核标准差，如果提供则覆盖初始化值

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 使用参数或初始化值
        sigma = sigma if sigma is not None else self.sigma

        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 应用高斯滤波
        denoised_data = ndimage.gaussian_filter(
            data,
            sigma=sigma,
            mode=self.mode,
            cval=self.cval
        )

        return denoised_data

    def apply_separable_filter(self, data, sigma_row=None, sigma_col=None):
        """
        分别对行和列应用1D高斯滤波（可分离滤波器）

        Args:
            data (np.ndarray): 输入数据
            sigma_row (float): 行方向标准差
            sigma_col (float): 列方向标准差

        Returns:
            np.ndarray: 降噪后的数据
        """
        sigma_row = sigma_row if sigma_row is not None else self.sigma
        sigma_col = sigma_col if sigma_col is not None else self.sigma

        data = np.asarray(data, dtype=np.float64)

        # 先对行进行滤波
        if sigma_row > 0:
            temp_data = ndimage.gaussian_filter1d(
                data,
                sigma=sigma_row,
                axis=1,  # 行方向
                mode=self.mode,
                cval=self.cval
            )
        else:
            temp_data = data.copy()

        # 再对列进行滤波
        if sigma_col > 0:
            denoised_data = ndimage.gaussian_filter1d(
                temp_data,
                sigma=sigma_col,
                axis=0,  # 列方向
                mode=self.mode,
                cval=self.cval
            )
        else:
            denoised_data = temp_data

        return denoised_data

    def get_gaussian_kernel(self, size, sigma=None):
        """
        生成1D高斯核

        Args:
            size (int): 核大小
            sigma (float): 标准差

        Returns:
            np.ndarray: 高斯核
        """
        sigma = sigma if sigma is not None else self.sigma
        kernel = gaussian_filter(size, sigma)
        return kernel / np.sum(kernel)  # 归一化
