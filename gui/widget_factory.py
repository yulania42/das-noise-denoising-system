# 文件位置: gui/widget_factory.py

"""
GUI组件工厂
提供统一的GUI组件创建接口，便于管理和扩展
"""

from PyQt5.QtWidgets import QWidget
from typing import Dict, Type, Any, Optional

# 导入所有GUI组件类
from .step1_file_selection import FileSelectionWidget
from .step2_noise_params import NoiseParametersWidget
from .step3_denoising_method import DenoisingMethodWidget
from .step4_image_display import ImageDisplayWidget


class WidgetFactory:
    """GUI组件工厂类"""

    # 组件注册表
    _widgets: Dict[str, Type[QWidget]] = {
        'file_selection': FileSelectionWidget,
        'noise_params': NoiseParametersWidget,
        'denoising_method': DenoisingMethodWidget,
        'image_display': ImageDisplayWidget,
    }

    @classmethod
    def register_widget(cls, name: str, widget_class: Type[QWidget]) -> None:
        """
        注册新的GUI组件

        Args:
            name: 组件名称
            widget_class: 组件类
        """
        cls._widgets[name] = widget_class

    @classmethod
    def create_widget(cls, name: str, parent: Optional[QWidget] = None, **kwargs) -> Optional[QWidget]:
        """
        创建GUI组件实例

        Args:
            name: 组件名称
            parent: 父组件
            **kwargs: 传递给组件构造函数的参数

        Returns:
            QWidget实例或None（如果未找到对应组件）
        """
        widget_class = cls._widgets.get(name)
        if widget_class:
            return widget_class(parent, **kwargs)
        return None

    @classmethod
    def get_available_widgets(cls) -> list:
        """
        获取所有可用的组件名称

        Returns:
            组件名称列表
        """
        return list(cls._widgets.keys())


# 便捷函数
def create_widget(name: str, parent: Optional[QWidget] = None, **kwargs) -> Optional[QWidget]:
    """
    创建GUI组件的便捷函数

    Args:
        name: 组件名称
        parent: 父组件
        **kwargs: 传递给组件构造函数的参数

    Returns:
        QWidget实例或None
    """
    return WidgetFactory.create_widget(name, parent, **kwargs)


def get_available_widgets() -> list:
    """
    获取所有可用的组件名称

    Returns:
        组件名称列表
    """
    return WidgetFactory.get_available_widgets()


# 使用示例（可以删除或注释掉）：
"""
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # 使用工厂创建组件
    file_widget = create_widget('file_selection')
    if file_widget:
        file_widget.show()

    noise_widget = create_widget('noise_params')
    if noise_widget:
        noise_widget.show()

    denoise_widget = create_widget('denoising_method')
    if denoise_widget:
        denoise_widget.show()

    display_widget = create_widget('image_display')
    if display_widget:
        display_widget.show()

    sys.exit(app.exec_())
"""
