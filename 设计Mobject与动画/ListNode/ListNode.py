from cycler import cycle
from manim import(
    RoundedRectangle, MathTex,VGroup,
    BLACK, RIGHT,
    Scene
)
class ListNode(RoundedRectangle):
    cycle_color = cycle(["#FFE4E1 ","#DDA0DD","#7CFC00","#FFFF77","#33FFFF","#F08080","#5599FF","#FFAA33","#FFC0CB","#BC8F8F"])

    def __init__(
            self,
            corner_radius = 0.14,
            height = 1.4,
            width = 2.1,
            stroke_width = 10,
            **kwargs,
    ):
        super().__init__(
            corner_radius=corner_radius,
            width = width,
            height = height,
            stroke_width = stroke_width,
            **kwargs
        )
        self.node_normal_color = "#FFE4E1"
        self.stroke_width = stroke_width
        self.set_stroke(color = BLACK, opacity = 0.9)
        self.set_fill(color = self.node_normal_color, opacity=1)

        self.set_info(isinit=True)
        self.scale(0.7)
    def scale(self, scale_factor:float, **kwargs):
        self.remove(self.submobjects[0])
        self.set_stroke(width = scale_factor * self.stroke_width)
        self.add(self.tex)
        return super().scale(scale_factor, **kwargs)
    
    def get_cycle_color(self):
        # 追求的是颜色的专一性还是颜色的多样性?
        cycle_color = cycle(["#FFE4E1 ","#DDA0DD","#7CFC00","#FFFF77","#33FFFF","#F08080","#5599FF","#FFAA33","#FFC0CB","#BC8F8F"])
        color_name = {
            "#FFE4E1": "米色",
            "#DDA0DD": "浅紫色",
            "#7CFC00": "浅绿色",
            "#FFFF77": "浅黄色",
            "#33FFFF": "青蓝色",
            "#F08080": "浅红色",
            "#5599FF": "浅蓝色",
            "#FFAA33": "棕黄色",
            "#FFC0CB": "浅粉色",
            "#BC8F8F": "淡棕色"
        }
        return (cycle_color, list(color_name.values()))

    def set_info(self, info = "1",height = 0.3, width = None, isinit = False):
        """
            用来设置节点信息的.
            isinit:判断是否初始化, 
        """
        if not isinit:
            self.remove(self.submobjects[0])
        tex = MathTex(info)

        if height is not None:
            tex.set(height = height)
        if width is not None:
            tex.set(width = width)

        if tex.height > self.height:
            tex.set(height = self.height - 0.2)
        if tex.width > self.width:
            tex.set(width = self.width - 0.2)

        tex.move_to(self.get_center())
        tex.set_color(self.stroke_color)
        self.tex = tex

        self.add(tex)
        return self
    
    def change_info(self, change_info = "1", height = 0.3, width = None):
        # 更换节点信息
        self.set_info(change_info, height, width)

    def set_node_color(self):
        # 多样化设置节点颜色
        self.remove(self.submobjects[0])
        self.set_fill(color = next(ListNode.cycle_color))
        self.add(self.tex)
        return self
    
    def remove_node_color(self):
        # 恢复成默认节点颜色
        self.remove(self.submobjects[0])
        self.set_fill(color = self.node_normal_color)
        self.add(self.tex)
        return self
    
    @staticmethod
    def get_listnode_grps(infos: list, scene:Scene):
        # 得到节点组
        grps = VGroup(*[
            ListNode().set_info(info).set_node_color()
            for info in infos
        ]).arrange(RIGHT, buff = 0)
        grps.set(width = scene.camera.frame_width - 1)

        return grps
        

