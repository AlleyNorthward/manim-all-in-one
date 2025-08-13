from manim import(
    Code, Rectangle, SVGMobject, 
    Transform, 
    RIGHT, LEFT, UP, DOWN,
    YELLOW
)
class MovingCode(Code):
    total_svg = [
        r".\灯.svg",
        r".\粉色小花.svg",
        r".\蜡烛.svg",
        r".\男生小手.svg"
    ]
    """
        难免不会有bug.
        整体思想是,想怎么移动就怎么移动,目前来看,似乎达到了目标.


        代码示例
        '''
        class Test(Scene):
            def construct(self):
                code = MovingCode(code_file = 'example.py', formatter_style='material',background='window')
                code.scale(0.8)
                rect = code.get_rect(4,color = BLUE)
                self.add(code,rect)
                self.play(code.transform_remark_rectangle(rect,6),run_time = 2)
                self.wait()
        '''
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
        self.remark_line_props = {  # 默认参数.
        "fill_opacity":0.2,
        "stroke_opacity":0,
        "stroke_width":0,
    }
        
    @staticmethod
    def get_code_param():
        # 由于会继承Code,而**kwargs不会显示,故提供接口,忘了可以查看参数.
        return [
            "code_file",
            "formatter_style = material",
            "background",
            "line_numbers_from:默认显示第一行,添加可以修改默认行数",
        ]
    
    def get_rect(self,start,end = None,color = YELLOW,include_numbers = True):
        buff = 0.1


        # 考虑到可以传入一个参数start,代表展示一行,所以这么弄.
        if end is None:
            end = start 

        # 我们目的是展示start行,end行,所以如果start为0,修改为1
        if start == 0:
            start = 1

        # 如果end 大于 start, 转换一下
        if end < start:
            start, end = end, start

        # 为了使start能从1开始,所以做了-1处理
        start = start - 1
        end = end
        rect = Rectangle(color = color,**self.remark_line_props)

        # 是否覆盖数字,整体宽度为 right - left
        if include_numbers:
            left = self[1].get_left()[0]
        else:
            left = self[2].get_left()[0]
        right = self[0].get_right()[0]
        
        # 获取高度.代码片段是VGroup,通过切片获取目标代码段
        height = self[1][start:end].height + buff

        # 修改高度宽度.
        rect.stretch_to_fit_width(right - left)
        rect.stretch_to_fit_height(height)

        # 移动位置,使得其能到目标位置.
        rect.move_to(self[2][start:end].get_center())
        rect.align_to(self,RIGHT)
        rect.align_to(self[1][start:end],UP)
        rect.shift(UP*buff/2)

        return rect

    def get_svg(self,start, svg:SVGMobject, istransform = False):
        # 只能展示一行, 无法展示多行
        if not istransform:
            svg.scale(0.2)
        if start == 0:
            start = 1
        start = start - 1
        
        width = self[0].width
        svg.move_to(self[1][start].get_center())
        svg.shift(RIGHT*width)
        svg.shift(LEFT*0.2)
        return svg


    def transform_remark_rectangle(self,rmk,start,end = None):
        new_rect = self.get_rect(start,end)
        new_rect.match_style(rmk)
        return Transform(rmk,new_rect)
    
    def transform_svg(self,svg:SVGMobject, start):
        new_svg = self.get_svg(start,svg.copy(), istransform=True)
        return Transform(svg, new_svg)