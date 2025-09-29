from manim import (
    BulletedList, TexTemplateLibrary, Brace, Tex,
    LEFT, RIGHT, 
    Transform, Succession,
    BLACK,
    override_animate
)
#_修改日志
"""
    @auther 巷北
    @time 2025.9.13
    将get_brace()改名为_init_brace()
    给transform_brace()添加了装饰器,并且将title与brace能一起移动

"""
class BulletedListBrace(BulletedList):
    #_代码示例
    """
        class Example(Scene):
            def construct(self):
                self.camera.background_color = "#cee"
                b = BulletedListBrace("Item 1", "Item 2", "Item 3", "Item 4", "Item 5", title = '你好')
                self.add(b)
                self.play(b.animate.transform_brace())
                self.play(b.animate.transform_brace(LEFT))
    """
    def __init__(
            self,
            *items,
            title = '',
            brace_color = BLACK,
            list_color = BLACK,
            title_color = BLACK,
            tex_template = TexTemplateLibrary.ctex,
            **kwargs,
    ):  
        super().__init__(*items, tex_template = tex_template, **kwargs)
        self.set_color(list_color)

        self.brace = self._init_brace(color = brace_color)
        self.title = self._init_title(title, title_color)
    
    def _init_brace(self, direction = LEFT, color = BLACK, **kwargs):
        brace = Brace(self, direction=direction, sharpness = 1.5, color = color, **kwargs)
        self.add(brace)
        return brace
    
    def transform_brace(self, brace, direction):
        return self.title.animate.next_to(brace, direction, buff = 0.3)
    
    @override_animate(transform_brace)
    def _transform_brace(self, direction = RIGHT, **anim_kwargs):
        # 作用是将左侧(举例)的brace转换到右侧(举例)
        new_brace = Brace(self, direction=direction, sharpness=1, color = self.brace.get_color(), )
        # _说明
        """
                这里一开始是ReplacementTransform, 然后self.brace = new_brace.总觉得不安全.测试了下后
            发现也没问题.后来想了想,这不就是Transform吗?又改成了下面这个.效果一样.
        """

        _transform = Transform(self.brace, new_brace)

        return Succession(
            _transform,
            self.transform_brace(new_brace, direction),
            **anim_kwargs
        )

    def _init_title(self, name, color = BLACK):
        tex = Tex(name, tex_template = TexTemplateLibrary.ctex)
        tex.set_color(color)
        tex.scale(0.8)

        tex.next_to(self.brace, LEFT, buff = 0.3)
        self.isfirst = True
        self.add(tex)
        return tex
