# test_add_noise_visualization.py
import numpy as np
import scipy.io as sio
from data_loader.data_loader_factory import DataLoaderFactory
from noise_generator.noise_factory import NoiseGeneratorFactory
from visualization.visualization_factory import VisualizationFactory

mat_file_path = r"C:\Users\17981\Desktop\科研\光纤\strain_fiber_rate_model3.mat"
def test_noise_and_visualization(mat_file_path, variable_name='data'):
    """
    测试噪声添加和可视化功能

    Args:
        mat_file_path (str): MATLAB文件路径
        variable_name (str): 数据变量名
    """

    print("开始测试噪声添加和可视化功能...")

    # 1. 加载数据
    print("1. 加载数据...")
    loader = DataLoaderFactory.create_loader('matlab')
    try:
        data, metadata = loader.load_data(mat_file_path, variable_name)
        print(f"   数据形状: {data.shape}")
        print(f"   数据类型: {data.dtype}")
        if metadata:
            print(f"   元数据: {metadata}")
    except Exception as e:
        print(f"   加载数据失败: {e}")

    # 2. 创建噪声生成器
    print("2. 创建噪声生成器...")
    # 高斯白噪声生成器
    gaussian_noise_gen = NoiseGeneratorFactory.create_generator(
        'gaussian',
        snr_db=40,  # 1000db的高斯白噪
    )

    # 脉冲噪声生成器 (噪声率5%，椒盐比例1:1)
    impulse_noise_gen = NoiseGeneratorFactory.create_generator(
        'impulse',
        noise_ratio=0.05,  # 5%的像素被噪声污染
        salt_ratio=0.5  # 椒盐比例1:1
    )

    # 3. 添加噪声
    print("3. 添加噪声...")
    # 添加高斯白噪声
    noisy_data_gaussian = gaussian_noise_gen.add_noise(data)
    print("   高斯白噪声已添加")

    # 添加脉冲噪声
    noisy_data_impulse = impulse_noise_gen.add_noise(data)
    print("   脉冲噪声已添加")

    # 同时添加两种噪声
    noisy_data_combined = impulse_noise_gen.add_noise(noisy_data_gaussian)
    print("   组合噪声已添加")

    # 4. 创建可视化器
    print("4. 创建可视化器...")
    heatmap_visualizer = VisualizationFactory.create_visualizer('heatmap')

    # 5. 绘制热力图比较
    print("5. 绘制热力图...")

    # 创建统一的颜色范围以便比较
    all_data = [data, noisy_data_combined]
    vmin = min(np.min(d) for d in all_data) * 1e-3
    vmax = max(np.max(d) for d in all_data) * 1e-3

    # 如果数据是时间序列，创建时间轴和距离轴
    time_points, distance_points = data.shape
    time_axis = np.linspace(0, time_points * 0.001, time_points)  # 假设采样率1000Hz
    distance_axis = np.linspace(0, distance_points, distance_points)  # 假设1m间距

    # 绘制原始数据热力图
    print("   绘制原始数据热力图...")
    heatmap_visualizer.plot_heatmap(
        data,
        time_axis=time_axis,
        distance_axis=distance_axis,
        title="Original DAS Data",
        xlabel="Distance (m)",
        ylabel="Time (s)",
        vmin=vmin,
        vmax=vmax,
        colorbar_label="Amplitude",
        save_path="original_data_heatmap.png"
    )

    # 绘制添加噪声后的数据热力图
    print("   绘制添加噪声后的数据热力图...")
    heatmap_visualizer.plot_heatmap(
        noisy_data_combined,
        time_axis=time_axis,
        distance_axis=distance_axis,
        title="DAS Data with Noise (Gaussian + Impulse)",
        xlabel="Distance (m)",
        ylabel="Time (s)",
        vmin=vmin,
        vmax=vmax,
        colorbar_label="Amplitude",
        save_path="noisy_data_heatmap.png"
    )

    # 绘制多个热力图进行比较
    print("   绘制多图比较...")
    heatmap_visualizer.plot_multiple_heatmaps(
        [data, noisy_data_gaussian, noisy_data_impulse, noisy_data_combined],
        ["Original", "Gaussian Noise", "Impulse Noise", "Combined Noise"],
        time_axis=time_axis,
        distance_axis=distance_axis,
        figsize=(20, 5),
        vmin=vmin,
        vmax=vmax
    )

    # 绘制带统计信息的热力图
    print("   绘制带统计信息的热力图...")
    heatmap_visualizer.plot_heatmap_with_stats(
        noisy_data_combined,
        time_axis=time_axis,
        distance_axis=distance_axis,
        title="Noisy DAS Data with Statistics",
        xlabel="Distance (m)",
        ylabel="Time (s)",
        vmin=vmin,
        vmax=vmax,
        colorbar_label="Amplitude",
        save_path="noisy_data_with_stats.png"
    )

    print("测试完成！")
    print("生成的文件:")
    print("  - original_data_heatmap.png")
    print("  - noisy_data_heatmap.png")
    print("  - noisy_data_with_stats.png")


# def create_simulated_das_data(time_points=1000, distance_points=200):
#     """
#     创建模拟DAS数据用于测试
#
#     Args:
#         time_points (int): 时间点数
#         distance_points (int): 距离点数
#
#     Returns:
#         np.ndarray: 模拟的DAS数据
#     """
#     # 创建时间和距离轴
#     t = np.linspace(0, 10, time_points)
#     x = np.linspace(0, 100, distance_points)
#
#     # 创建网格
#     T, X = np.meshgrid(t, x, indexing='ij')
#
#     # 创建模拟信号：正弦波 + 高频噪声
#     data = np.sin(2 * np.pi * 0.5 * T) * np.exp(-0.1 * X)  # 衰减正弦波
#     data += 0.3 * np.sin(2 * np.pi * 2 * T) * np.exp(-0.05 * X)  # 高频成分
#     data += 0.1 * np.random.randn(*data.shape)  # 背景噪声
#
#     # 添加一些事件
#     event_time_idx = int(0.3 * time_points)
#     event_distance_idx = int(0.4 * distance_points)
#     data[event_time_idx:event_time_idx + 50, event_distance_idx:event_distance_idx + 20] += 2.0
#
#     return data
#
#
# def test_with_specific_parameters():
#     """
#     使用特定参数进行测试
#     """
#     print("=== 使用特定参数进行测试 ===")
#
#     # 创建模拟数据
#     data = create_simulated_das_data(500, 100)
#
#     # 创建噪声生成器
#     gaussian_noise_gen = NoiseGeneratorFactory.create_generator(
#         'gaussian',
#         snr_db=10
#     )
#
#     impulse_noise_gen = NoiseGeneratorFactory.create_generator(
#         'impulse',
#         noise_ratio=0.03,  # 3%的像素被噪声污染
#         salt_ratio=0.3  # 30%盐噪声，70%胡椒噪声
#     )
#
#     # 添加噪声
#     noisy_data_gaussian = gaussian_noise_gen.add_noise(data)
#     noisy_data_combined = impulse_noise_gen.add_noise(noisy_data_gaussian)
#
#     # 创建可视化器
#     heatmap_visualizer = VisualizationFactory.create_visualizer('heatmap')
#
#     # 统一颜色范围
#     vmin = min(np.min(data), np.min(noisy_data_combined))
#     vmax = max(np.max(data), np.max(noisy_data_combined))
#
#     # 绘制对比图
#     heatmap_visualizer.plot_multiple_heatmaps(
#         [data, noisy_data_combined],
#         ["Original Data", "Noisy Data (10dB + 3% Impulse)"],
#         figsize=(15, 6),
#         vmin=vmin,
#         vmax=vmax
#     )
#
#     print("特定参数测试完成！")


if __name__ == "__main__":
    # 测试1: 如果有真实数据文件
    test_noise_and_visualization(r"C:\Users\17981\Desktop\科研\光纤\strain_fiber_rate_model3.mat", "strain_fiber_rate")

    # # 测试2: 使用模拟数据进行测试
    # test_with_specific_parameters()

    print("\n所有测试完成！")
