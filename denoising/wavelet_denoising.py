# denoising/wavelet_denoising.py
import numpy as np

try:
    import pywt

    PYWT_AVAILABLE = True
except ImportError:
    PYWT_AVAILABLE = False
    print("警告: pywt库未安装，小波降噪功能不可用")


class WaveletDenoising:
    """
    小波降噪器
    用于DAS数据的小波变换降噪
    """

    def __init__(self, wavelet='db4', level=4, threshold_mode='soft', sigma_multiplier=1.0):
        """
        初始化小波降噪器

        Args:
            wavelet (str): 小波基函数名称
            level (int): 分解层数
            threshold_mode (str): 阈值模式 ('soft', 'hard')
            sigma_multiplier (float): 阈值倍数因子
        """
        if not PYWT_AVAILABLE:
            raise ImportError("pywt库未安装，请运行 'pip install PyWavelets'")

        self.wavelet = wavelet
        self.level = level
        self.threshold_mode = threshold_mode
        self.sigma_multiplier = sigma_multiplier

    def denoise(self, data, wavelet=None, level=None, threshold_mode=None):
        """
        对数据进行小波降噪

        Args:
            data (np.ndarray): 输入数据 (1D或2D数组)
            wavelet (str): 小波基函数名称
            level (int): 分解层数
            threshold_mode (str): 阈值模式

        Returns:
            np.ndarray: 降噪后的数据
        """
        if not PYWT_AVAILABLE:
            raise ImportError("pywt库未安装，请运行 'pip install PyWavelets'")

        # 使用参数或初始化值
        wavelet = wavelet if wavelet is not None else self.wavelet
        level = level if level is not None else self.level
        threshold_mode = threshold_mode if threshold_mode is not None else self.threshold_mode

        # 确保输入数据是numpy数组
        data = np.asarray(data, dtype=np.float64)

        # 根据数据维度选择处理方法
        if data.ndim == 1:
            denoised_data = self._denoise_1d(data, wavelet, level, threshold_mode)
        elif data.ndim == 2:
            denoised_data = self._denoise_2d(data, wavelet, level, threshold_mode)
        else:
            raise ValueError("不支持的数据维度，仅支持1D和2D数据")

        return denoised_data

    def _denoise_1d(self, data, wavelet, level, threshold_mode):
        """
        1D小波降噪

        Args:
            data (np.ndarray): 1D输入数据
            wavelet (str): 小波基函数
            level (int): 分解层数
            threshold_mode (str): 阈值模式

        Returns:
            np.ndarray: 降噪后的数据
        """
        # 小波分解
        coeffs = pywt.wavedec(data, wavelet, level=level)

        # 估计噪声标准差
        sigma = self._estimate_sigma(coeffs)

        # 应用阈值
        threshold = sigma * self.sigma_multiplier * np.sqrt(2 * np.log(len(data)))

        # 阈值处理
        coeffs_thresh = [coeffs[0]]  # 保留近似系数
        for i in range(1, len(coeffs)):
            if threshold_mode == 'soft':
                coeffs_thresh.append(pywt.threshold(coeffs[i], threshold, mode='soft'))
            else:
                coeffs_thresh.append(pywt.threshold(coeffs[i], threshold, mode='hard'))

        # 小波重构
        denoised_data = pywt.waverec(coeffs_thresh, wavelet)

        # 确保输出长度与输入一致
        if len(denoised_data) != len(data):
            denoised_data = denoised_data[:len(data)]

        return denoised_data

    def _denoise_2d(self, data, wavelet, level, threshold_mode):
        """
        使用真正的二维小波变换进行降噪
        替换掉原来分行列处理方法
        Args:
            data (np.ndarray): 2D输入数据
            wavelet (str): 小波基函数
            level (int): 分解层数
            threshold_mode (str): 阈值模式
        Returns:
            np.ndarray: 降噪后的数据
        """
        # 处理NaN值
        data = np.nan_to_num(data)
        # 二维小波分解
        coeffs = pywt.wavedec2(data, wavelet=wavelet, level=level)
        # 估计噪声标准差（使用最高频细节系数的中值绝对偏差）
        if len(coeffs) > 1:
            details = coeffs[1]
            mad = np.median(np.abs(np.concatenate([d.ravel() for d in details])))
            sigma = mad / 0.6745
            threshold = sigma * self.sigma_multiplier * np.sqrt(2 * np.log(data.size))
        else:
            threshold = 0
        # 阈值处理细节系数
        coeffs_thresh = [coeffs[0]]  # 保留近似系数
        for i in range(1, len(coeffs)):
            detail_tuple = tuple(
                pywt.threshold(detail, threshold, mode=threshold_mode)
                for detail in coeffs[i]
            )
            coeffs_thresh.append(detail_tuple)
        # 重构去噪数据
        denoised = pywt.waverec2(coeffs_thresh, wavelet=wavelet)
        # 裁剪到原始尺寸（小波变换可能有边界效应）
        return denoised[:data.shape[0], :data.shape[1]]

    def _estimate_sigma(self, coeffs):
        """
        估计噪声标准差（使用最高频系数）

        Args:
            coeffs (list): 小波系数列表

        Returns:
            float: 估计的噪声标准差
        """
        # 使用最高频系数估计噪声标准差
        if len(coeffs) > 1:
            detail_coeffs = coeffs[-1]  # 最高频细节系数
            sigma = np.median(np.abs(detail_coeffs)) / 0.6745
        else:
            sigma = 1.0
        return sigma

    def apply_visu_shrink(self, data, wavelet=None, level=None):
        """
        应用VisuShrink阈值方法

        Args:
            data (np.ndarray): 输入数据
            wavelet (str): 小波基函数
            level (int): 分解层数

        Returns:
            np.ndarray: 降噪后的数据
        """
        wavelet = wavelet if wavelet is not None else self.wavelet
        level = level if level is not None else self.level

        data = np.asarray(data, dtype=np.float64)

        # 计算VisuShrink阈值
        n = data.size if data.ndim == 1 else np.prod(data.shape)
        threshold = self.sigma_multiplier * np.sqrt(2 * np.log(n))

        # 应用标准小波降噪
        return self.denoise(data, wavelet, level, 'soft')

    def get_wavelet_coefficients(self, data, wavelet=None, level=None):
        """
        获取小波系数（用于分析）

        Args:
            data (np.ndarray): 输入数据
            wavelet (str): 小波基函数
            level (int): 分解层数

        Returns:
            list: 小波系数列表
        """
        if not PYWT_AVAILABLE:
            raise ImportError("pywt库未安装，请运行 'pip install PyWavelets'")

        wavelet = wavelet if wavelet is not None else self.wavelet
        level = level if level is not None else self.level

        data = np.asarray(data, dtype=np.float64)

        if data.ndim == 1:
            coeffs = pywt.wavedec(data, wavelet, level=level)
        elif data.ndim == 2:
            # 对2D数据进行分离的小波变换
            coeffs = []
            # 行方向分解
            row_coeffs = []
            for i in range(data.shape[0]):
                row_coeffs.append(pywt.wavedec(data[i, :], wavelet, level=level))
            coeffs.append(row_coeffs)
        else:
            raise ValueError("不支持的数据维度")

        return coeffs
