# noise_generator/gaussian_noise.py
import numpy as np


class GaussianNoiseGenerator:
    """
    高斯噪声生成器
    为DAS数据添加高斯白噪声
    """

    def __init__(self, mean=0.0, std=1.0, seed=None, snr_db=10):
        """
        初始化高斯噪声生成器

        Args:
            mean (float): 噪声均值
            std (float): 噪声标准差
            seed (int): 随机种子
        """
        self.mean = mean
        self.std = std
        self.seed = seed
        self.snr_db = snr_db
        if seed is not None:
            np.random.seed(seed)

    def add_noise(self, data, snr_db=None):
        data = np.asarray(data, dtype=np.float64)
        # 如果没有单独提供 snr_db，则尝试使用 self.snr_db
        if snr_db is None and hasattr(self, 'snr_db'):
            snr_db = self.snr_db
        if snr_db is not None:
            noise_std = self._calculate_noise_std_from_snr(data, snr_db)
            noise = np.random.normal(self.mean, noise_std, data.shape)
        else:
            noise = np.random.normal(self.mean, self.std, data.shape)
        noisy_data = data + noise
        return noisy_data

    def _calculate_noise_std_from_snr(self, data, snr_db):
        """
        根据信噪比计算噪声标准差

        Args:
            data (np.ndarray): 原始数据
            snr_db (float): 信噪比(dB)

        Returns:
            float: 噪声标准差
        """
        # 计算信号功率
        signal_power = np.mean(data ** 2)

        # 计算噪声功率
        snr_linear = 10 ** (snr_db / 10)
        noise_power = signal_power / snr_linear

        # 计算噪声标准差
        noise_std = np.sqrt(noise_power)
        return noise_std

    def generate_noise_only(self, shape):
        """
        仅生成高斯噪声（不添加到数据）

        Args:
            shape (tuple): 噪声数组形状

        Returns:
            np.ndarray: 生成的高斯噪声
        """
        return np.random.normal(self.mean, self.std, shape)
