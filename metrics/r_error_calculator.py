# -----------------------------
# 插入位置：metrics/r_error_calculator.py
# 描述：用于计算相对误差
# -----------------------------
import numpy as np


class RelativeErrorCalculator:
    """相对误差计算器类"""

    def calculate(self, original_data, processed_data, epsilon=1e-10):
        """
        计算两幅图像之间的相对误差

        参数:
            original_data: 原始数据 (numpy array)
            processed_data: 处理后数据 (numpy array)
            epsilon: 防止除零的小常数 (float)

        返回:
            relative_error: 相对误差值 (float)
        """
        # 确保数据形状一致
        if original_data.shape != processed_data.shape:
            raise ValueError("原始数据和处理后数据的形状必须一致")

        # 计算绝对误差
        absolute_error = np.abs(original_data - processed_data)

        # 计算原始数据的绝对值
        original_abs = np.abs(original_data)

        # 防止除零，将接近零的值替换为epsilon
        original_abs_safe = np.where(original_abs < epsilon, epsilon, original_abs)

        # 计算相对误差
        relative_error = np.mean(absolute_error / original_abs_safe)

        return relative_error

    def calculate_rmse_based(self, original_data, processed_data):
        """
        基于均方根误差的相对误差计算

        参数:
            original_data: 原始数据 (numpy array)
            processed_data: 处理后数据 (numpy array)

        返回:
            relative_error: 相对误差值 (float)
        """
        # 确保数据形状一致
        if original_data.shape != processed_data.shape:
            raise ValueError("原始数据和处理后数据的形状必须一致")

        # 计算均方根误差
        rmse = np.sqrt(np.mean((original_data - processed_data) ** 2))

        # 计算原始数据的均方根
        original_rmse = np.sqrt(np.mean(original_data ** 2))

        # 避免除零
        if original_rmse == 0:
            return float('inf') if rmse > 0 else 0.0

        # 计算相对误差
        relative_error = rmse / original_rmse

        return relative_error
