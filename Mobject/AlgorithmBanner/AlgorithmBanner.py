from manim import(
    VGroup,SVGMobject, Graph, Tex,TexTemplateLibrary, VMobjectFromSVGPath, 
    UpdateFromAlphaFunc, FadeIn, Succession, Create, AnimationGroup,SpiralIn,FadeOut,
    ORIGIN, LEFT, RIGHT, UP, DOWN, 
    TEAL, MAROON_B, BLUE, GREEN, BLUE_A, GRAY_BROWN,
    Scene,
    # config,
    override_animation,
    override_animate
)
from manim.utils.rate_functions import ease_in_out_cubic, smooth
import svgelements as se
from .ACreature import ACreature

# 修改日志
"""...
    @auther 巷北
    @time 2025.9.11 23:02 
    刚弄好环境,熄灯了.没做修改,但有了设想.像目前这种情况,应该再增添一个
    待办注释,方便以后查看,并且还能随时删除.
    ...
    @auther 巷北
    @time 2025.9.12 
    更换了A的造型,使用自制的ACreature.修改了computer、node、tree路径,并更改了颜色.
    修改了生成A、computer、node、tree的对应代码
    修复了入场动画样式bug(Create(A)).(svg图传入,无stroke_width属性会赋为None,发生危险.对组save_state,对应属性可能有问题(比如一个对象opacity为1,另一个为0,那么组的opacity可能选的是最前面的,而不是最大的).)
    
    更换了lgorithm字体,并且重新写了expand()的对应算法,并且添加装饰器,可以使用.animate生成动画.
    去除了一些非必要属性(以前不知道self.和参数传入有什么用,分析了这么多代码后,也知道了,self.设计的属性,最好要跟本类相关,而不是万物都设为属性.).
    ...
"""

# 待办
"""
    动画最后,将Aflip()一下,
    最后一边放大,一边FadeOut(),
    将路径封装到一个包中,统一管理一下.
"""
# 导入图片就下面这样最合法
from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"/"A"
A_PATH = ASSETS_DIR / "A.svg"
COMPUTER_PATH = ASSETS_DIR / "电脑.svg"
NODE_PATH = ASSETS_DIR / "Node.svg"
POINTER_PATH = ASSETS_DIR / "指针.svg"
TREE_PATH = ASSETS_DIR / "tree.svg"

# 如果需要导入package包中的某个东西, 需要用.来访问当前文件夹内的包


class AlgorithmBanner(VGroup):

    # 说明
    """
        @auther 巷北
        @time 2025.9.12 21:33

            这个动画很早就设计好了,如今做了修改.老版本的代码在github中,数据结构2.2视频package文件夹中还能找到.
        当时设计完了之后, 一直存在问题,就是SpiralIn()中传入组, 认为有问题.今天做了许多测试, 发现并没有问题.manim
        底层对于多submobjects解决还是很不错的.可是我一开始写的时候为什么会有问题呢? 最终发现原来是svg图的问题(也
        不是图的问题,还是manim没能很好的避免).最后这些问题也都解决了,动画也达到了理想的效果.
            用作开场动画吧.看看初始图能不能用作头像, 但可能会有些奇怪.

    """

    # 属性
    """
        A                                   标志性设计
        tree
        node
        computer
        shapes                              三个组件,由上面三个组成的
        lgorithm                            algorithm后面的字母
        title                               个性名称

        scale_factor                        源码有的,目前不好去除
    """

    # 私有方法
    """
        _init_A()
        _init_node()
        _init_computer()
        _init_tree()
        _init_lgorithm()
        _get_title()
        _expand()                           拓展动画
        create()                            被装饰器装饰了,可以通过Create访问
        fadeout()                           同上,通过FadeOut()访问
    """
    
    # 公有方法
    """
        scale()                             统一缩小,防止lgorithm未加入self而无法缩小
        expand()                            _expand()接口,通过.animate访问
        get_background_color()              类方法.初期时颜色代码记不住,只能写个方法,便于访问.
        fade_out_without_lgorithm()         如果未添加lgorithm()就FadeOut(),会存在问题.
        clear_all_mobjects()                静态方法,传入场景,清除.
    """
    ALGORITHM_SVG_PATH = [
        # l
        se.Path("M0,7.91V.97C0,.65.07.41.21.25s.33-.25.58-.25.44.08.59.24.22.41.22.73v6.94c0," \
        ".32-.08.57-.23.73s-.34.24-.58.24-.42-.08-.57-.25-.22-.41-.22-.72Z"),
        # g
        se.Path("M6.24,1.17v4.65c0,.53-.06.99-.17,1.37s-.29.7-.54.95-.58.44-.98.56-.91.18-1.51.18c-" \
        ".55,0-1.04-.08-1.48-.23s-.77-.35-1-.6-.35-.5-.35-.75c0-.2.07-.35.2-.48s.29-.18.48-.18c.23,0," \
        ".44.1.62.31.09.11.17.21.27.32s.19.2.3.28.25.13.4.17.34.06.54.06c.41,0,.74-.06.96-.17s.39-.28.48-." \
        "48.15-.43.16-.67.03-.62.04-1.14c-.25.34-.53.61-.85.79s-.71.27-1.15.27c-.54,0-1-.14-1.4-.41s-.71-.66-." \
        "92-1.15-.32-1.06-.32-1.71c0-.48.07-.91.2-1.3s.32-.71.56-.98.52-.47.84-.6S2.26.01,2.64.01c.45,0,.85.09,1.18" \
        ".26s.64.45.93.82v-.22c0-.28.07-.49.21-.64s.31-.23.53-.23c.31,0,.51.1.62.3s.15.49.15.87ZM1.61,3.2c0,.65.14,1.14" \
        ".42,1.47s.65.5,1.1.5c.27,0,.52-.07.75-.21s.43-.36.58-.64.22-.64.22-1.05c0-.65-.14-1.16-.43-1.52s-.67-.54-1.13-.54"
        "-.82.17-1.1.52-.41.84-.41,1.48Z"),
        # o
        se.Path("M6.37,3.25c0,.48-.07.92-.22,1.32s-.36.75-.64,1.04-.62.51-1.01.67-.83.23-1.32.23-.92-.08-1.31-.23-." \
        "72-.38-1-.67-.5-.63-.64-1.03-.22-.83-.22-1.32.07-.93.22-1.33.36-.75.64-1.03S1.47.39,1.87.23s.83-.23,1.31-.23." \
        "92.08,1.32.23.73.38,1.01.67.5.63.64,1.03.22.84.22,1.32ZM4.76,3.25c0-.65-.14-1.16-.43-1.52s-.67-.54-1.16-.54c-." \
        "31,0-.59.08-.83.24s-.42.4-.55.72-.19.69-.19,1.11.06.78.19,1.1.31.55.54.72.51.25.83.25c.48,0,.87-.18,1.16-.55s.43-" \
        ".87.43-1.51Z"),
        # r
        se.Path("M1.6,4.2v1.34c0,.32-.08.57-.23.73s-.35.24-.58.24-.42-.08-.57-.25-.22-.41-.22-.73V1.08C0,.36.26,0,.78,0c." \
        "27,0,.46.08.57.25s.18.42.19.74c.19-.33.39-.58.59-.74s.47-.25.81-.25.66.08.98.25.47.39.47.67c0,.2-.07.36-.2.48s-.28" \
        ".19-.44.19c-.06,0-.2-.04-.42-.11s-.42-.11-.59-.11c-.23,0-.43.06-.57.18s-.26.31-.35.55-.14.53-.17.86-.05.74-.05,1.22Z"),
        # i
        se.Path("M.81,1.56c-.22,0-.41-.07-.57-.21s-.24-.33-.24-.58c0-.23.08-.41.24-.56s.35-.22.57-.22.39.07.55.2.24.33.24." \
        "58-.08.44-.23.58-.34.21-.56.21ZM1.6,3.22v4.62c0,.32-.08.56-.23.73s-.35.25-.58.25-.42-.08-.57-.25-.22-.41-.22-.72V3." \
        "26c0-.32.07-.55.22-.71s.34-.24.57-.24.43.08.58.24.23.38.23.67Z"),
        # t
        se.Path("M.74,2.31h.18v-.96c0-.26,0-.46.02-.61s.05-.27.11-.38c.06-.11.15-.2.27-.27s.25-.1.39-.1c.2,0,.39.08.55.23.11.1" \
        ".18.23.21.37s.04.35.04.62v1.09h.59c.23,0,.4.05.52.16s.18.25.18.41c0,.21-.08.37-.25.45s-.41.13-.73.13h-.3v2.94c0,.25,0," \
        ".44.03.58s.06.24.14.33.2.13.37.13c.09,0,.22-.02.38-.05s.29-.05.38-.05c.13,0,.25.05.35.16s.16.23.16.38c0,.26-.14.46-.42.59" \
        "s-.69.21-1.21.21c-.5,0-.88-.08-1.14-.25s-.43-.4-.51-.7-.12-.69-.12-1.19v-3.07h-.21c-.23,0-.41-.05-.53-.16s-.18-.25-.18-.42." \
        "06-.31.19-.41.31-.16.55-.16Z"),
        # h
        se.Path("M1.6.97v2.37c.2-.23.4-.42.59-.56s.41-.24.64-.31.49-.1.76-.1c.41,0,.77.09,1.08.26s.56.42.74.75c.11.19.19.41.23.6" \
        "4s.06.51.06.82v3.06c0,.32-.07.56-.22.73s-.34.25-.58.25c-.53,0-.79-.32-.79-.97v-2.7c0-.51-.08-.91-.23-1.18s-.44-.41-.87-.4" \
        "1c-.29,0-.54.08-.77.24s-.4.38-.51.67c-.09.24-.13.66-.13,1.27v2.12c0,.32-.07.56-.21.72s-.34.25-.59.25c-.53,0-.79-.32-.79-.97V" \
        ".97C0,.65.07.41.21.24s.33-.24.58-.24.45.08.59.25.21.41.21.73Z"),
        # m
        se.Path("M5.41,3.37v2.13c0,.34-.08.59-.23.76s-.35.25-.6.25-.44-.08-.59-.25-.23-.42-.23-.76v-2.55c0-.4-.01-.71-.04-.94s-.1-.41-" \
        ".22-.55-.31-.21-.57-.21c-.52,0-.87.18-1.03.54s-.25.88-.25,1.55v2.16c0,.33-.08.58-.23.75s-.35.25-.59.25-.44-.08-.59-.25-.23-.4" \
        "2-.23-.75V.92C0,.62.07.39.21.23s.32-.23.55-.23.4.07.55.22.22.35.22.61v.15c.28-.33.57-.58.89-.73S3.08.01,3.47.01s.75.08,1.04.24." \
        "53.4.71.73c.27-.33.56-.57.87-.73S6.74.01,7.11.01c.44,0,.81.09,1.13.26s.55.42.71.74c.14.29.21.74.21,1.37v3.12c0,.34-.08.59-.23.76s-." \
        "35.25-.6.25-.44-.08-.59-.25-.23-.42-.23-.75v-2.69c0-.34-.01-.62-.04-.83s-.11-.38-.24-.52-.32-.21-.59-.21c-.21,0-.41.06-.6.19s-.34.29"
        "-.44.5c-.12.27-.18.75-.18,1.43Z")
    ]
    a_height_over_lgorithm_height = 0.75748

    def __init__(self, dark_theme: bool = False):
        super().__init__()
        self.font_color = "#ece6e2" if dark_theme else "#343434"

        self.scale_factor = 1

        self.A = self._init_A()
        self.tree = self._init_tree()
        self.computer = self._init_computer()
        self.node = self._init_node()
        self.shapes = VGroup(self.tree, self.computer, self.node)
        
        self.add(self.shapes, self.A)
        self.move_to(ORIGIN)

        self.lgorithm = self._init_lgorithm(AlgorithmBanner.a_height_over_lgorithm_height)
        self.title = self._get_title()
        self.scale(0.77)

    def _init_A(self):
        A = ACreature('plain')
        A = A[0]
        A.set_color(self.font_color)
        A.set(height = 3)
        A.flip()
        A.shift(1.725*LEFT + 0.65*UP)
        return A
    
    def _init_tree(self):
        g = SVGMobject(TREE_PATH)
        g[0].set_color(MAROON_B)
        g[1].set_color(TEAL)
        g.scale(0.89)
        g.shift(RIGHT*2.1 + LEFT*0.63)
        g.stroke_width = 0 if g.stroke_width is None else g.stroke_width
        g.set_fill(opacity = 1 if g.get_fill_opacity() == 0 else g.get_fill_opacity())
        return g
    
    def _init_computer(self):
        computer = SVGMobject(COMPUTER_PATH)
        computer.set_color("#935300")
        computer[1].set_color("#f0f36a")
        computer.scale(0.94)
        computer.shift(UP*0.7+RIGHT*0.07)
        computer.stroke_width = 0 if computer.stroke_width is None else computer.stroke_width
        computer.set_fill(opacity = 1 if computer.get_fill_opacity() == 0 else computer.get_fill_opacity())
        return computer

    def _init_node(self):
        node = SVGMobject(NODE_PATH)
        node.scale(0.91)
        node.shift(LEFT*0.79+DOWN*0.17)
        node.stroke_width = 0 if node.stroke_width is None else node.stroke_width
        node.set_fill(opacity = 1 if node.get_fill_opacity() == 0 else node.get_fill_opacity())
        return node
    
    def _init_lgorithm(self, a_height_over_lgorithm_height):
        lgorithm = VGroup()
        for index, path in enumerate(AlgorithmBanner.ALGORITHM_SVG_PATH):
            tex = VMobjectFromSVGPath(path).flip(RIGHT)
            tex.set(stroke_width = 0)
            tex.scale(0.3)
            tex.center()
            if index > 0:
                tex.next_to(lgorithm, buff = 0.02)
            lgorithm.add(tex)
        lgorithm.set_fill(color = self.font_color, opacity=1)
        lgorithm.height = a_height_over_lgorithm_height * self.A.height
        for tex in lgorithm:
            tex.align_to(self.A, DOWN)

        return lgorithm

    def _get_title(self):
        title = Tex(
            r"\textbf{巷北}",
            tex_template = TexTemplateLibrary.ctex
        ).set_color_by_gradient([BLUE_A,BLUE, GREEN,GRAY_BROWN]).scale(2)
        pointer = SVGMobject(POINTER_PATH).next_to(title,LEFT, buff = -0.25).scale(0.4)
        pointer.set_color(self.font_color)
        grps = VGroup(pointer, title)
        grps.scale(1.4)
        grps.move_to(ORIGIN)
        grps.shift(UP*2.4)

        return grps
    
    @override_animation(Create)
    def create(self, run_time = 2) -> AnimationGroup:

        return AnimationGroup(
            SpiralIn(self.shapes, run_time = run_time),
            FadeIn(self.A, run_time = run_time / 2),
            lag_ratio = 0.1
        )
    
    def scale(self, scale_factor:float, **kwargs):
        self.scale_factor *= scale_factor
        if self.lgorithm not in self.submobjects:
            self.lgorithm.scale(scale_factor, **kwargs)
        if self.title not in self.submobjects:
            self.title.scale(scale_factor, **kwargs)
        return super().scale(scale_factor, **kwargs)
    
    def expand(self):
        #todo 可以拆分一下_expand()中部分代码到这里来.
        pass

    @override_animate(expand)
    def _expand(self, run_time: float = 2, has_title = True, **anim_kwargs) -> Succession:    
        run_time = 2 if has_title else 1.5

        A_shape_offset = 11 * self.scale_factor
        shape_sliding_overshoot = 0.8 * self.scale_factor

        self.lgorithm.next_to(self.A, buff = 0.06).align_to(self.A, DOWN)
        self.lgorithm[1].shift(DOWN*0.6432)

        self.lgorithm.set_opacity(0)
        self.shapes.save_state()
        m_clone = self.lgorithm[-1].copy()
        m_clone.set_opacity(0)
        self.add(m_clone)
        m_clone.move_to(self.shapes)

        self.A.save_state()
        left_group = VGroup(self.A, self.lgorithm, m_clone)

        def shift(vector):
            self.shapes.restore()
            left_group.align_to(self.A.saved_state, LEFT)
            self.shapes.shift(vector / 2)
            left_group.shift(-vector / 2)

        
        def slide_and_uncover(mob, alpha):
            shift(alpha * (A_shape_offset + shape_sliding_overshoot) * RIGHT)

            for letter in mob.lgorithm:
                if mob.computer.get_left()[0] > letter.get_center()[0]:
                    letter.set_opacity(1)
                    self.add_to_back(letter)

            if alpha == 1:
                self.remove(*[self.lgorithm])
                self.add_to_back(self.lgorithm)
                # 弃案 源代码存在 mob.shapes.set_z_index(0)
                mob.shapes.save_state()
                mob.A.save_state()

        def slide_back(mob, alpha):
            if alpha == 0:
                m_clone.set_opacity(1)
                m_clone.move_to(self.lgorithm[-1])
                mob.lgorithm.set_opacity(1)

            shift(alpha * shape_sliding_overshoot * LEFT*0.9527)

            if alpha == 1:
                mob.remove(m_clone)
                mob.add_to_back(mob.shapes)
            
        return Succession(
            UpdateFromAlphaFunc(
                self,
                slide_and_uncover,
                run_time = run_time * 2 / 4,
                rate_func = ease_in_out_cubic,
            ),
            UpdateFromAlphaFunc(
                self,
                slide_back,
                run_time = run_time * 1 / 4,
                rate_func = smooth,
            ),
            AnimationGroup(
                FadeIn(
                    self.title,
                    run_time = run_time * 1 / 4,
                    rate_func = smooth
                ),
                # self.A.animate.flip(), #todo  传入UP是绕Y轴旋转.需要研究一下. 有问题, AnimationGroup()与.flip()结合可能会产生问题.play分隔就没事.
            ),
            **anim_kwargs
        ) if has_title else Succession(
            UpdateFromAlphaFunc(
                self,
                slide_and_uncover,
                run_time = run_time * 2 / 3,
                rate_func = ease_in_out_cubic,
            ),
            UpdateFromAlphaFunc(
                self,
                slide_back,
                run_time = run_time * 1 / 3,
                rate_func = smooth,
            ),
            # 待优化 self.A.animate.flip(),
            **anim_kwargs
        )
    @classmethod
    def get_background_color(cls):
        return ("#343434", "#ece6e2")
    
    @override_animation(FadeOut)
    def fadeout(self, run_time = 1) :
        # todo可以设计一边放大,一边消退
        return AnimationGroup(
            FadeOut(self.shapes, run_time = run_time), 
            FadeOut(self.title, run_time = run_time),
            FadeOut(self.A, run_time = run_time),
            FadeOut(self.lgorithm, run_time = run_time)
        )
    
    # 说明 上面存在bug是, 如果没有添加lgorithm或者title, FadeOut对象整体的时候, 仍然显现.
    def fadeout_without_lgorithm(self, run_time = 1):
        return AnimationGroup(
            FadeOut(self.shapes, run_time =run_time),
            FadeOut(self.A, run_time = run_time)
        )
    
    @staticmethod
    def clear_all_mobjects(scene: Scene):
        scene.clear()

