# data_loader/data_loader_factory.py
from .matlab_loader import MatlabLoader


class DataLoaderFactory:
    """
    数据加载器工厂
    根据文件类型创建相应的数据加载器
    """

    @staticmethod
    def create_loader(file_type, **kwargs):
        """
        创建数据加载器工厂方法

        Args:
            file_type (str): 文件类型 ('matlab', 'numpy', 等)
            **kwargs: 传递给加载器的参数

        Returns:
            DataLoader: 数据加载器实例

        Raises:
            ValueError: 不支持的文件类型
        """
        if file_type.lower() == 'matlab' or file_type.lower() == 'mat':
            return MatlabLoader(**kwargs)
        elif file_type.lower() == 'numpy' or file_type.lower() == 'npy':
            # 这里可以添加numpy加载器
            raise NotImplementedError("numpy加载器暂未实现")
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")

# 使用示例：
# loader = DataLoaderFactory.create_loader('matlab', file_path='data.mat')
