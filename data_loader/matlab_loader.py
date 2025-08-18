# data_loader/matlab_loader.py
import scipy.io
import numpy as np
import os
from utils.file_utils import check_file_exists


class MatlabLoader:
    """
    MATLAB数据加载器
    支持加载.mat文件中的DAS数据
    """

    def __init__(self, file_path=None):
        """
        初始化MATLAB加载器

        Args:
            file_path (str): MATLAB文件路径
        """
        self.file_path = file_path
        self.data = None
        self.metadata = None

    def load_data(self, file_path=None, variable_name=None):
        """
        加载MATLAB数据文件

        Args:
            file_path (str): 文件路径
            variable_name (str): 要加载的变量名

        Returns:
            tuple: (data, metadata) 数据和元数据
        """
        if file_path is not None:
            self.file_path = file_path

        if not check_file_exists(self.file_path):
            raise FileNotFoundError(f"文件不存在: {self.file_path}")

        try:
            # 加载.mat文件
            mat_data = scipy.io.loadmat(self.file_path)

            # 如果指定了变量名，直接加载该变量
            if variable_name:
                if variable_name in mat_data:
                    self.data = mat_data[variable_name]
                else:
                    raise KeyError(f"变量 '{variable_name}' 在文件中不存在")
            else:
                # 自动查找数据变量（排除MATLAB内部变量）
                data_vars = {k: v for k, v in mat_data.items()
                             if not k.startswith('__') and not k.endswith('__')}
                if len(data_vars) == 1:
                    self.data = list(data_vars.values())[0]
                elif len(data_vars) > 1:
                    # 如果有多个变量，返回字典形式
                    self.data = data_vars
                else:
                    raise ValueError("文件中没有找到有效的数据变量")

            # 提取元数据
            self.metadata = self._extract_metadata(mat_data)

            return self.data, self.metadata

        except Exception as e:
            raise Exception(f"加载MATLAB文件失败: {str(e)}")

    def _extract_metadata(self, mat_data):
        """
        从MATLAB文件中提取元数据

        Args:
            mat_data (dict): 加载的MATLAB数据

        Returns:
            dict: 元数据字典
        """
        metadata = {
            'file_path': self.file_path,
            'file_size': os.path.getsize(self.file_path) if self.file_path else 0,
            'variables': list(mat_data.keys()),
            'data_shape': self.data.shape if hasattr(self.data, 'shape') else None,
            'data_type': type(self.data).__name__
        }
        return metadata

    def get_data_info(self):
        """
        获取数据信息

        Returns:
            dict: 数据信息
        """
        if self.data is None:
            return None

        info = {
            'shape': self.data.shape if hasattr(self.data, 'shape') else None,
            'dtype': self.data.dtype if hasattr(self.data, 'dtype') else None,
            'min_value': np.min(self.data) if isinstance(self.data, np.ndarray) else None,
            'max_value': np.max(self.data) if isinstance(self.data, np.ndarray) else None
        }
        return info
