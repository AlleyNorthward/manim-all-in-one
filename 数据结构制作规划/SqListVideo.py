from manim import *
from .AlgorithmBanner import AlgorithmBanner


class VideoText:
    def __init__(
            self,
    ):
        self.opening_animation_text()

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

        

