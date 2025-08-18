# noise_generator/impulse_noise.py
import numpy as np


class ImpulseNoiseGenerator:
    """
    脉冲噪声生成器
    为DAS数据添加脉冲噪声（椒盐噪声）
    """

    def __init__(self, noise_ratio=0.05, salt_ratio=0.5, seed=None):
        """
        初始化脉冲噪声生成器

        Args:
            noise_ratio (float): 噪声像素比例 (0-1)
            salt_ratio (float): 盐噪声比例 (0-1)，剩余为胡椒噪声
            seed (int): 随机种子
        """
        self.noise_ratio = noise_ratio
        self.salt_ratio = salt_ratio
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)

    def add_noise(self, data, noise_ratio=None, salt_ratio=None):
        """
        为数据添加脉冲噪声

        Args:
            data (np.ndarray): 原始数据
            noise_ratio (float): 噪声比例，如果提供则覆盖初始化值
            salt_ratio (float): 盐噪声比例，如果提供则覆盖初始化值

        Returns:
            np.ndarray: 添加脉冲噪声后的数据
        """
        # 使用参数或初始化值
        noise_ratio = noise_ratio if noise_ratio is not None else self.noise_ratio
        salt_ratio = salt_ratio if salt_ratio is not None else self.salt_ratio

        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)
        noisy_data = data.copy()

        # 计算噪声点数量
        total_points = data.size
        noise_points = int(total_points * noise_ratio)

        # 生成随机位置
        flat_data = noisy_data.flatten()
        indices = np.random.choice(total_points, noise_points, replace=False)

        # 计算盐噪声和胡椒噪声的数量
        salt_points = int(noise_points * salt_ratio)
        pepper_points = noise_points - salt_points

        # 获取数据的统计信息
        data_min = np.min(data)
        data_max = np.max(data)
        data_range = data_max - data_min

        # 添加盐噪声（高值）
        salt_indices = indices[:salt_points]
        flat_data[salt_indices] = data_max + 0.1 * data_range  # 超出正常范围的高值

        # 添加胡椒噪声（低值）
        pepper_indices = indices[salt_points:noise_points]
        flat_data[pepper_indices] = data_min - 0.1 * data_range  # 超出正常范围的低值

        # 重塑回原始形状
        noisy_data = flat_data.reshape(data.shape)

        return noisy_data

    def generate_mask(self, shape, noise_ratio=None):
        """
        生成脉冲噪声掩码

        Args:
            shape (tuple): 掩码形状
            noise_ratio (float): 噪声比例

        Returns:
            np.ndarray: 噪声掩码 (0:正常, 1:盐噪声, 2:胡椒噪声)
        """
        noise_ratio = noise_ratio if noise_ratio is not None else self.noise_ratio

        # 创建掩码
        mask = np.zeros(shape, dtype=np.int8)
        total_points = np.prod(shape)
        noise_points = int(total_points * noise_ratio)

        # 生成随机位置
        flat_mask = mask.flatten()
        indices = np.random.choice(total_points, noise_points, replace=False)

        # 计算盐噪声和胡椒噪声的数量
        salt_points = int(noise_points * self.salt_ratio)

        # 设置掩码值
        flat_mask[indices[:salt_points]] = 1  # 盐噪声
        flat_mask[indices[salt_points:noise_points]] = 2  # 胡椒噪声

        return flat_mask.reshape(shape)
