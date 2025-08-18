# test_noise_generator.py
from noise_generator import NoiseGeneratorFactory
import numpy as np


def test_noise_generator():
    """测试噪声生成器"""
    print("=" * 50)
    print("噪声生成模块测试")
    print("=" * 50)

    # 创建测试数据
    test_data = np.random.randn(10, 10) * 100
    print("原始测试数据 (5x5):")
    print(test_data[:5, :5])
    print()

    try:
        # 1. 测试高斯噪声生成器
        print("1. 测试高斯噪声生成器...")
        gaussian_generator = NoiseGeneratorFactory.create_generator(
            'gaussian', mean=0.0, std=10.0, seed=42
        )

        # 添加高斯噪声 (固定标准差)
        noisy_gaussian = gaussian_generator.add_noise(test_data)
        print("   ✓ 高斯噪声添加成功")
        print("   添加高斯噪声后数据 (5x5):")
        print(noisy_gaussian[:5, :5])
        print()

        # 添加高斯噪声 (指定SNR)
        noisy_gaussian_snr = gaussian_generator.add_noise(test_data, snr_db=20)
        print("   ✓ 指定SNR的高斯噪声添加成功")
        print("   SNR=20dB时的数据 (5x5):")
        print(noisy_gaussian_snr[:5, :5])
        print()

        # 2. 测试脉冲噪声生成器
        print("2. 测试脉冲噪声生成器...")
        impulse_generator = NoiseGeneratorFactory.create_generator(
            'impulse', noise_ratio=0.1, salt_ratio=0.5, seed=42
        )

        # 添加脉冲噪声
        noisy_impulse = impulse_generator.add_noise(test_data)
        print("   ✓ 脉冲噪声添加成功")
        print("   添加脉冲噪声后数据 (5x5):")
        print(noisy_impulse[:5, :5])
        print()

        # 生成噪声掩码
        mask = impulse_generator.generate_mask(test_data.shape, noise_ratio=0.05)
        print("   ✓ 噪声掩码生成成功")
        print("   噪声掩码 (5x5):")
        print(mask[:5, :5])
        print()

        print("✓ 所有测试通过！")

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_noise_generator()
