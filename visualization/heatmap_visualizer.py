# visualization/heatmap_visualizer.py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import Normalize
from typing import Optional, Tuple, Dict, Any


class HeatmapVisualizer:
    """
    热力图可视化器
    用于绘制DAS数据的热力图可视化
    """

    def __init__(self,
                 cmap: str = 'seismic',
                 figsize: Tuple[float, float] = (12, 8),
                 dpi: int = 100,
                 aspect: str = 'auto'):
        """
        初始化热力图可视化器

        Args:
            cmap (str): 颜色映射
            figsize (tuple): 图形大小 (width, height)
            dpi (int): 图形分辨率
            aspect (str): 图像纵横比 ('auto', 'equal', numeric)
        """
        self.cmap = cmap
        self.figsize = figsize
        self.dpi = dpi
        self.aspect = aspect
        self.fig = None
        self.ax = None

    def plot_heatmap(self,
                     data: np.ndarray,
                     time_axis: Optional[np.ndarray] = None,
                     distance_axis: Optional[np.ndarray] = None,
                     title: str = "DAS Data Heatmap",
                     xlabel: str = "Distance (m)",
                     ylabel: str = "Time (s)",
                     vmin: Optional[float] = None,
                     vmax: Optional[float] = None,
                     colorbar: bool = True,
                     colorbar_label: str = "Amplitude",
                     show: bool = True,
                     save_path: Optional[str] = None,
                     **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        绘制数据热力图

        Args:
            data (np.ndarray): 2D数据数组
            time_axis (np.ndarray): 时间轴数据
            distance_axis (np.ndarray): 距离轴数据
            title (str): 图形标题
            xlabel (str): X轴标签
            ylabel (str): Y轴标签
            vmin (float): 颜色映射最小值
            vmax (float): 颜色映射最大值
            colorbar (bool): 是否显示颜色条
            colorbar_label (str): 颜色条标签
            show (bool): 是否显示图形
            save_path (str): 保存路径
            **kwargs: 传递给imshow的其他参数

        Returns:
            tuple: (figure, axes) matplotlib图形和轴对象
        """
        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 验证数据维度
        if data.ndim != 2:
            raise ValueError("数据必须是2D数组")

        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # 设置默认参数
        plot_kwargs = {
            'cmap': self.cmap,
            'aspect': self.aspect,
            'origin': 'lower'
        }
        plot_kwargs.update(kwargs)

        # 如果提供了vmin和vmax，则使用它们
        if vmin is not None:
            plot_kwargs['vmin'] = vmin
        if vmax is not None:
            plot_kwargs['vmax'] = vmax

        # 绘制热力图
        im = self.ax.imshow(data.T, **plot_kwargs)

        # 设置坐标轴
        self._set_axes(data, time_axis, distance_axis, xlabel, ylabel)

        # 设置标题
        self.ax.set_title(title, fontsize=14, pad=20)

        # 添加颜色条
        if colorbar:
            cbar = self.fig.colorbar(im, ax=self.ax, shrink=0.8)
            cbar.set_label(colorbar_label, rotation=270, labelpad=20)

        # 调整布局
        self.fig.tight_layout()

        # 保存图形
        if save_path:
            self.fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')

        # 显示图形
        if show:
            plt.show()

        return self.fig, self.ax

    def _set_axes(self,
                  data: np.ndarray,
                  time_axis: Optional[np.ndarray],
                  distance_axis: Optional[np.ndarray],
                  xlabel: str,
                  ylabel: str):
        """
        设置坐标轴标签和刻度

        Args:
            data (np.ndarray): 数据数组
            time_axis (np.ndarray): 时间轴数据
            distance_axis (np.ndarray): 距离轴数据
            xlabel (str): X轴标签
            ylabel (str): Y轴标签
        """
        time_points, distance_points = data.shape

        if time_axis is not None and len(time_axis) == time_points:
            # 使用提供的时间轴
            self.ax.set_yticks(np.linspace(0, time_points - 1, min(10, time_points)))
            time_tick_labels = np.linspace(time_axis[0], time_axis[-1], min(10, time_points))
            self.ax.set_yticklabels([f'{t:.2f}' for t in time_tick_labels])
        else:
            # 使用默认索引
            self.ax.set_yticks(np.linspace(0, time_points - 1, min(10, time_points)))
            self.ax.set_yticklabels([f'{int(i)}' for i in np.linspace(0, time_points - 1, min(10, time_points))])

        if distance_axis is not None and len(distance_axis) == distance_points:
            # 使用提供的距离轴
            self.ax.set_xticks(np.linspace(0, distance_points - 1, min(10, distance_points)))
            distance_tick_labels = np.linspace(distance_axis[0], distance_axis[-1], min(10, distance_points))
            self.ax.set_xticklabels([f'{d:.0f}' for d in distance_tick_labels])
        else:
            # 使用默认索引
            self.ax.set_xticks(np.linspace(0, distance_points - 1, min(10, distance_points)))
            self.ax.set_xticklabels(
                [f'{int(i)}' for i in np.linspace(0, distance_points - 1, min(10, distance_points))])

        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def plot_heatmap_with_stats(self,
                                data: np.ndarray,
                                time_axis: Optional[np.ndarray] = None,
                                distance_axis: Optional[np.ndarray] = None,
                                title: str = "DAS Data Heatmap with Statistics",
                                show_stats: bool = True,
                                additional_text: Optional[str] = None,
                                vmin: Optional[float] = None,
                                vmax: Optional[float] = None,
                                **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        绘制带统计信息的热力图
        Args:
            data (np.ndarray): 2D数据数组
            time_axis (np.ndarray): 时间轴数据
            distance_axis (np.ndarray): 距离轴数据
            title (str): 图形标题
            show_stats (bool): 是否显示基础统计信息 (mean, std, max, min)
            additional_text (str): 自定义附加文本（如PSNR等），显示在图像左上角
            vmin (float): 颜色映射最小值
            vmax (float): 颜色映射最大值
            **kwargs: 传递给imshow的其他参数
        Returns:
            tuple: (figure, axes) matplotlib图形和轴对象
        """
        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)
        # 计算默认统计数据
        stats_title_part = ""
        if show_stats:
            data_mean = np.mean(data)
            data_std = np.std(data)
            data_max = np.max(data)
            data_min = np.min(data)
            stats_title_part = f'\nMean: {data_mean:.2f} | Std: {data_std:.2f} | Max: {data_max:.2f} | Min: {data_min:.2f}'
        # 完整标题组合
        full_title = title + stats_title_part
        # 传递 vmin 和 vmax 到 plot_heatmap
        fig, ax = self.plot_heatmap(
            data, time_axis, distance_axis,
            full_title,
            vmin=vmin,
            vmax=vmax,
            **kwargs
        )
        # 显示附加文本（科研指标如 PSNR、SSIM）
        if additional_text:
            ax.text(
                0.02, 0.98, additional_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7)
            )
        return fig, ax

    def plot_multiple_heatmaps(self,
                               data_list: list,
                               titles: list,
                               time_axis: Optional[np.ndarray] = None,
                               distance_axis: Optional[np.ndarray] = None,
                               figsize: Tuple[float, float] = (15, 5),
                               vmin: Optional[float] = None,
                               vmax: Optional[float] = None,
                               vmin_list: Optional[list] = None,
                               vmax_list: Optional[list] = None,
                               **kwargs) -> Tuple[plt.Figure, list]:
        """
        绘制多个热力图进行比较

        Args:
            data_list (list): 数据数组列表
            titles (list): 标题列表
            time_axis (np.ndarray): 时间轴数据
            distance_axis (np.ndarray): 距离轴数据
            figsize (tuple): 图形大小
            vmin (float): 默认最小值（用于所有图）
            vmax (float): 默认最大值（用于所有图）
            vmin_list (list): 每张图对应的vmin值（覆盖vmin）
            vmax_list (list): 每张图对应的vmax值（覆盖vmax）
            **kwargs: 其他imshow参数（注意会被共享）

        Returns:
            tuple: (figure, axes_list) matplotlib图形和轴对象列表
        """
        num_plots = len(data_list)

        if len(titles) != num_plots:
            raise ValueError("标题数量必须与数据数量一致")

        # 处理 vmin/vmax 列表或统一值
        if vmin_list is not None:
            if len(vmin_list) != num_plots:
                raise ValueError("vmin_list长度必须与data_list相同")
        else:
            vmin_list = [vmin] * num_plots

        if vmax_list is not None:
            if len(vmax_list) != num_plots:
                raise ValueError("vmax_list长度必须与data_list相同")
        else:
            vmax_list = [vmax] * num_plots

        # 创建图形
        self.fig, axes = plt.subplots(1, num_plots, figsize=figsize, dpi=self.dpi)
        if num_plots == 1:
            axes = [axes]

        # 为每个数据集绘制热力图
        for i, (data, title, vmin_i, vmax_i) in enumerate(zip(data_list, titles, vmin_list, vmax_list)):
            data = np.asarray(data, dtype=np.float64)

            # 设置默认imshow参数
            plot_kwargs = {
                'cmap': self.cmap,
                'aspect': self.aspect,
                'origin': 'lower'
            }
            if vmin_i is not None:
                plot_kwargs['vmin'] = vmin_i
            if vmax_i is not None:
                plot_kwargs['vmax'] = vmax_i
            plot_kwargs.update(kwargs)

            # 绘制热力图
            im = axes[i].imshow(data.T, **plot_kwargs)

            # 设置坐标轴
            self._set_axes(data, time_axis, distance_axis, "Distance (m)", "Time (s)")

            # 设置标题
            axes[i].set_title(title, fontsize=12)

            # 添加颜色条
            cbar = self.fig.colorbar(im, ax=axes[i], shrink=0.8)
            cbar.set_label("Amplitude", rotation=270, labelpad=15)

        # 调整布局
        self.fig.tight_layout()

        return self.fig, axes

    def plot_heatmap_contour(self,
                             data: np.ndarray,
                             time_axis: Optional[np.ndarray] = None,
                             distance_axis: Optional[np.ndarray] = None,
                             title: str = "DAS Data Heatmap with Contours",
                             contour_levels: int = 10,
                             **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """
        绘制带等高线的热力图

        Args:
            data (np.ndarray): 2D数据数组
            time_axis (np.ndarray): 时间轴数据
            distance_axis (np.ndarray): 距离轴数据
            title (str): 图形标题
            contour_levels (int): 等高线层数
            **kwargs: 传递给imshow的其他参数

        Returns:
            tuple: (figure, axes) matplotlib图形和轴对象
        """
        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # 绘制热力图
        plot_kwargs = {
            'cmap': self.cmap,
            'aspect': self.aspect,
            'origin': 'lower'
        }
        plot_kwargs.update(kwargs)

        im = self.ax.imshow(data.T, **plot_kwargs)

        # 添加等高线
        if distance_axis is not None and time_axis is not None:
            X, Y = np.meshgrid(distance_axis, time_axis)
            contours = self.ax.contour(X, Y, data.T, levels=contour_levels, colors='black', alpha=0.4, linewidths=0.5)
        else:
            # 使用索引坐标
            Y_indices, X_indices = np.meshgrid(range(data.shape[0]), range(data.shape[1]))
            contours = self.ax.contour(X_indices, Y_indices, data.T, levels=contour_levels, colors='black', alpha=0.4,
                                       linewidths=0.5)

        # 设置坐标轴
        self._set_axes(data, time_axis, distance_axis, "Distance (m)", "Time (s)")

        # 设置标题
        self.ax.set_title(title, fontsize=14)

        # 添加颜色条
        cbar = self.fig.colorbar(im, ax=self.ax, shrink=0.8)
        cbar.set_label("Amplitude", rotation=270, labelpad=20)

        # 添加等高线标签
        self.ax.clabel(contours, inline=True, fontsize=8)

        # 调整布局
        self.fig.tight_layout()

        return self.fig, self.ax

    def close(self):
        """关闭当前图形"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
