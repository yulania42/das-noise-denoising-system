# visualization/visualization_factory.py
from .heatmap_visualizer import HeatmapVisualizer


# 后续可以添加其他可视化器

class VisualizationFactory:
    """
    可视化器工厂
    根据可视化类型创建相应的可视化器
    """

    @staticmethod
    def create_visualizer(visualizer_type: str, **kwargs):
        """
        创建可视化器工厂方法

        Args:
            visualizer_type (str): 可视化器类型
                'heatmap': 热力图可视化器
            **kwargs: 传递给可视化器的参数

        Returns:
            Visualizer: 可视化器实例

        Raises:
            ValueError: 不支持的可视化器类型
        """
        visualizer_type = visualizer_type.lower()

        if visualizer_type == 'heatmap':
            return HeatmapVisualizer(**kwargs)
        else:
            available_types = ['heatmap']
            raise ValueError(f"不支持的可视化器类型: {visualizer_type}. 可用类型: {available_types}")
