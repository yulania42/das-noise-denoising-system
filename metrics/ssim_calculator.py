# -----------------------------
# 插入位置：metrics/ssim_calculator.py
# 描述：用于计算结构相似性指数(SSIM)
# -----------------------------
import numpy as np
from skimage.metrics import structural_similarity as ssim_skimage


class SSIMCalculator:
    """SSIM计算器类"""

    def calculate(self, original_data, processed_data, **kwargs):
        """
        计算两幅图像之间的SSIM值

        参数:
            original_data: 原始数据 (numpy array)
            processed_data: 处理后数据 (numpy array)
            **kwargs: 其他传递给ssim_skimage的参数

        返回:
            ssim_value: SSIM值 (float)
        """
        # 确保数据形状一致
        if original_data.shape != processed_data.shape:
            raise ValueError("原始数据和处理后数据的形状必须一致")

        # 如果是多维数据，需要指定通道轴
        if len(original_data.shape) == 3:
            # 对于3D数据，我们计算每个通道的SSIM然后取平均
            ssim_values = []
            for i in range(original_data.shape[2]):
                ssim_val = ssim_skimage(
                    original_data[:, :, i],
                    processed_data[:, :, i],
                    data_range=processed_data[:, :, i].max() - processed_data[:, :, i].min(),
                    **kwargs
                )
                ssim_values.append(ssim_val)
            return np.mean(ssim_values)
        else:
            # 对于2D数据直接计算
            return ssim_skimage(
                original_data,
                processed_data,
                data_range=processed_data.max() - processed_data.min(),
                **kwargs
            )

    def calculate_per_channel(self, original_data, processed_data, **kwargs):
        """
        分别计算每个通道的SSIM值

        参数:
            original_data: 原始数据 (numpy array)
            processed_data: 处理后数据 (numpy array)
            **kwargs: 其他传递给ssim_skimage的参数

        返回:
            ssim_values: 每个通道的SSIM值列表 (list)
        """
        if len(original_data.shape) != 3:
            raise ValueError("此方法仅适用于多通道数据")

        ssim_values = []
        for i in range(original_data.shape[2]):
            ssim_val = ssim_skimage(
                original_data[:, :, i],
                processed_data[:, :, i],
                data_range=processed_data[:, :, i].max() - processed_data[:, :, i].min(),
                **kwargs
            )
            ssim_values.append(ssim_val)
        return ssim_values
