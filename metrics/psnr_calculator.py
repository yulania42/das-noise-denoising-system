# -----------------------------
# 插入位置：metrics/psnr_calculator.py
# 描述：用于计算峰值信噪比(PSNR)
# -----------------------------
import numpy as np


class PSNRCalculator:
    """PSNR计算器类"""

    def calculate(self, original_data, processed_data):
        """
        计算两幅图像之间的PSNR值

        参数:
            original_data: 原始数据 (numpy array)
            processed_data: 处理后数据 (numpy array)

        返回:
            psnr_value: PSNR值 (float)
        """
        # 确保数据形状一致
        if original_data.shape != processed_data.shape:
            raise ValueError("原始数据和处理后数据的形状必须一致")

        # 计算均方误差(MSE)
        mse = np.mean((original_data - processed_data) ** 2)

        # 避免除零错误
        if mse == 0:
            return float('inf')

        # 计算数据范围
        data_range = original_data.max() - original_data.min()

        # 计算PSNR
        psnr = 20 * np.log10(data_range / np.sqrt(mse))

        return psnr

    def calculate_per_channel(self, original_data, processed_data):
        """
        分别计算每个通道的PSNR值

        参数:
            original_data: 原始数据 (numpy array)
            processed_data: 处理后数据 (numpy array)

        返回:
            psnr_values: 每个通道的PSNR值列表 (list)
        """
        if len(original_data.shape) != 3:
            raise ValueError("此方法仅适用于多通道数据")

        psnr_values = []
        for i in range(original_data.shape[2]):
            mse = np.mean((original_data[:, :, i] - processed_data[:, :, i]) ** 2)
            if mse == 0:
                psnr_values.append(float('inf'))
            else:
                data_range = original_data[:, :, i].max() - original_data[:, :, i].min()
                psnr = 20 * np.log10(data_range / np.sqrt(mse))
                psnr_values.append(psnr)
        return psnr_values
