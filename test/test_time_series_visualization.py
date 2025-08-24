# test_time_series_visualization.py
import config2
import numpy as np
import sys
import os
import matplotlib as plt
# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_time_series_visualization(das_file_path):
    """
    测试时序一维图像生成功能

    参数:
    das_file_path: str - DAS数据文件路径
    """

    try:
        # 读取DAS数据文件
        # 根据您的文件格式选择合适的读取方式
        # 如果是.npy文件:
        if das_file_path.endswith('.npy'):
            data = np.load(das_file_path)
        # 如果是.mat文件:
        elif das_file_path.endswith('.mat'):
            import scipy.io
            mat_data = scipy.io.loadmat(das_file_path)
            # 请根据您的mat文件结构调整这里
            data = mat_data['strain_fiber_rate']  # 假设数据存储在'data'变量中
        # 如果是CSV文件:
        elif das_file_path.endswith('.csv'):
            data = np.loadtxt(das_file_path, delimiter=',')
        else:
            raise ValueError("不支持的文件格式")

        print(f"数据形状: {data.shape}")

        # 生成时间轴和深度轴
        time_samples = data.shape[0]
        depth_samples = data.shape[1]

        # 假设采样率和空间采样间隔（请根据实际情况调整）
        time_axis = np.linspace(0, time_samples / 1000, time_samples)  # 假设1000Hz采样率
        distance_axis = np.linspace(0, depth_samples * 10, depth_samples)  # 假设10m空间间隔

        # 导入可视化模块
        from visualization.visualization_factory import VisualizationFactory

        # 创建可视化器实例
        visualizer = VisualizationFactory().create_visualizer("time_series")

        # 测试1: 绘制指定深度的时序图像
        depth_index = depth_samples // 2  # 选择中间深度
        fig1, ax1 = visualizer.plot_strain_rate_time_series(
            data=data,
            time_axis=time_axis,
            depth_index=depth_index,
            title=f'DAS时序数据 - 深度索引 {depth_index}',
            xlabel='时间 (s)',
            ylabel='应变率',
            show=True,
            save_path=f'test_time_series_depth_{depth_index}.png',
            figsize=(12, 6)
        )
        print(f"时序图像已保存到: test_time_series_depth_{depth_index}.png")

        # 测试2: 绘制多个深度的时序对比图像
        depth_indices = [depth_samples // 4, depth_samples // 2, 3 * depth_samples // 4]
        fig2, ax2 = visualizer.plot_multiple_depths_time_series(
            data=data,
            time_axis=time_axis,
            depth_indices=depth_indices,
            title='多个深度位置的时序数据对比',
            xlabel='时间 (s)',
            ylabel='应变率',
            show=True,
            save_path='test_multiple_depths_time_series.png',
            figsize=(12, 8)
        )
        print("多深度时序对比图像已保存到: test_multiple_depths_time_series.png")

        # 测试3: 绘制带统计信息的时序图像
        fig3, ax3 = visualizer.plot_time_series_with_statistics(
            data=data,
            time_axis=time_axis,
            depth_index=depth_index,
            window_size=100,
            title=f'带统计信息的时序数据 - 深度索引 {depth_index}',
            xlabel='时间 (s)',
            ylabel='应变率',
            show=True,
            save_path=f'test_time_series_with_stats_{depth_index}.png',
            figsize=(12, 6)
        )
        print(f"带统计信息的时序图像已保存到: test_time_series_with_stats_{depth_index}.png")

        return True

    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # 请在这里填入您的DAS文件路径
    das_file_path = r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\docs\strain_fiber_rate_model3.mat"  # 请修改为您的实际文件路径

    # 检查文件是否存在
    if not os.path.exists(das_file_path):
        print(f"文件不存在: {das_file_path}")
        print("请修改代码中的文件路径为您的实际DAS数据文件路径")
        sys.exit(1)

    # 运行测试
    success = test_time_series_visualization(das_file_path)

    if success:
        print("所有测试完成!")
    else:
        print("测试失败!")
