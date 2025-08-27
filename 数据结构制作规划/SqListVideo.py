from manim import *
from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"/"展示代码"

from ..AlgorithmBanner import AlgorithmBanner
from ..BulletedListBrace import BulletedListBrace
from ..MyCurvedLine import MyCurvedLine
from ..MovingCode import MovingCode
from ..FileMobject import FileMobject
from ..BigTree import BigTree
from ..ListNode import ListNode

class VideoText:
    def __init__(
            self,
    ):
        self.opening_animation_text()
        self.head_file_text()

    def opening_animation_text(self):
        self.START_TEX = r"""
            \begin{tabular}{p{8cm}}
            \hspace{1em}
            “形而上者谓之道，形而下者谓之器。”
            \end{tabular}
        """

        self.AUTHER_TEX = r"""
            \begin{tabular}{p{8cm}}
            \hspace{1em}
            ————《易经$\bullet$系辞》
            \end{tabular}
        """

        self.EXPLAIN_TEX = r"""
            \begin{tabular}{p{8cm}}
            \hspace{1em}
            详见课本19页，中华传统文化中的抽象思维。
            \end{tabular}
        """
    def head_file_text(self):
        self.TOTAL_TEX = [
            r"InitList(\&L)",
            r"DestroyList(\&L)",
            r"ListInsert(\&L, i, e)",
            r"ListErase(\&L, i, \&e)",
            r"ListClear(\&L)",
            r"ListAssign(L, i, value)",
            r"ListEmpty(L)",
            r"ListSize(L)",
            r"ListGetElem(L, i \&e)",
            r"ListFind(L, e)",
            r"ListTraverse(L, visit())"
        ]

        self.TITLE = r"线性表\\基本操作方法"

        self.CAPTION1 = r"""
            可暂停了解,\\
            详情见课本14页
        """

        self.CAPTION2 = r"""
            \&
        """
        self.CAPTION3 = r"""
            Sequential
        """

class SqListVideo:

    def __init__(
            self,
            scene:Scene
    ):
        self.banner = AlgorithmBanner()
        self.total_text = VideoText()
        self.scene = scene
        
    def opening_animation(self):
        self.scene.camera.background_color = AlgorithmBanner.get_background_color()[1]
        start_tex = Tex(
            self.total_text.START_TEX,
            tex_template = TexTemplateLibrary.ctex
        )
        start_tex.set_color(BLACK)
        start_tex.shift(UP*2.1)
        self.scene.play(FadeIn(start_tex), run_time = 1.3)
        self.scene.wait(1.8)

        auther_tex = Tex(
            self.total_text.AUTHER_TEX,
            tex_template = TexTemplateLibrary.ctex
        )
        auther_tex.scale(0.8).set_color(YELLOW_E)
        auther_tex.next_to(start_tex, DOWN, buff = 0.8)
        auther_tex.shift(RIGHT*1.8)
        self.scene.play(FadeIn(auther_tex), run_time = 1.5)
        self.scene.wait(1.5)

        explain_tex = Tex(
            self.total_text.EXPLAIN_TEX,
            tex_template = TexTemplateLibrary.ctex
        )
        explain_tex.set_color(GRAY_D)
        explain_tex.scale(0.6)
        explain_tex.to_edge(DOWN, buff = 1.3)
        self.scene.play(Write(explain_tex), run_time = 1.3)
        self.scene.wait(4.6)
        self.scene.clear()

        self.scene.play(Create(self.banner))
        self.scene.wait(1.3)
        self.scene.play(self.banner.expand())
        self.scene.wait(3.5)
        self.scene.play(FadeOut(self.banner))

        self.banner.clear_all_mobjects(self.scene)
        self.scene.wait()


    def head_file_animation(self):
        # Scene1
        start_tex = BulletedListBrace(*self.total_text.TOTAL_TEX, )
        start_tex.set(height = self.scene.camera.frame_height - 1)
        title = start_tex.get_title(self.total_text.TITLE)
        title.set_color(BLUE_D)
        start_tex.add(title)
        start_tex.shift(RIGHT*1.7)  
        
        self.scene.play(GrowFromCenter(title))
        start_tex.remove(title)
        self.scene.play(FadeIn(start_tex), run_time = 1.7)

        caption1 = Tex(self.total_text.CAPTION1, tex_template = TexTemplateLibrary.ctex)
        caption1.to_corner(UL, buff = 0.9).scale(0.7)
        caption1.set_color(YELLOW_E)
        cl = MyCurvedLine(start = start_tex.brace.get_center()+UP*0.1, end = caption1.get_center()+DOWN*0.8)

        self.scene.play(Write(caption1), cl.create())
        self.scene.wait(3)

        self.scene.clear()

        # Scene2
        CODE_PATH = ASSETS_DIR / "0头文件.cpp"
        define_code = MovingCode(CODE_PATH, formatter_style=MovingCode.get_cpp_stycle())

        self.scene.play(FadeIn(define_code))
        self.scene.wait(4.5)
        self.scene.play(define_code.animate.scale(0.9).to_edge(LEFT, buff = 0.9))
        define_code_rect = define_code.get_rect(1,3)
        define_code_svg = define_code.get_svg(2,'F')

        self.scene.wait(2)

        # Scene3
        caption2 = Tex(self.total_text.CAPTION2, tex_template = TexTemplateLibrary.ctex).scale(2)
        caption2.shift(RIGHT*2.8+DOWN*1.3).set_color(ORANGE)

        self.scene.play(Write(caption2))
        self.scene.wait()

        file_c = FileMobject().scale(0.7)
        file_cpp = FileMobject(name = '.cpp').scale(0.7)
        file_c.next_to(caption2, UP, buff = 1.9).shift(LEFT*1.3)
        file_cpp.next_to(file_c, RIGHT, buff = 1.5)

        file_c_curve_line = MyCurvedLine(caption2.get_center()+UP*0.3, file_c.get_center()+DOWN*0.4, points = 3)
        file_cpp_curve_line = MyCurvedLine(caption2.get_center() + UP*0.3, file_cpp.get_center()+DOWN*0.4, points = 3)
        self.scene.play(FadeIn(file_c))
        self.scene.play(FadeIn(file_cpp))
        self.scene.play(file_c_curve_line.create(), file_cpp_curve_line.create())

        self.scene.wait()
        self.scene.play(file_c.animate.set_color(GREEN_D).set_opacity(0.3))
        self.scene.play(file_cpp.animate.set_color(RED_D))
        self.scene.wait()

        self.scene.play(FadeIn(define_code_rect), FadeIn(define_code_svg))
        self.scene.wait(9)
        
        self.scene.clear()
        code_grps = VGroup(define_code, define_code_rect, define_code_svg)
        self.scene.add(code_grps)

        self.scene.play(code_grps.animate.scale(1.1).move_to(ORIGIN))
        self.scene.play(define_code.transform_both_svg_and_rectangle(code_grps[1], code_grps[2], 5, 8, 11))
        self.scene.wait(4)

        self.scene.play(define_code.transform_both_svg_and_rectangle(code_grps[1], code_grps[2], 13, 13))
        self.scene.wait(11)

    def define_list_Sq_animation(self):
        CODE_PATH = ASSETS_DIR /"1定义.cpp"
        movingcode = MovingCode(CODE_PATH)
        moving_copy = movingcode[0].copy()
        movingcode.to_edge(LEFT, buff = 0.6)

        self.scene.play(FadeIn(moving_copy[0]))
        self.scene.play(moving_copy[0].animate.to_edge(LEFT, buff = 0.6))
        self.scene.remove(moving_copy)
        self.scene.add(movingcode[0])
        self.scene.wait()

        SVG_PATH = ASSETS_DIR.parent/"场景切分"/"电脑1.svg"
        computer = SVGMobject(SVG_PATH) 
        computer.scale(3).to_edge(RIGHT, buff = 0.4).shift(DOWN*0.4)
        # self.add(movingcode.to_edge(LEFT, buff = 0.6))

        self.scene.play(FadeIn(computer))
        self.scene.wait(0.5)
        self.scene.play(Write(movingcode[1][0]), Write(movingcode[2][0]))
        self.scene.play(Circumscribe(movingcode[2][0]))
        self.scene.wait()

        l1 = ListNode().set_info(r"e_1").set_node_color()
        l2 = ListNode().set_info(r"e_2",).set_node_color()
        l3 = ListNode().set_info(r"\cdots", height = 0.07).set_node_color()
        l4 = ListNode().set_info(r'e_i').set_node_color()

        l_grps = VGroup(l1, l2, l3, l4).arrange(RIGHT, buff = 0)
        l_grps.set(width = computer.width - 0.57)
        l_grps.scale(0.87)
        l_grps.move_to(computer.get_center())

        my_line = MyCurvedLine(movingcode[2][1][12].get_center()+DOWN*0.12, l_grps[0].get_center()+DOWN*0.24, points=4)
        self.scene.play(
            Succession(
                FadeIn(l_grps[0]),
                FadeIn(l_grps[1]),
                FadeIn(l_grps[2]),
                FadeIn(l_grps[3]),
            ),
            AnimationGroup(
                FadeIn(movingcode[1][1]), 
                FadeIn(movingcode[2][1]),
                my_line.create()
            )
        )

        self.scene.play(
            my_line.fadeout(),
            FadeOut(my_line.arrows),
            FadeIn(movingcode[1][2]),
            FadeIn(movingcode[2][2]),
            FadeIn(movingcode[1][6]),
            FadeIn(movingcode[2][6])
        )

        self.scene.play(
            Write(movingcode[1][3]),
            Write(movingcode[2][3]),
        )
        self.scene.play(Circumscribe(movingcode[2][3]))
        self.scene.wait(3.5)

        self.scene.play(
            Write(movingcode[1][4]),
            Write(movingcode[2][4])
        )
        self.scene.play(
            Write(movingcode[1][5]),
            Write(movingcode[2][5]),
        )

        self.scene.wait(4.5)

    def initList_Sq_animation(self):
        CODE_PATH = ASSETS_DIR / "2InitList_Sq.cpp"
        mycode = MovingCode(CODE_PATH, formatter_style=MovingCode.get_cpp_stycle())
        mycode.width = self.scene.camera.frame_width - 1.7
        mycode.move_to(ORIGIN)
        self.scene.play(FadeIn(mycode),run_time = 1.5)
        self.scene.wait(0.5)
        self.scene.play(mycode.animate.to_edge(UP, buff = 0.3))
        
        tree = BigTree(self.scene, run_time=0.6)
        tree.create_tree(0.5, )

        caption3 = Tex(self.total_text.CAPTION3, tex_template = TexTemplateLibrary.ctex)
        caption3.set_color("#7CFC00")
        caption3.to_corner(DL,buff = 2).shift(LEFT)
        self.scene.play(Write(caption3))
        self.scene.wait()

        chars = VGroup(*[
            mycode[2][0][i]
            for i in range(16, 18)
        ])

        curve_line = MyCurvedLine(chars.get_center() + DOWN*0.2, caption3.get_center()+UP*0.3)

        self.scene.play(curve_line.create())
        self.scene.wait(4)

        moving_svg = mycode.get_svg(2, 'B')
        moving_rect = mycode.get_rect(2)

        self.scene.play(curve_line.fadeout(), FadeOut(curve_line.arrows), FadeOut(caption3), run_time = 2)
        self.scene.play(FadeIn(moving_svg), FadeIn(moving_rect), run_time = 0.75)
        self.scene.wait(0.25)
        self.scene.play(mycode.transform_both_svg_and_rectangle(moving_rect, moving_svg, 3, 3, 4), run_time = 0.85)
        self.scene.wait(0.25)
        self.scene.play(mycode.transform_both_svg_and_rectangle(moving_rect, moving_svg, 6, 7, 8), run_time = 0.9)
        self.scene.wait(4.5)

    def destroy_and_clear_animation(self):
        CODE_PATH1 = ASSETS_DIR / "3DestroyList_Sq.cpp"
        CODE_PATH2 = ASSETS_DIR / "4ListClear_Sq.cpp"
        movingcode1 = MovingCode(CODE_PATH1)
        movingcode2 = MovingCode(CODE_PATH2)
        moving_grps = VGroup(movingcode1, movingcode2).arrange(DOWN, buff = 0.5)
        moving_grps.set(height = self.scene.camera.frame_height - 1)

        self.scene.play(FadeIn(moving_grps[0]), FadeIn(moving_grps[1]))
        self.scene.play(Wiggle(moving_grps[0]))
        self.scene.play(Wiggle(moving_grps[1]))
        self.scene.wait(4.5)
