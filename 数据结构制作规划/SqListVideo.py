from manim import *
from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"/"展示代码"

from ..AlgorithmBanner import AlgorithmBanner
from ..BulletedListBrace import BulletedListBrace
from ..MyCurvedLine import MyCurvedLine
from ..MovingCode import MovingCode
from ..FileMobject import FileMobject

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
