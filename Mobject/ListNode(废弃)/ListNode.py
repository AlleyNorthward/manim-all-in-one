from cycler import cycle
from manim import(
    RoundedRectangle, MathTex,VGroup, SVGMobject, Tex, TexTemplateLibrary,
    Create, Succession, AnimationGroup, Restore, MoveToTarget,
    RIGHT, DOWN, UP, LEFT, 
    BLACK, GREEN_D, TEAL, MAROON,
    Scene,
    PI,
    override_animate
)
from .MyCurvedLine import MyCurvedLine

from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

#_修改日志
"""
    @auther 巷北
    @time 2025.9.14 18:46
    修改变量引用方式.(其实self.tex/self[0]/self.submobjects[0]都是同一个对象.)
    更新了get_nodes_curved_arrows() 方法中获取箭头的逻辑, 使之更加合理,并且易于理解.
    修改了交换动画的逻辑,更清晰易懂
    未去除ListNodeAnimation类, 并在ListNode中添加了.animate接口,用于产生动画.
    ...
    @auther 巷北
    @time 2025.9.17 21:15
    该文档已废弃.后续将单独分成Node, 其他的数据结构采用继承Node的方式存在.所以ListNode
    会以另一种形式展现,而这里的ListNode废弃.保留的目的是学习、参考.
    最近在练习vim,学习曲线很陡,所以打字、写代码的欲望没有这么强烈.一些平时的敲代码的习惯
    都要强行改变,转而使用另一种不同的方式来敲代码,确实有些不太习惯.不过长远考虑,这些都是
    很有必要的.后续打算终端+vim编写代码,移除vscode的使用.
    最后祝我好运吧.
"""
#_待办
"""
    restore_nodes存在问题.
    本来它面向整体.现在拆分成单一结点,无法操作
    建议改成类方法,可控一些.
    择日修改.
    错误代码:
    
class Test(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        infos = [
            "1",
            "2",
            "253",
            "245",
            "789",
            "961"
        ]
        l:ListNode = ListNode.get_listnode_grps(infos)
        index = ["0", "1", "2", "3", "4", "5"]
        i = ListNode.get_array_index(l, index)
        self.add(l, i)
        c = ListNode.get_nodes_curved_arrows(l, 1, 2, buff = 0.1,direction=0.05)
        l[0].save_state()
        l[1].save_state()
        self.play(
            l[0].animate.swap(l[1], c)
        )
        c2 = c.copy().shift(RIGHT*l[0].width)
        self.play(l[0].animate.swap(l[2],c2), FadeOut(c))
        self.play(l[0].animate.restore_nodes())


"""
class ListNode(RoundedRectangle):
    #_说明

    """
        @auther 巷北
        @time 2025.9.14 17:14
            哎, 现在刚打开文件, 看了头疼, 哈哈. 
            这就不得不提到面向对象设计问题了, 只为当下考虑, 不为未来考虑, 想到什么些什么, 确实很容易产生问题.
        经过这么一次修改, 也知道麻烦了, 以后肯定也就注意了.
            不过这也怪不得当时的我, 制作视频过程中, 考虑到需要结点的问题, 便设计了结点.可是随着视频的进行, 发现
        又需要下标, 便提供了显示下标的接口.然后又需要展示多结点, 又需要展示结点移动,等等等等, 都是发现需要的时候,
        现去添加的.所以虽然制作时也修改, 整理过, 后续也不那么的难受, 但主要重心并不是结点设计上, 而是视频制作, 加
        上时间也比较赶, 现在看起来比较乱, 自然也就理所应当.
            我肯定也希望一次性设计好, 但实际中总是事与愿违.所以我才来更新代码, 使得后续使用、增添功能、更新时更轻
        松, 少走些弯路.当然, 这也能提升编程设计能力, 而不仅仅是能跑起来就足够了.
            现在来看, 设计Mobject的时候, 就全身心地投入到设计之中, 不要被视频制作影响.可能迅速完成Mobject设计, 能
        接替上视频制作, 但玩一后续视频还要使用, 又不得不缝缝补补, 发现bug的话, 可能会浪费不少时间, 得不偿失.
    """

    #_属性
    """
        animations                  便于生成动画
        tex                         结点信息
    """

    #_私有方法
    """
        set_info()                      结点信息设置.其接口是change_info()
        _swap()                         交换动画
        _resotre_nodes()                恢复动画
        _insert_nodes()                 插入动画

        get_list_node_grps_with_index() 老版本方法.不再使用

    """

    #_公有方法
    """
        scale()                     修改了一下逻辑
        get_cycle_color()           渐变颜色接口
        change_info()               更换结点信息接口
        set_node_color()            设置结点颜色
        remove_node_color()         恢复结点颜色至默认颜色
        get_listnode_grps()         得到结点组
        get_array_index()           得到结点组下标
        scale_single_node_infos()   缩放单一结点信息
        scale_nodes_infos()         缩放结点组信息
        get_nodes_curved_arrows()   得到结点指向箭头
        
        swap()                      交换结点动画接口
        insert_node()               插入结点动画接口
        restore_nodes()             恢复结点动画接口
    """

    #_代码示例
    """
        class Test(Scene):
            def construct(self):
                self.camera.background_color = "#ece6e2"
                infos = [
                    "1",
                    "2",
                    "253",
                    "245",
                    "789",
                    "961"
                ]
                l:ListNode = ListNode.get_listnode_grps(infos)
                index = ["0", "1", "2", "3", "4", "5"]
                i = ListNode.get_array_index(l, index)
                self.add(l, i)
                c = ListNode.get_nodes_curved_arrows(l, 1, 2, buff = 0.1,direction=0.05)
                l[0].save_state()
                l[1].save_state()
                self.play(
                    l[0].animate.swap(l[1], c)
                )
                self.play(l[0].animate.restore_nodes())
    """
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
        self.animations = ListNodeAnimation()
        node_normal_color = "#FFE4E1"
        self.set_stroke(color = BLACK, opacity = 0.9)
        self.set_fill(color = node_normal_color, opacity=1)

        self.set_info(isinit=True)
        self.scale(0.7)

    def scale(self, scale_factor:float, **kwargs):
        self.remove(self.tex)                   #_解释 这里是动态增粗.由于是组合形式,所以self中submobject的stroke,也会变.这里就先去除tex,再添加tex,避免增粗.
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
        #_解释
        """
            用来设置节点信息的.
            isinit:判断是否初始化, 
            可以更熟传入info自动调整大小, 适应不同的ListNode
            私有方法.接口是change_info()
        """
        if not isinit:
            self.remove(self.tex)
            del self.tex #_解释 其实没必要这么操作, 但是为了深入理解python, 就这么写了.

        #todo 无法提供中文文本. 如果需要, 可以再添加, 只是加个判断语句就好了.
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
        #_解释 更换节点信息  用户接口
        self.set_info(change_info, height, width)
        return self.tex

    def set_node_color(self):
        #_解释  多样化设置节点颜色
        self.remove(self.tex)
        self.set_fill(color = next(ListNode.cycle_color))
        self.add(self.tex)
        return self
    
    def remove_node_color(self):
        #_解释  恢复成默认节点颜色
        node_normal_color = "#FFE4E1"
        self.remove(self.tex)
        self.set_fill(color = node_normal_color)
        self.add(self.tex)
        return self
    
    @staticmethod
    def get_listnode_grps(infos: list, ref_length = None):
        if ref_length is None:
            ref_length = 1.342*len(infos)
        grps = VGroup(*[
            ListNode().set_info(info).set_node_color()
            for info in infos
        ]).arrange(RIGHT, buff = 0)
        grps.set(width = ref_length - 0.2)

        return grps
    
    @staticmethod
    def get_array_index(list_node_grps, indexes):
        #_说明 未与list_node_grps保留成组, 调用后在外自己设立就好.
        digits = VGroup(*[
            MathTex(f"{index}").next_to(node, DOWN, buff = 0.05).scale(0.6).set_color(GREEN_D)
            for index, node in zip(indexes, list_node_grps)
            if index != ""
        ])

        return digits
    
    @staticmethod
    def scale_single_node_infos(nodes: VGroup, index = 0, scale_factor = 0.4):
        # _说明  这里默认的只是结点组, 而不是其他组的整合
        nodes[index].tex.scale(scale_factor)

    @staticmethod
    def scale_nodes_infos(nodes: VGroup, indexes:list, scale_factors:list):

        for index, scale_factor in zip(indexes, scale_factors,):
            ListNode.scale_single_node_infos(nodes, index, scale_factor)
    
    @staticmethod
    def get_nodes_curved_arrows(nodes, index1, index2, isflip = False, istop = True, buff = 0.1, direction = UP*0.1):
        #_解释 buff 是因为箭头第一个点有些靠下, 提供接口, 灵活移动 direction是整体移动
        #_解释 isflip并不是flip,而是"肚子"朝向. istop是箭头在结点的上方还是下方

        #_说明  箭头朝下的参数配置参考c = ListNode.get_nodes_curved_arrows(l, 1, 2, buff = -0.1, direction=- 0.1, istop = False, isflip = True)(自己修改调整就好)
        index1 = index1 - 1 #_解释 输入下标从1开始, 用户可以更直观地找准对应关系.
        index2 = index2 - 1
        up = UP*buff
        m = MyCurvedLine(
            nodes[index1].get_top() + up if istop else nodes[index1].get_bottom() - up,
            nodes[index2].get_top() if istop else nodes[index2].get_bottom(),
            iscurvedarrows = True,
            angle = PI / 2 if isflip else -PI / 2
        )
        m.shift(direction)
        return m
            
    #_说明 Animation部分
    def swap(self, node, curved_line,):
        return self.animations.transform_nodes(self,node, curved_line)

    @override_animate(swap)
    def _swap(self, node, curved_line, **anim_kwargs):
        if anim_kwargs is None:
            anim_kwargs = {}
        animation = self.swap(node, curved_line, )
        return animation
    
    def restore_nodes(self):
        return self.animations.restore_nodes()
    
    @override_animate(restore_nodes)
    def _restore_nodes(self, **anim_kwargs):
        if anim_kwargs is None:
            anim_kwargs = {}
        animation = self.restore_nodes()
        return animation
    
    def insert_node(self, single_node,):
        return self.animations.insert_node(self, single_node)

    @override_animate(insert_node)
    def _insert_node(self, single_node, **anim_kwargs):
        if anim_kwargs is None:
            anim_kwargs = {}
        animation = self.insert_node(single_node)
        return animation
    
    @staticmethod
    def get_list_node_grps_with_index(
        scene: Scene, 
        node_infos: list, 
        index_infos: list = None, 
    ):
        # 这个方法是固定的, 独属于ListInsert, ListErase视频的, 其他情况最好不要使用
        #_说明 这个注释很明确, 那就不做修改, 但仍然保留.后续使用该类的时候可以删掉
        list_grps = ListNode.get_listnode_grps(node_infos, scene)
        list_grps.set(width = scene.camera.frame_width - 5)

        tex = Tex(r"首地址\\L.base", tex_template = TexTemplateLibrary.ctex).scale(0.4).set_color(TEAL)

        PATH_POINTER = ASSETS_DIR / "ListNode" / "指针.svg"
        pointer = SVGMobject(PATH_POINTER)
        pointer.scale(0.37)
        pointer.rotate(-PI/2)
        pointer.next_to(list_grps[0], LEFT, buff = 0.15)
        pointer.shift(UP*0.3)
        tex.next_to(pointer, DOWN, buff = 0.1)
        tex.shift(LEFT*0.1)        
        pointer_with_tex = VGroup(pointer, tex)
        if index_infos is not None:
            index_digits = ListNode.get_array_index(list_grps, index_infos)
            grps = VGroup(list_grps, index_digits, pointer_with_tex)
        else:
            grps = VGroup(list_grps, pointer_with_tex)

        return grps

class ListNodeAnimation:
    """
            这里本来想继承ListNode, 但是上面产生的是Mobject, 子类却是产生动画, 
        属性上不太相关. 而且我也只是想封装一些动画, 要是继承的话, 创建对象时还需要
        添加父类相关属性, 偏离的我实际想法.
            所以打算采用组合的方式专门为该对象封装其对应的动画, 从而能达到我自己
        想要的效果
            做这一点的原因是因为在写ListInsert动画的时候, 采取贪心思想, 每步选择当前最优
        随着代码量的提高, 我发现重复代码也升高了. 但是陷进去了, 写了几百行, 没法出来,
        只能硬着头皮继续写. 等写完复盘发现, 不如将这些功能封装起来, 减少代码量.
            我也没有开天眼, 也是第一次尝试去做, 并不确定后续是否会添加相同代码, 也
        算是经验积累吧.不过站在全局的角度来看, 我现在其实仍然是动态规划着来的, 要不然
        ListErase也一直重复写, 贪心到底了.
    """
    saved_mob = []
    def __init__(
        self,
    ):
        pass

    def save_nodes_state(self, nodes,):
        if isinstance(nodes, ListNode):
            nodes.save_state()
        else:
            for node in nodes:
                node.save_state()

    def transform_nodes(self, node1, node2, curved_line,):
        ListNodeAnimation.saved_mob.append(node1)
        ListNodeAnimation.saved_mob.append(node2)
        node1.generate_target()
        node2.generate_target()

        position = node1.get_center()
        node1.target.move_to(node2.get_center())
        node2.target.move_to(position)

        return Succession(
            Create(curved_line),
            AnimationGroup(
                MoveToTarget(node1),
                MoveToTarget(node2)
            )
        )
    
    def insert_node(self,node, single_node):
        #! 未保留初始信息.

        index = index - 1
        single_node.generate_target()
        single_node.target.move_to(node.get_center())
        return MoveToTarget(single_node)

    def restore_nodes(self,):
        animations = []
        for mob in ListNodeAnimation.saved_mob:
            animations.append(Restore(mob))

        ListNodeAnimation.saved_mob.clear()
        return AnimationGroup(*animations)
    



    