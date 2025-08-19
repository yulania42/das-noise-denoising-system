DAS数据添加噪音、降噪一体化处理系统
🧪 适用于DAS（分布式声学传感）原始数据添加可控噪音、进行降噪处理并分析效果的一体化Python系统

✨ 支持多种噪声和多个降噪算法，并计算图像相似性指标与可视化对比图

📦 模块化设计，易于扩展

📌 项目概述
本项目实现了从加载DAS数据、加噪、降噪、指标评估到可视化的完整流程。

主要功能如下：

读取 .mat 文件形式的 DAS 数据
添加高斯白噪声或脉冲噪声
使用如下降噪方法处理噪声数据：
高斯滤波
移动平均
中值滤波
小波变换降噪 (VisuShrink)
双边滤波
计算图像质量指标（PSNR、SSIM、相对误差）
绘制热力图并展示对比效果
📁 目录结构
<TEXT>
├── data_loader/                  # 加载数据（如 matlab 数据）
├── noise_generator/              # 生成不同类型噪声
├── denoising/                    # 各类降噪方法
├── metrics/                      # 图像质量评估指标计算
├── visualization/                # 热力图与比较图绘制工具
├── utils/                        # 工具函数（如有需要）
├── test/                         # 单元测试与样例脚本
├── output/                       # 输出结果示例图或日志
├── main.py                       # 主程序入口
└── README.md                     # 本文档
⚙️ 安装说明
前置依赖
Python 3.8+
NumPy, SciPy, Matplotlib, scikit-image, PyWavelets
你可以通过以下命令安装依赖：

<BASH>
pip install numpy scipy matplotlib scikit-image PyWavelets
🚀 使用方法
运行主程序：

<BASH>
python main.py
在 main.py 中可以按需配置以下内容：

输入 .mat 文件路径
选择噪声类型与参数（SNR / 噪声比例）
选择降噪方法与参数
指定输出图像保存位置
🔧 示例配置请查看 test/ 目录中提供的测试脚本

🧪 测试案例
该系统附带测试脚本，以验证核心模块功能正确性：

文件名	功能
test_data_loader.py	测试数据加载器
test_noise_generator.py	测试噪声生成器
test_noise_visualization.py	测试绘图功能（单图与对比图）
🧱 模块架构说明
请查阅 /docs/readme.docx 获取详细的模块接口与类方法定义文档。

或参考源代码中各工厂方法及其实现类以获取完整说明。

✒️ 作者
yulania

最新更新时间：2025年8月18日

