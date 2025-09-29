from manim import *
from mobject.creature.a_creature import ACreature
from mobject.data_structure_nodes.single_node import SingleNode
from mobject.data_structure_nodes.sequential_list import SequentialList
from mobject.display_guidance.bulleted_list_brace import BulletedListBrace
from mobject.display_guidance.curved_line_builder import CurvedArrowBuilder, CurvedSingleArrow
from mobject.display_guidance.moving_code import MovingCode
from mobject.logo import AlgorithmBanner
from scene.data_structure.sequential_list_scene.sequential_list_scene import SequentialListScene
#基本测试说明
"""
    @auther 巷北
    @time 2025.9.24 23:10
        这个分支代码(branch_test)应该是存储的最新代码,比main代码还要新.代码上传基本流程是,
    branch_test -> main -> origin main.所以,不存在什么pull main,pull origin main,
    因为这里就是最新的,没问题之后,会直接merge到main中.
        这个test文件,主要是用于测试处理.每当更新完文件之后,先在main中做做测试,成功之后,直接
    将测试代码贴到这里来,然后,方便后续调试.
    ...
    @auther 巷北
    @time 2025.9.29 20:28
        代码结构更新,重新测试各包内代码, 确保路径导入正确.
"""
config.background_color = "#cee"
class ACreature_scene(Scene):
    def construct(self):

        A = ACreature()

        self.play(
            FadeIn(A)
        )
        self.wait()
        self.play(
            A.animate.blink()
        )
        self.wait()

        self.play(
            A.animate.look_at(UP)
        )
        self.wait()
        self.play(
            A.animate.look_at(DL)
        )
        self.wait()
        self.play(
            A.animate.restore_eyes()
        )
        self.wait()
        self.play(A.animate.blink())
        self.wait()

class SingleNode_scene(Scene):
    def construct(self):
        s = SingleNode()
        self.add(s)

class SequentialList_scene(Scene):
    def construct(self):
        s = SequentialList(isindex=True)
        self.add(s)

class BulletedListBrace_scene(Scene):
    def construct(self):
        b = BulletedListBrace("Item 1", "Item 2", "Item 3", "Item 4", "Item 5")
        self.add(b)

        self.play(b.animate.transform_brace())

class CurvedArrowBuilder_scene(Scene):
    def construct(self):
        c = CurvedArrowBuilder(ORIGIN, RIGHT*3, points = 4)
        self.play(Create(c))
        self.wait()
        self.play(Uncreate(c))

        self.wait()

        c = CurvedArrowBuilder(ORIGIN, RIGHT * 3, angle = - TAU / 4, curvedline_class=CurvedSingleArrow)

        self.play(Create(c))
        self.wait()
        self.play(Uncreate(c))

        self.wait()

class MovingCode_scene(Scene):
    def construct(self):
        m = MovingCode(r".\assets\showing_code\test.cpp")

        self.add(m)

        r = m.get_svg_and_rect(0)
        self.play(FadeIn(r))
        self.play(m.animate.transform(3, r))
        self.play(m.animate.transform(4, r))
        self.play(m.animate.transform(5, r))
        self.play(m.animate.transform(7, r))
        self.play(m.animate.transform(0, r))

class AlgorithmBanner_scene(Scene):
    def construct(self):
        a = AlgorithmBanner()
        self.play(Create(a))
        self.wait()
        self.play(a.animate.expand())
        self.wait()
        self.play(FadeOut(a))

class SequentialListScene_scene(SequentialListScene):
    def construct(self):
        sqlist:SequentialList[SingleNode] = self.init_sq(["3", "5", "4", "6", "7", "3"])

        print(sqlist.submobjects)
        insert_node = SingleNode("55").set_node_color(8)
        insert_node.set(height = sqlist[0].height)
        insert_node.to_edge(UP)
        self.add(insert_node)

        self.Insert_Sq(sqlist, 1, insert_node)
        print(sqlist.submobjects)

        self.wait()

        self.play(sqlist.animate.to_edge(RIGHT))
        self.play(sqlist[1].animate.move_to(UP), sqlist[2].animate.move_to(DOWN))

            
