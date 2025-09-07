from manim import (
    Mobject, 
    ORIGIN,
    np,
)
from manim.typing import Point3DLike, Vector3D

def set_position(
        self, 
        point_or_mobject: Point3DLike | Mobject, 
        anchor = ORIGIN,
        coor_mask: Vector3D = np.array([1, 1, 1]),
):
    """
        整体思想:manim本身有锚点思想, 不过是贝塞尔曲线
        中的思想, 我这里的锚点是移动参考点.一般的移动参考点
        是mob的中心点, 但是manim并没有直接提供更换移动
        参考点的接口, 所以我理解了一下move_to的实现原理,
        发现mob.get_critical_point()有转换参考点的意思,
        所以在此基础之上, 重新写了这个方法.

        可以直接添加到Mobject中, 但是比较危险, 
        更新、换版本时, 就无法使用.为了安全性
        以及写起来舒服些, 最好在全局添加下面语句
        Mobject.set_position = set_position
        从而使之能够像下面代码示例中一样访问.
        当然, 我们也可以直接当做函数使用, 但有失manim编写特性.

        锚点(也就是移动参考点)一共有9个, 对应着mob的9个方向
        (ORIGIN, UP ,DOWN, LEFT, RIGHT, UL, UR, DL, DR)
        默认是ORIGIN, 当移动时, 如果想转换锚点的话, 可以选择
        上面的9个锚点, 从而使移动更加灵活.

        编写示例:
            Mobject.set_position = set_position
            
            class Example(Scene):
                def construct(self):
                    s = Square()
                    square = Square().scale(3)
                    self.add(square)
                    self.play(s.animate.set_position(square.get_corner(UL), UL))
                    
        这个动画虽然直接使用move_to() shift()等也能实现, 
        但是我这里直接转换锚点, 就能直接实现.这样做的另一
        个好处是, 可以使用矩形任意划分屏幕,  且能够更加
        灵活的移动.
    """
    if isinstance(point_or_mobject, Mobject):
        target = point_or_mobject.get_center()
    else:
        target = point_or_mobject
    
    move_mob = self.get_critical_point(anchor)
    self.shift((target - move_mob) * coor_mask)
    return self

