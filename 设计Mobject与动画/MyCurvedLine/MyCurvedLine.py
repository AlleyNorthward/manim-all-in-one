from manim import(
    VMobject, TangentLine, VGroup, CurvedArrow, CurvedDoubleArrow,
    Create, FadeIn, Uncreate, Succession, FadeOut, AnimationGroup,
    MAROON, TEAL,
    DEGREES, RIGHT, DOWN, LEFT, UP,
    normalize, rotate_vector, interpolate,override_animation,
)
import numpy as np

class MyCurvedLine(VGroup):

    """
        @time:2025/9/4
        @auther:巷北
        @Updating

        更新了一下MyCurvedLine的代码, 使之更加灵活使用    
        混淆了VMobject和VGroup作用, 之前继承时总达不到预期效果, 产生问题

        VMobject产生的是路径, 其实就是一个对象, 虽然可以使用self.add()向
        内部添加元素, 但是如果想使用组合的话, 不建议这么做, 产生的问题, 你也
        在老版本的MyCurvedLine中看到了, 并不理想. 因为VMobject就是单纯创建路径
        的, 不适合组合.想要组合就继承VGroup, 这才是理想的操作方法.
    """
    def __init__(
            self,
            start,
            end,
            thickness = 0.45,
            points = 7,
            curve_color = MAROON,
            tan_length = 0.3,
            tan_color = TEAL,
            tan_degrees = 20*DEGREES,
            stroke_opacity = 0.7,
            buff = 0.05,
            **kwargs,
    ):
        self.start = start + DOWN*buff + RIGHT*buff
        self.end = end + LEFT*buff + UP*buff
        self.thickness = thickness
        self.mypoints = points
        self.curve_color = curve_color
        self.tan_length = tan_length
        self.tan_color = tan_color
        self.tan_degrees = tan_degrees
        
        super().__init__(**kwargs)

        self.curve = VMobject()
        self._generate_points(self.curve)

        self.set_color(self.curve_color)
        self.arrows = self._set_arrows()
        self.set_stroke(opacity = stroke_opacity)

    def _get_curved_points(self, start, end):
        uv = normalize(end - start)
        nv = rotate_vector(uv, 90*DEGREES) * self.thickness
        zz = [nv, -nv]

        return [
            np.array(
                interpolate(start, end, i/self.mypoints)
            ) + zz[i % 2]
            for i in range(1, self.mypoints)
        ]
    
    def _generate_points(self, curve:VMobject):
        points = self._get_curved_points(self.start, self.end)
        curve.set_points_smoothly([self.start, *points, self.end])

        self.add(curve)

    def _set_arrows(self):
        tangentline = TangentLine(self[0], 1)
        tangentline.set_length(self.tan_length)
        tangentline.rotate(-self.tan_degrees)
        tangentline.shift(tangentline.get_unit_vector()* -tangentline.get_length()/2)
        
        tangentline2 = tangentline.copy()
        tangentline2.rotate(self.tan_degrees*2 + 5*DEGREES, about_point=tangentline2.get_end())

        tan_grps = VGroup(tangentline, tangentline2)
        tan_grps.set_color(self.tan_color)
        self.add(tan_grps)

        return tan_grps
    
    def get_curved_arrows(self, isdouble = False, isflip = False, color = None, **kwargs):
        if color is None:
            color = self.curve_color
        if isdouble:
            curved_arrows = CurvedDoubleArrow(self.start, self.end, color = color, **kwargs)
            tip = curved_arrows.get_tips()
        else:
            curved_arrows = CurvedArrow(self.start, self.end, color = color, **kwargs)
            tip = curved_arrows.get_tip()

        tip.set_color(self.tan_color)
        if isflip:
            curved_arrows.flip(RIGHT)

        return curved_arrows
    
    @override_animation(Create)
    def create(self, run_time = 2,):

        return Succession(
            Create(self.curve, run_time = run_time*3/4),
            FadeIn(self.arrows, run_time = run_time/4)
        )
    
    @override_animation(FadeOut)
    def fadeout(self, run_time = 2):

        return AnimationGroup(
            Uncreate(self.curve, run_time = run_time),
            FadeOut(self.arrows, run_time = run_time)
        )
            



# 老版本, 可以对比参考, 这里就不去掉了
class MyCurvedLine(VMobject):
    def __init__(
            self,
            start,
            end,
            thickness = 0.45,
            points = 7,
            curve_color = MAROON,
            tan_length = 0.3,
            tan_color = TEAL,
            tan_degrees = 20*DEGREES,
            stroke_opacity = 0.7,
            buff = 0.05,
            **kwargs,
    ):
        self.start = start + DOWN*buff + RIGHT*buff
        self.end = end + LEFT*buff + UP*buff
        self.thickness = thickness
        self.mypoints = points
        self.curve_color = curve_color
        self.tan_length = tan_length
        self.tan_color = tan_color
        self.tan_degrees = tan_degrees
        
        super().__init__(**kwargs)

        self._generate_points()
        self.set_color(self.curve_color)
        self.arrows = self._set_arrows()
        self.set_stroke(opacity = stroke_opacity)

    def _get_curved_points(self, start, end):
        uv = normalize(end - start)
        nv = rotate_vector(uv, 90*DEGREES) * self.thickness
        zz = [nv, -nv]

        return [
            np.array(
                interpolate(start, end, i/self.mypoints)
            ) + zz[i % 2]
            for i in range(1, self.mypoints)
        ]
    
    def _generate_points(self):
        points = self._get_curved_points(self.start, self.end)
        self.set_points_smoothly([self.start, *points, self.end])

    def _set_arrows(self):
        tangentline = TangentLine(self, 1)
        tangentline.set_length(self.tan_length)
        tangentline.rotate(-self.tan_degrees)
        tangentline.shift(tangentline.get_unit_vector()* -tangentline.get_length()/2)
        
        tangentline2 = tangentline.copy()
        tangentline2.rotate(self.tan_degrees*2 + 5*DEGREES, about_point=tangentline2.get_end())

        tan_grps = VGroup(tangentline, tangentline2)
        tan_grps.set_color(self.tan_color)
        self.add(tan_grps)

        return tan_grps
    def get_curved_arrows(self, isdouble = False, isflip = False, color = None, **kwargs):
        if color is None:
            color = self.curve_color
        if isdouble:
            curved_arrows = CurvedDoubleArrow(self.start, self.end, color = color, **kwargs)
            tip = curved_arrows.get_tips()
        else:
            curved_arrows = CurvedArrow(self.start, self.end, color = color, **kwargs)
            tip = curved_arrows.get_tip()

        tip.set_color(self.tan_color)
        if isflip:
            curved_arrows.flip(RIGHT)

        return curved_arrows
    
    def create(self, run_time = 2,):
        self.remove(self.arrows) # 危险操作!  
            
        animation1 = Create(self, run_time = run_time*3/4),
        animation2 = FadeIn(self.arrows, run_time = run_time/4)
        s = Succession(animation1, animation2)
        return s
    
    def fadeout(self, run_time = 2):

        return AnimationGroup(
            Uncreate(self, run_time = run_time),
            FadeOut(self.arrows, run_time = run_time)
        )



