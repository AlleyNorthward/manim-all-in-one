from manim import(
    Rectangle, ImageMobject,TexTemplateLibrary, Tex,
    FadeIn, FadeOut, SpinInFromNothing, Create,
    BLACK, YELLOW_E, MAROON_B,
    DOWN,
    Scene,
    PI
)
from ..AlgorithmBanner import AlgorithmBanner
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"


class VideoChapter:
    # 打算是传入一个字符串列表,作为每个章节的标题动画
    # 只是针对这个动画而言
    def __init__(
            self,
            scene:Scene,
    ):
        self.scene = scene
        self.rec = self._get_reference_rec()
        self.banner = self._get_banner()
        self.photo = self._get_background()

    def _get_reference_rec(self):
        rec = Rectangle().set_color(BLACK)
        rec.set(height = self.scene.camera.frame_height)
        rec.stretch_to_fit_width(7)
        rec.move_to([-3.57, 0, 0])

        return rec

    def _get_banner(self):
        banner = AlgorithmBanner().scale(0.91)
        banner.move_to(self.rec.get_center())
        banner.shift(DOWN*1.67)

        return banner
    
    def _get_background(self):

        PATH_PHOTO = ASSETS_DIR / "背景设计" / "四个小人.png" 
        photo = ImageMobject(PATH_PHOTO)
        photo.set(width = self.scene.camera.frame_width)
        photo.set_z_index(-1)

        return photo

    def set_tex(self, text):
        self.tex = Tex(text, tex_template = TexTemplateLibrary.ctex).set_color(MAROON_B)
        self.tex.move_to(self.rec.get_top())
        self.tex.shift(DOWN*2.21)
    
    def create(self):
        PATH_SOUND = ASSETS_DIR / "音效" / "章节过度音效.mp3"
        self.scene.add_sound(PATH_SOUND, gain = 0)
        self.scene.play(
            FadeIn(self.photo),
            SpinInFromNothing(self.tex, point_color= YELLOW_E, angle=2*PI),
            run_time = 2
        )
        self.scene.play(Create(self.banner))
        self.scene.wait(1.5)
        self.scene.play(
            FadeOut(self.photo),
            FadeOut(self.tex),
            self.banner.fadeout_without_lgorithm()
        )