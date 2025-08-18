# test_data_loader.py
from data_loader import DataLoaderFactory
import numpy as np


def test_data_loader():
    """测试数据加载器"""
    print("=" * 50)
    print("数据加载模块测试")
    print("=" * 50)

    try:
        # 1. 测试工厂创建加载器
        print("1. 测试工厂创建MATLAB加载器...")
        loader = DataLoaderFactory.create_loader('matlab', file_path=r"C:\Users\17981\Desktop\科研\光纤\strain_fiber_rate_model3.mat")
        print("   ✓ 工厂创建加载器成功")

        # 2. 测试加载数据
        print("2. 测试加载数据...")
        data, metadata = loader.load_data()
        print("   ✓ 数据加载成功")
        print(f"   加载数据形状: {data.shape}")

        # 3. 测试数据信息获取
        print("3. 测试获取数据信息...")
        info = loader.get_data_info()
        print("   ✓ 数据信息获取成功")
        print(f"   数据类型: {info['dtype']}")
        if info['min_value'] is not None and info['max_value'] is not None:
            print(f"   数据范围: [{info['min_value']:.2f}, {info['max_value']:.2f}]")
        print()

        # 4. 输出前5行前5列数据
        print("4. 输出前5行前5列数据:")
        print("-" * 30)
        if isinstance(data, np.ndarray) and len(data.shape) >= 2:
            print(data[:5, :5])
        elif hasattr(data, '__getitem__'):
            print("数据内容:")
            print(data)
        else:
            print(f"数据类型: {type(data)}")
            print(f"数据内容: {data}")
        print("-" * 30)

        # 5. 输出元数据
        print("5. 元数据信息:")
        print("-" * 30)
        for key, value in metadata.items():
            print(f"   {key}: {value}")
        print("-" * 30)

        print("\n✓ 所有测试通过！")

    except FileNotFoundError:
        print("❌ 错误: 找不到文件 'das_data.mat'")
        print("   请确保文件路径正确，或修改测试文件中的文件路径")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    test_data_loader()
