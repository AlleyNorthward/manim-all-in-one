import os
ASSETS_DIR = None

# _说明
"""
    @auther 巷北
    @time 2025.9.13 17.08
        先吃饭,待会回来写.
        在更新MovingCode的时候, 发现总是会获取svg图, 这样路径的获取就必不可少.由于刚写了渐变颜色差值装饰器, 所以
    打算写一个获取svg路径的装饰器, 这样能结合实际练习一下,理解也会更深入.
        虽然刚写了个装饰器, 但是对内部函数参数的使用并不多, 我自己对装饰器中*args及**kwargs还是有疑问的.在渐变颜色
    差值装饰器中给的解释是有些mob需要修改颜色、opacity等,会用到这里面的, 但本质, 我感觉不是这样.所以带着疑问又投入
    到写这个路径装饰器之中.
        下面两个装饰器看着简短,却也是我一直更改过后的(虽然本来就不长).一直修改的就是参数, 总是有问题.
        具体问题是, 参数调用问题.装饰器中的wrapper函数中有两处函数参数, 一个是wrapper中传入的参数,另一个是wrapper里,
    返回func中的参数.而在被装饰函数, 以及调用被装饰函数时, 也会需要传入两次参数.我的困惑点就在这,总是不对.而且我装饰的是
    方法, 并不是不是函数, 所以难度也上升了些.
        我尝试在wrapper、返回值中带有mode, 但总感觉有些奇怪.
        后来我明白了, 装饰器的作用, 其实就是a = decorator(a).
        所以wrapper中的参数, 对应的是我们实际调用时的传参, wrapper返回的函数, 则是我们编写时, 通过装饰器装饰的那个函数的
    参数.
        正如下面的例子所示, get_svg中虽然有path参数, 且没有默认值,但是调用时,我们并没有使用该函数, 实际上是使用了闭包中的
    wrapper()函数.所以调用时我们的参数只需要满足wrapper中传入参数要求即可.而get_svg()中的参数, 需要符合wrapper中返回值函
    数的要求.这也就是对应关系.
        那么装饰器1和装饰器2有什么区别吗?
        肯定有的.如果我们每次都都显式传入mode的话,装饰器1和2没区别.他俩的区别主要在于默认mode.装饰器1,默认mode是candle.而
    装饰器2提供了接口,方便我们修改默认mode.
        可能有人会说,这有啥区别.区别可大了.装饰器1只能针对于MovingCode使用,因为它一定有candle这个图, 而其他方法可能没有这
    个图, 产生问题.而装饰器2能装饰所有需要svg路径的方法, 因为提供了接口, 方便我们修改默认svg图.
"""

# _代码示例
""" 
    待装饰函数/方法.
    def get_svg(self,path, start):
        pass
        
    装饰器1:
    @svg_path
    def get_svg(self, path, start):
        pass
    
    调用:
    m = self.get_svg(0) 此时调用mode = "candle"的svg图
    m = self.get_svg(0, mode = 's') 获取名为s.svg的图像
        
    装饰器2:
    @svg_path(mode)
    def get_svg(self, path, start):
        pass
    调用:
    m = self.get_svg(0) 同上
    m = self.get_svg(0, mode = 's')同上.
"""
def svg_path(func):
    #_弃案 不具备一般性,对比学习使用.建议使用下面的

    #_代码示例
    """
            待装饰函数/方法.
            def get_svg(self,path, start):
                pass
                
            装饰器1:
            @svg_path
            def get_svg(self, path, start):
                pass
            
            调用:
            m = self.get_svg(0) 此时调用mode = "candle"的svg图
            m = self.get_svg(0, mode = 's') 获取名为s.svg的图像
    """
    def wrapper(self, *args, **kwargs):
        mode = kwargs.pop("mode", "candle")
        path = os.path.join(ASSETS_DIR, f"{mode}.svg")
        if not os.path.exists(path):
            path = os.path.join(ASSETS_DIR, "candle.svg")
        return func(self, path, *args, **kwargs)
    return wrapper



def svg_path(mode):
    #_代码示例
    """
            待装饰函数/方法.
            def get_svg(self,path, start):
                pass
                
            装饰器2:
            @svg_path(mode)
            def get_svg(self, path, start):
                pass
            调用:
            m = self.get_svg(0) 同上
            m = self.get_svg(0, mode = 's')同上.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            current_mode = kwargs.pop("mode", mode)
            path = os.path.join(ASSETS_DIR, f"{current_mode}.svg")
            if not os.path.exists(path):
                path = os.path.join(ASSETS_DIR, f"{mode}.svg")
            return func(self, path, *args,**kwargs)
        return wrapper
    return decorator
