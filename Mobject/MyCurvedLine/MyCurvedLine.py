from manim import(
    VMobject, TangentLine, VGroup, CurvedArrow,
    Create, FadeIn, Uncreate, Succession, FadeOut, AnimationGroup,Uncreate,
    MAROON, TEAL,
    DEGREES, RIGHT, DOWN, LEFT, UP,
    normalize, rotate_vector, interpolate,
    override_animation,
    PI
)
import numpy as np

#_修改日志
"""
    @auther 巷北
    @time 2025.9.14
    将线条路径换为VGroup,便于访问路径
    去除多余不必要属性
    去除get_curved_arrows()中flip()
    使用Create、Uncreate, 替换了普通的create、fadeout
    将get_curved_arrows()设为静态方法(修改的少,没必要分离,但与本体也要有区分)
    给get_curved_arrows()添加angle,灵活调整方向
    将get_curved_arrows()更名为init_curves_arrows并做出较大改变
    增添iscurvedarrows判断参数接口, 提升性能.
"""

class MyCurvedLine(VGroup):
    
#_代码示例
"""
    class Example(Scene):
        def construct(self):
            m = MyCurvedLine(LEFT*3+UP*2.21, DOWN*2+ RIGHT*2.3, points = 4)
            self.add(m)

    class Example(Scene):
        def construct(self):
            m = MyCurvedLine(LEFT*3+UP*2.21, DOWN*2+ RIGHT*2.3, points = 4)
            m.init_curved_arrows()
            self.add(m)

    class Test(Scene):
        def construct(self):
            m = MyCurvedLine(LEFT*3+UP*2.21, DOWN*2+ RIGHT*2.3, iscurvedarrows = True)
            self.add(m)
"""
    def __init__(
            self,
            start,
            end,
            points = 7,
            thickness = 0.45,
            curve_color = MAROON,
            tan_length = 0.3,
            tan_color = TEAL,
            tan_degrees = 20*DEGREES,
            stroke_opacity = 0.7,
            buff = 0.05,
            iscurvedarrows = False,
            angle = PI/2,
            **kwargs,
    ):
        self.start = start + DOWN*buff + RIGHT*buff
        self.end = end + LEFT*buff + UP*buff
        
        super().__init__(**kwargs)

        if iscurvedarrows:
            self.init_curved_arrows(start, end, angle, curve_color, tan_color)

        else:
            self.path = self._generate_points(start, end, curve_color, thickness, points)
            self.arrows = self._set_arrows(tan_length, tan_degrees, tan_color)
            self.set_stroke(opacity = stroke_opacity)


    def _get_curved_points(
            self, 
            start, 
            end, 
            thickness, 
            points
    ):
        uv = normalize(end - start)
        nv = rotate_vector(uv, 90*DEGREES) * thickness
        zz = [nv, -nv]

        return [
            np.array(
                interpolate(start, end, i/ points)
            ) + zz[i % 2]
            for i in range(1, points)
        ]
    
    def _generate_points(
            self, 
            start, 
            end, 
            curve_color, 
            thickness, 
            _points,
    ):
        points = self._get_curved_points(start, end, thickness, _points)
        path = VMobject().set_points_smoothly([start, *points, end])
        path.set_color(curve_color)

        self.add(path)
        return path
        
    def _set_arrows(
            self, 
            tan_length, 
            tan_degrees, 
            tan_color
    ):
        tangentline = TangentLine(self.path, 1)
        tangentline.set_length(tan_length)
        tangentline.rotate(-tan_degrees)
        tangentline.shift(tangentline.get_unit_vector()* -tangentline.get_length()/2)
        
        tangentline2 = tangentline.copy()
        tangentline2.rotate(tan_degrees*2 + 5*DEGREES, about_point=tangentline2.get_end())

        tan_grps = VGroup(tangentline, tangentline2)
        tan_grps.set_color(tan_color)
        self.add(tan_grps)

        return tan_grps
    
    @override_animation(Create)
    def _create(self, run_time = 2,):
        self.remove(self.arrows) # 危险操作!  
            
        animation1 = Create(self.path, run_time = run_time*3/4),
        animation2 = FadeIn(self.arrows, run_time = run_time/4)
        s = Succession(animation1, animation2)
        return s
    
    @override_animation(Uncreate)
    def _fadeout(self, run_time = 2):

        return AnimationGroup(
            Uncreate(self.path, run_time = run_time),
            FadeOut(self.arrows, run_time = run_time)
        )
    
    def init_curved_arrows(
            self,
            start = None,
            end = None,
            angle = PI/2,
            curve_color = MAROON, 
            tan_color = TEAL, 
            buff = 0.05,
            **kwargs
    ):
        # _说明
        """
                经过一系列的修改后, 发现双曲线似乎没用了.所以直接去掉了.
            后续有用的时候再创建吧.
                单独这么初始化,是为了共用一个Create与UnCreate,提高复用性.
        """
        if start is None:
            start = self.start
        else:
            start = start + DOWN*buff + RIGHT*buff
        if end is None:
            end = self.end
        else:
            end = end + LEFT*buff + UP*buff

        curved_arrows = CurvedArrow(start, end, color = curve_color, angle = angle, **kwargs)
        tip = curved_arrows.get_tip()

        tip.set_color(tan_color)


        #_待优化
        """
            不知道这么弄是否合理.
            只要有become就可以了.但是self.submobjects没有更新, 不过并不影响使用.
            这里其他的代码是为了更新self.submobjects而写的.
            可以测试一下self.add(self.path)与self.add(self.arrows),会发现并未更新.

            _已解决
            重新更改了架构.可以直接创建,但仍旧保留了接口,使得用户可以创建本身的curved_
            line后,还能更换成curved_arrows.但替换逻辑还是使用的上述待优化逻辑.
        """
        curved_arrows.remove(tip)

        if hasattr(self, "path"):
            self.remove(self.path)
            self.path.become(curved_arrows)
        else:
            self.path = curved_arrows

        if hasattr(self, "arrows"):
            self.remove(self.arrows)
            self.arrows.become(tip)
        else:
            self.arrows = tip

        self.add(curved_arrows)
        self.add(tip)






