from manim import(
    Code, Rectangle, SVGMobject, VGroup,
    Transform, AnimationGroup,
    RIGHT, LEFT, UP, DOWN,
    YELLOW,
    override_animate
)
from utils.路径装饰器 import svg_path  #! 注意路径修改

# _修改日志
"""
    ...
    @auther 巷北
    @time 2025.9.13
    增添路径装饰器,修改get_svg获取图像方式.
    去除多余注释.
    修复get_rect中的bug(start = 0, 不在对应位置上)
    添加get_svg_and_rect()方法.
    将get_svg_and_rect()中获取的svg与rect加入到MovingCode的submobjects中,不过get_svg,get_rect仍未添加.#_弃案 rect添加到self中, 移动存在bug,建议不要添加
    更改了transform_both_svg_and_rectangle()的调用方式,通过接口transform以及.animate访问
    给transform_svg()以及transform_remark_rectangle()添加了装饰器,通过.animate访问,使得其逻辑性更强.动画要么通过动画类产生,要么通过.animate生成.
    将get_svg()重命名为_init_svg(),并新定义get_svg(),返回_init_svg()(因为被装饰器修饰后, 无法直接访问mode, 而是通过path获取的.其实是私有方法,不如添加接口.)
    增添了代码示例
    ...
"""
#! 经过测试,无法将svg、rect添加到self中,以后也别做尝试了.需要注意的是, 最后再去创建移动对象,要不然移动code后,移动对象不还在原处.
#_解决方法 想了想,只是在scale、move、next_to、align_to等中存在问题, 那我们可以重写一下这些方法.以前也没重写过,可以尝试一下.

#_待办
"""
    后续可以使用cycler,随着移动自动变换svg.
"""
class MovingCode(Code):

    # _说明
    """
        @auther 巷北
        @time 2025.9.13 21.42
            将原本的代码更新了一下, 老版本(虽然过去不到一个月)代码, 是在当时深入没多久写的, 
        虽能用, 但是整体架构上有些混乱. 
            按照如今的理解, 又重新梳理了下结构, 虽然功能一样,但是更加清晰、具体了.实际中,更
        多的是svg以及rect的结合使用,所以拓展了一下,可以直接获取二者对象,并且能直接移动二者.
            总之, 更新后的代码更加健壮、逻辑更加清晰.
    """
    # _属性
    """
        mode                                    svg的样式
    """

    # _私有方法
    """
        _init_svg()                         本来是get_svg()后面被装饰后无法直接获取mode属性, 还需要切割路径.想了想设为私有方法,提供接口访问吧.
        _transform_remark_rectangle()       下面的三个都是老版本的转换方式,直接通过.访问.不过我觉得,mainm中动画部分,要么是动画类,要么是.animate
        _transform_svg()                    访问,直接通过mobject返回方法架构上太混乱,逻辑不清晰.所以就添加了装饰器,使得通过.animate访问,这样我们
        _transform_both_svg_and_rectangle() 在使用的时候就知道,这是播放的动画,而不是其他的东西了.
    """
    
    #_公有方法
    """
        get_code_param()                    老版本静态方法,访问参数列表
        get_cpp_stycle()                    获取适合cpp代码风格样式.类方法
        get_mode()

        get_rect()
        get_svg()                           _init_svg()接口方法,容易获取mode属性
        get_svg_and_rect()
        transform_svg()
        transform_rect()
        transform()
    """

    #_代码示例
    """
        class Example(Scene):
            def construct(self):
                m = MovingCode('test.cpp')
                self.add(m)
                movingcode = m.get_svg_and_rect(0, 'light')
                self.add(movingcode)
                self.play(m.animate.transform(3, movingcode))
                self.play(m.animate.transform(5, movingcode))
                self.play(m.animate.transform(7, movingcode))
                self.play(m.animate.transform(0, movingcode))
    """
    def __init__(
            self,
            code_file = None,
            formatter_style = None,
            background = None,
            line_numbers_from = None,
            **kwargs,
    ):
        if formatter_style is None:
            formatter_style = 'material'
        if background is None:
            background = 'window'
        if line_numbers_from is None:
            line_numbers_from = 1

        super().__init__(
            code_file=code_file,
            formatter_style=formatter_style,
            background=background,
            line_numbers_from=line_numbers_from,
            **kwargs
        )
        self.remark_line_props = { 
        "fill_opacity":0.2,
        "stroke_opacity":0,
        "stroke_width":0,
    }
        
    @staticmethod
    def get_code_param():
        return [
            "code_file",
            "formatter_style = material",
            "background",
            "line_numbers_from:默认显示第一行,添加可以修改默认行数",
        ]
    
    def get_rect(self,start,end = None,color = YELLOW,include_numbers = True):
        buff = 0.1

        if start == 0:
            start = 1

        if end is None:  #_已解决 一开始这一句代码在上一行代码前面,导致start为0的时候,rect不在0的位置上
            end = start 

        if end < start:
            start, end = end, start

        start = start - 1
        end = end
        rect = Rectangle(color = color,**self.remark_line_props)

        if include_numbers:
            left = self[1].get_left()[0]
        else:
            left = self[2].get_left()[0]
        right = self[0].get_right()[0]
        
        height = self[1][start:end].height + buff

        rect.stretch_to_fit_width(right - left)
        rect.stretch_to_fit_height(height)

        rect.move_to(self[2][start:end].get_center())
        rect.align_to(self,RIGHT)
        rect.align_to(self[1][start:end],UP)
        rect.shift(UP*buff/2)

        # todo 后续使用时,注意是否需要将rect添加入self
        # _弃案 不需要添加
        return rect
    
    @svg_path("flower", "MovingCode")
    def _init_svg(self,path, start):

        svg = SVGMobject(path)
        svg.scale(0.2)
        if start == 0:
            start = 1

        start = start - 1
        width = self[0].width
        svg.move_to(self[1][start].get_center())
        svg.shift(RIGHT*width)
        svg.shift(LEFT*0.2)

        # todo 后续使用时,注意是否需要将svg添加到self中. 
        # _弃案 不需要添加到self中
        return svg
    
    def get_svg(self, start, mode = 'flower'):
        self.mode = mode
        return self._init_svg(start, mode = mode)
    
    def transform_rect(self, start,rmk, end = None):
        rect = self.get_rect(start,end)
        rect.match_style(rmk)
        return rect

    @override_animate(transform_rect)
    def _transform_remark_rectangle(self,start, rmk, end = None, **anim_kwargs):
        new_rect = self.transform_rect(start, rmk, end)
        return Transform(rmk, new_rect, **anim_kwargs)
    
    def transform_svg(self, start, svg):
        return self.get_svg(start, mode = self.mode)

    @override_animate(transform_svg)
    def _transform_svg(self, start, svg:SVGMobject, **anim_kwargs):
        new_svg = self.transform_svg(start, svg)
        return Transform(svg, new_svg, **anim_kwargs)
    
    def get_svg_and_rect(self, start, mode = 'flower'):
        svg = self.get_svg(start, mode = mode)
        rect = self.get_rect(start)

        grps = VGroup(svg, rect)
        # self.add(grps) # _弃案 加入组后,transform会存在问题
        return grps
    
    def transform(self, start, svg_rect):
        return svg_rect
    
    @override_animate(transform)
    def _transform_both_svg_and_rectangle(self, start, svg_rect,**anim_kwargs):
        svg, rmk = self.transform(start, svg_rect)
        return AnimationGroup(
            self.animate.transform_svg(start, svg),
            self.animate.transform_rect(start, rmk),
            **anim_kwargs
        )
    
    @classmethod
    def get_cpp_stycle(cls):
        return "monokai"
    
    def get_mode(self):
        if hasattr(self, "mode"):
            return self.mode
        return None
    
