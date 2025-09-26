from manim import *
from package.MovingCode.MovingCode import MovingCode
from package.ACreature.ACreature import ACreature
from package.AlgorithmBanner.AlgorithmBanner import AlgorithmBanner
from package.BulletedListBrace.BulletedListBrace import BulletedListBrace
from package.data_structure_nodes.SequentialList import SequentialList, SingleNode
from package.MyCurvedLine.MyCurvedLine import MyCurvedLine

#基本测试说明
"""
    @auther 巷北
    @time 2025.9.24 23:10

        这个分支代码(branch_test)应该是存储的最新代码,比main代码还要新.代码上传基本流程是,
    branch_test -> main -> origin main.所以,不存在什么pull main,pull origin main,
    因为这里就是最新的,没问题之后,会直接merge到main中.
        这个test文件,主要是用于测试处理.每当更新完文件之后,先在main中做做测试,成功之后,直接
    将测试代码贴到这里来,然后,方便后续调试.
"""

class MovingCode_scene(Scene):
    def construct(self):
        m = MovingCode(r"assets\showing_code\test.cpp")
        mm = m.get_svg_and_rect(0)
        self.add(m, mm)
        self.play(m.animate.transform(3, mm))
        self.play(m.animate.transform(5, mm))


class ACreature_scene(Scene):
    def construct(self):
        A = ACreature()
        A.scale(2)
        self.add(A)
        self.play(A.animate.blink())
        self.wait()
        self.play(A.animate.look_at(UL))
        self.wait()
        self.play(A.animate.look_at(DR))
        self.wait()
        self.play(A.animate.restore_eyes())
        self.wait()
        self.play(A.animate.blink())

class AlgorithmBanner_scene(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        A = AlgorithmBanner()
        self.play(Create(A))
        self.wait()
        self.play(A.animate.expand())
        self.wait()

class BulletedListBrace_scene(Scene):
    def construct(self):
        self.camera.background_color = "#cee"
        b = BulletedListBrace("Item 1", "Item 2", "Item 3", "Item 4", "Item 5", title = '你好')
        self.add(b)
        self.play(b.animate.transform_brace())
        self.play(b.animate.transform_brace(LEFT))

class SingleNode_scene(Scene):
    def construct(self):
        self.camera.background_color = "#cee"

        s = SingleNode()
        s.change_info("44")
        s.set_node_color()
        s.set_index()
        self.add(s)

class SequentialList_scene(Scene):
    def construct(self):
        self.camera.background_color = "#cee"

        l = SequentialList()
        l.set_indexes()
        l.change_single_node_info(0, "333")

        self.add(l)

class MyCurvedLine_scene(Scene):
    def construct(self):
        m = MyCurvedLine(LEFT * 1.5, RIGHT * 2, points = 4)
        m.change_mode()
        self.add(m)

