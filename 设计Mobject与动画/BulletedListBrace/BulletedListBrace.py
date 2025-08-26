from manim import (
    BulletedList, TexTemplateLibrary, Brace, Tex,
    LEFT, RIGHT, 
    ReplacementTransform,
    BLACK
)
class BulletedListBrace(BulletedList):
    def __init__(
            self,
            *items,
            brace_color = BLACK,
            list_color = BLACK,
            tex_template = TexTemplateLibrary.ctex,
            **kwargs,
    ):
        self.list_color = list_color
        self.brace_color = brace_color
        super().__init__(*items, tex_template = tex_template, **kwargs)
        self.set_color(BLACK)

        self.brace = self.get_brace()
    
    def get_brace(self, direction = LEFT, **kwargs):
        brace = Brace(self, direction=direction, sharpness = 1.5, color = self.brace_color, **kwargs)
        self.add(brace)
        return brace
    
    def transform_brace(self, direction = RIGHT, **kwargs):
        # 作用是将左侧(举例)的brace转换到右侧(举例)
        new_brace = Brace(self, direction=direction, sharpness=1, color = self.brace_color, **kwargs)
        transform = ReplacementTransform(self.brace, new_brace)
        self.brace = new_brace

        return transform

    def get_title(self, name):
        tex = Tex(name, tex_template = TexTemplateLibrary.ctex)
        tex.set_color(self.brace_color)
        tex.scale(0.8)

        tex.next_to(self.brace, LEFT, buff = 0.3)
        return tex
