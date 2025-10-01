import os
from pathlib import Path
ASSETS_DIR = None

def svg_path(mode, dir_name, i):
    #_代码示例
    """
            待装饰函数/方法.
            def get_svg(self,path, start):
                pass
                
            装饰器2:
            @svg_path(mode, dir_name)
            def get_svg(self, path, start):
                pass
            调用:
            m = self.get_svg(0) 同上
            m = self.get_svg(0, mode = 's')同上.
    """
    ASSETS_DIR = Path(__file__).resolve().parents[i] / "assets" / dir_name
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            current_mode = kwargs.pop("mode", mode)
            path = os.path.join(ASSETS_DIR, f"{current_mode}.svg")
            if not os.path.exists(path):
                path = os.path.join(ASSETS_DIR, f"{mode}.svg")
            return func(self, path, *args,**kwargs)
        return wrapper
    return decorator
