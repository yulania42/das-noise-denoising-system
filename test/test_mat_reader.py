# test_mat_reader.py
import scipy.io as sio
import numpy as np

file_path=r"C:\Users\17981\Desktop\科研\optic_code\new_denoise\docs\strain_fiber_rate_model3.mat"
def test_mat_file(file_path):
    try:
        mat_data = sio.loadmat(file_path)
        print("文件加载成功！")
        print("变量列表:")
        for key in mat_data.keys():
            if not key.startswith('__'):
                var_data = mat_data[key]
                if isinstance(var_data, np.ndarray):
                    print(f"  {key}: shape={var_data.shape}, dtype={var_data.dtype}")
                else:
                    print(f"  {key}: type={type(var_data)}")
    except Exception as e:
        print(f"加载失败: {e}")

# 使用方法
test_mat_file(file_path)
