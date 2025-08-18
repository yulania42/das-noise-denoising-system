# -----------------------------
# 插入位置：metrics/metrics_factory.py
# 描述：用于创建指标计算器的工厂类
# -----------------------------
from .ssim_calculator import SSIMCalculator
from .psnr_calculator import PSNRCalculator
from .r_error_calculator import RelativeErrorCalculator


class MetricsFactory:
    """指标计算器工厂类"""

    @staticmethod
    def create_calculator(metric_type, **kwargs):
        """
        创建指定类型的指标计算器

        参数:
            metric_type: 指标类型 (str)
            **kwargs: 传递给具体计算器的参数

        返回:
            具体的指标计算器实例
        """
        if metric_type == "ssim":
            return SSIMCalculator(**kwargs)
        elif metric_type == "psnr":
            return PSNRCalculator(**kwargs)
        elif metric_type == "relative_error":
            return RelativeErrorCalculator(**kwargs)
        else:
            raise ValueError(f"不支持的指标类型: {metric_type}")
