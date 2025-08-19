# test/test_wavelet.py

import os
import numpy as np
from data_loader.data_loader_factory import DataLoaderFactory
from noise_generator.noise_factory import NoiseGeneratorFactory
from denoising.denoising_factory import DenoisingFactory
from metrics.metrics_factory import MetricsFactory
from visualization.visualization_factory import VisualizationFactory

def test_noise_visualization():
    # ========== 参数设置 ==========
    mat_file_path = r"C:\Users\17981\Desktop\科研\光纤\strain_fiber_rate_model3.mat"  # 请更换为你实际的 .mat 文件路径
    variable_name = "strain_fiber_rate"                # 你.mat文件中包含DAS数据的变量名
    output_dir = os.path.join("output", "png_test_noise_visualization")
    os.makedirs(output_dir, exist_ok=True)

    # ========== 1. 数据加载 ==========
    loader_factory = DataLoaderFactory()
    loader = loader_factory.create_loader("matlab")
    data, metadata = loader.load_data(mat_file_path, variable_name)
    print("原始数据形状:", data.shape)

    # ========== 2. 添加噪声 ==========
    # 高斯噪声 SNR=40dB
    gaussian_noise_gen = NoiseGeneratorFactory().create_generator("gaussian")
    noisy_gaussian = gaussian_noise_gen.add_noise(data, snr_db=60)

    # 脉冲噪声 较弱 (noise_ratio=0.02 表示噪声比例为2%，salt_ratio默认为0.5)
    impulse_noise_gen = NoiseGeneratorFactory().create_generator("impulse")
    noisy_impulse = impulse_noise_gen.add_noise(noisy_gaussian, noise_ratio=0.01, salt_ratio=0.25)

    # 合成最终噪音数据
    noisy_data = noisy_impulse.copy()

    # ========== 3. 小波降噪 ==========
    denoiser = DenoisingFactory().create_denoiser("wavelet", wavelet='db4', level=3, threshold_mode='soft')
    denoised_data = denoiser.denoise(noisy_data, wavelet='db4', level=1, threshold_mode='soft')

    # ========== 4. 指标计算 ==========
    psnr_calculator = MetricsFactory().create_calculator("psnr")
    ssim_calculator = MetricsFactory().create_calculator("ssim")
    rel_error_calculator = MetricsFactory().create_calculator("relative_error")

    psnr_value = psnr_calculator.calculate(data, denoised_data)
    ssim_value = ssim_calculator.calculate(data, denoised_data)
    rel_error = rel_error_calculator.calculate(data, denoised_data)

    print(f"PSNR: {psnr_value:.2f} dB")
    print(f"SSIM: {ssim_value:.4f}")
    print(f"Relative Error: {rel_error:.4f}")

    # ========== 5. 可视化 & 输出 ==========
    visualizer = VisualizationFactory().create_visualizer("heatmap")

    time_axis = np.arange(data.shape[0])  # 假设第一维是时间轴
    distance_axis = np.arange(data.shape[1])  # 第二维是距离轴

    vmin_raw = data.min()*1e-3
    vmax_raw = data.max()*1e-3
    stats_text = f"PSNR={psnr_value:.2f}dB\nSSIM={ssim_value:.4f}\nRel.Err={rel_error:.4f}"

    # ----(a) 原始图像----
    fig1, ax1 = visualizer.plot_heatmap_with_stats(
        data, time_axis, distance_axis,
        title="Original Data",
        show_stats=False,
        vmin=vmin_raw,
        vmax=vmax_raw,
    )
    fig1.savefig(os.path.join(output_dir, "original_data_heatmap.png"), dpi=200, bbox_inches='tight')
    print("Saved: original_data_heatmap.png")

    # ----(b) 加噪图像----
    fig2, ax2 = visualizer.plot_heatmap_with_stats(
        noisy_data, time_axis, distance_axis,
        title="Noisy Data (Gaussian + Impulse)",
        show_stats=False,
        vmin=vmin_raw,
        vmax=vmax_raw,

    )
    fig2.savefig(os.path.join(output_dir, "noisy_data_with_stats.png"), dpi=200, bbox_inches='tight')
    print("Saved: noisy_data_with_stats.png")

    # ----(c) 降噪图像+统计----
    fig3, ax3 = visualizer.plot_heatmap_with_stats(
        denoised_data, time_axis, distance_axis,
        title="Denoised Data (Wavelet)",
        show_stats=False,
        additional_text=stats_text,
        vmin=vmin_raw,
        vmax=vmax_raw,
    )
    fig3.savefig(os.path.join(output_dir, "denoised_data_with_stats.png"), dpi=200, bbox_inches='tight')
    print("Saved: denoised_data_with_stats.png")

    # ----(d) 多图对比----
    fig4, axes = visualizer.plot_multiple_heatmaps(
        data_list=[data, noisy_data, denoised_data],
        titles=["Original", "Noisy", "Denoised"],
        time_axis=time_axis,
        distance_axis=distance_axis,
        figsize=(15, 4),
        vmax=vmax_raw,
        vmin=vmin_raw,
    )

    # 在每张子图添加相应统计信息
    axes[0].text(0.02, 0.98, "Original", transform=axes[0].transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))

    axes[1].text(0.02, 0.98, "Noisy", transform=axes[1].transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))

    axes[2].text(0.02, 0.98, stats_text, transform=axes[2].transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))

    fig4.suptitle("Data Comparison: Original vs Noisy vs Denoised", y=1.02, fontsize=14)
    fig4.savefig(os.path.join(output_dir, "comparison_heatmaps.png"), dpi=200, bbox_inches='tight')
    print("Saved: comparison_heatmaps.png")

if __name__ == "__main__":
    test_noise_visualization()
