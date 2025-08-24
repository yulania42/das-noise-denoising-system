# time_series_visualizer.py
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Optional


class TimeSeriesVisualizer:
    """专门用于绘制DAS数据时间序列的可视化器"""

    def __init__(self):
        """初始化时间序列可视化器"""
        pass

    def plot_strain_rate_time_series(self, data: np.ndarray, time_axis: np.ndarray,
                                     depth_index: int, title: str = "Strain Rate Time Series",
                                     xlabel: str = "Time (s)", ylabel: str = "Strain Rate (με/s)",
                                     show: bool = True, save_path: Optional[str] = None,
                                     figsize: Tuple[int, int] = (12, 6), **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        绘制特定深度处应变率随时间变化的曲线图

        参数:
        - data: 2D numpy array - DAS数据 (time x depth)
        - time_axis: 1D array - 时间轴
        - depth_index: int - 指定深度索引
        - title: str - 图像标题
        - xlabel: str - x轴标签
        - ylabel: str - y轴标签
        - show: bool - 是否显示图像
        - save_path: str - 保存路径
        - figsize: tuple - 图像大小
        - **kwargs: 其他绘图参数

        返回:
        - fig: matplotlib figure对象
        - ax: matplotlib axes对象
        """
        # 验证输入参数
        if not isinstance(data, np.ndarray) or data.ndim != 2:
            raise ValueError("数据必须是二维numpy数组")

        if not isinstance(time_axis, np.ndarray) or time_axis.ndim != 1:
            raise ValueError("时间轴必须是一维numpy数组")

        if depth_index < 0 or depth_index >= data.shape[1]:
            raise ValueError(f"深度索引 {depth_index} 超出数据范围 [0, {data.shape[1] - 1}]")

        if len(time_axis) != data.shape[0]:
            raise ValueError("时间轴长度必须与数据时间维度匹配")

        # 提取特定深度的数据
        strain_rate_at_depth = data[:, depth_index]

        # 创建图形
        fig, ax = plt.subplots(figsize=figsize)

        # 绘制时间序列
        line_plot = ax.plot(time_axis, strain_rate_at_depth, linewidth=1, color='blue', **kwargs)

        # 设置标题和标签
        ax.set_title(f"{title} at Depth Index {depth_index}", fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        # 添加网格
        ax.grid(True, alpha=0.3)

        # 设置样式
        ax.tick_params(axis='both', which='major', labelsize=10)

        # 添加统计信息
        mean_value = np.mean(strain_rate_at_depth)
        std_value = np.std(strain_rate_at_depth)
        ax.axhline(y=mean_value, color='red', linestyle='--', alpha=0.7,
                   label=f'Mean: {mean_value:.2e}')
        ax.axhline(y=mean_value + std_value, color='orange', linestyle=':', alpha=0.7,
                   label=f'+1σ: {mean_value + std_value:.2e}')
        ax.axhline(y=mean_value - std_value, color='orange', linestyle=':', alpha=0.7,
                   label=f'-1σ: {mean_value - std_value:.2e}')
        ax.legend()

        # 保存图像
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')

        # 显示图像
        if show:
            plt.show()

        return fig, ax

    def plot_multiple_depths_time_series(self, data: np.ndarray, time_axis: np.ndarray,
                                         depth_indices: list, title: str = "Strain Rate Time Series Comparison",
                                         xlabel: str = "Time (s)", ylabel: str = "Strain Rate (με/s)",
                                         show: bool = True, save_path: Optional[str] = None,
                                         figsize: Tuple[int, int] = (12, 8), **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        绘制多个深度处应变率随时间变化的对比曲线图

        参数:
        - data: 2D numpy array - DAS数据 (time x depth)
        - time_axis: 1D array - 时间轴
        - depth_indices: list - 指定深度索引列表
        - title: str - 图像标题
        - xlabel: str - x轴标签
        - ylabel: str - y轴标签
        - show: bool - 是否显示图像
        - save_path: str - 保存路径
        - figsize: tuple - 图像大小
        - **kwargs: 其他绘图参数

        返回:
        - fig: matplotlib figure对象
        - ax: matplotlib axes对象
        """
        # 验证输入参数
        if not isinstance(depth_indices, list) or len(depth_indices) == 0:
            raise ValueError("深度索引列表不能为空")

        # 创建图形
        fig, ax = plt.subplots(figsize=figsize)

        # 定义颜色循环
        colors = plt.cm.tab10(np.linspace(0, 1, len(depth_indices)))

        # 绘制每个深度的时间序列
        for i, depth_index in enumerate(depth_indices):
            if depth_index < 0 or depth_index >= data.shape[1]:
                print(f"警告: 深度索引 {depth_index} 超出范围，跳过")
                continue

            strain_rate_at_depth = data[:, depth_index]
            ax.plot(time_axis, strain_rate_at_depth, linewidth=1,
                    color=colors[i], label=f'Depth {depth_index}', **kwargs)

        # 设置标题和标签
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        # 添加网格和图例
        ax.grid(True, alpha=0.3)
        ax.legend()

        # 设置样式
        ax.tick_params(axis='both', which='major', labelsize=10)

        # 保存图像
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')

        # 显示图像
        if show:
            plt.show()

        return fig, ax

    def plot_time_series_with_statistics(self, data: np.ndarray, time_axis: np.ndarray,
                                         depth_index: int, window_size: int = 100,
                                         title: str = "Strain Rate Time Series with Statistics",
                                         xlabel: str = "Time (s)", ylabel: str = "Strain Rate (με/s)",
                                         show: bool = True, save_path: Optional[str] = None,
                                         figsize: Tuple[int, int] = (12, 6)) -> Tuple[plt.Figure, plt.Axes]:
        """
        绘制时间序列及其移动平均和标准差

        参数:
        - data: 2D numpy array - DAS数据 (time x depth)
        - time_axis: 1D array - 时间轴
        - depth_index: int - 指定深度索引
        - window_size: int - 移动窗口大小
        - title: str - 图像标题
        - xlabel: str - x轴标签
        - ylabel: str - y轴标签
        - show: bool - 是否显示图像
        - save_path: str - 保存路径
        - figsize: tuple - 图像大小

        返回:
        - fig: matplotlib figure对象
        - ax: matplotlib axes对象
        """
        # 提取特定深度的数据
        strain_rate_at_depth = data[:, depth_index]

        # 计算移动平均和标准差
        if len(strain_rate_at_depth) >= window_size:
            moving_avg = np.convolve(strain_rate_at_depth, np.ones(window_size) / window_size, mode='valid')
            # 计算移动标准差
            moving_std = np.array([np.std(strain_rate_at_depth[i:i + window_size])
                                   for i in range(len(strain_rate_at_depth) - window_size + 1)])

            # 调整时间轴以匹配移动平均长度
            valid_time_axis = time_axis[window_size // 2:-window_size // 2 + 1] if window_size % 2 == 1 else \
                time_axis[window_size // 2 - 1:-window_size // 2]
        else:
            moving_avg = strain_rate_at_depth
            moving_std = np.zeros_like(strain_rate_at_depth)
            valid_time_axis = time_axis

        # 创建图形
        fig, ax = plt.subplots(figsize=figsize)

        # 绘制原始数据
        ax.plot(time_axis, strain_rate_at_depth, linewidth=0.8, color='lightblue', alpha=0.7, label='Original')

        # 绘制移动平均
        if len(valid_time_axis) == len(moving_avg):
            ax.plot(valid_time_axis, moving_avg, linewidth=2, color='blue',
                    label=f'Moving Average ({window_size} points)')

            # 绘制标准差带
            ax.fill_between(valid_time_axis, moving_avg - moving_std, moving_avg + moving_std,
                            alpha=0.3, color='blue', label='±1σ')

        # 设置标题和标签
        ax.set_title(f"{title} at Depth Index {depth_index}", fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)

        # 添加网格和图例
        ax.grid(True, alpha=0.3)
        ax.legend()

        # 设置样式
        ax.tick_params(axis='both', which='major', labelsize=10)

        # 保存图像
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')

        # 显示图像
        if show:
            plt.show()

        return fig, ax
