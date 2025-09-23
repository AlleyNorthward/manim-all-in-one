from manim import *
from itertools import cycle

# 日志记录
"""
    @auter 巷北
    @time 2025.9.19 17:08

    这是配置好vim终端后第一次写manim代码,只会一些基本的vim操作,但实际上,也满足了我很多需求.
    至于为什么要学vim呢,其实主要还是因为非常喜欢在终端操作.所以大一的时候,很早就用vscode.可
    由于理解不深,很多都不懂,外加上配置C/C++十分困难, 所以十分难操作.不过我一直强制要求我使用
    vscode,明白终端之后,也一直要求自己使用终端运行代码,虽然那段时间没怎么学习,但是也有了一些
    积累.随着积累的越来越多,我觉得可以去了解一下其他的东西了.在今年五月份左右吧,我知到了vim
    并且安装了gvim.不过忘了当时为什么没有坚持下去,不过好在也没有深入,时间并没有浪费掉.后面写
    的代码多起来了之后,vscode也是用的越发熟练,同时,每想用鼠标点击一下,我就越发感到不舒服.还因
    为vscode中运行代码,我都是通过终端运行的,跟vscode关系非常小.终于,差不多三四天前忍不住了,
    选择放弃vscode,投奔vim+powershell.可是整个过程异常艰难.因为这段时间是我敲代码的重要时期,
    vim学习曲线非常陡峭,敲代码速度下滑的很厉害,而且有些厌恶用vim敲代码.哦对了,一开始是用的vscode
    的vim,发现有些操作还是不得不用鼠标,所以直接放弃vscode了.(其实这段话应该插入到上面的,但是vim
    操作还不会,所以就先这么弄吧)后面觉得,终端+vim需要界面美化,所以用了一天半的时间去捣鼓这些东西,
    你懂的,很不容易,好在终于弄完了,vim的book也到了,可以专心操作vim编辑文本了.写这么多,并不是Node
    的日志记录,而是个人第一次使用终端使用vim的记录吧~~~(吐槽一下,中文vim使用起来很不友善啊,每次想
    快捷操作,一看是中文输入法,还得多按个按钮...)
    哎,文件名为Node,跟vim一个插件名重复了,再进来就有问题...

    ...
    @auther 巷北
    @time 2025.9.20 23:30
    设计了一下,用ListNodes继承SingleNode也不合理.因为ListNodes是组,而SingleNode是单一结点,设计了一下
    发现,还是继承VGroup好,之后再集成相关功能.
    另外,发现继承就必须要带有**kwargs,即使当前并没有东西要加入,因为底层会涉及manim相关的体系构建,都隐藏
    在**kwargs之中.我是clear_points发现报错了,重新添加回**kwargs才没问题.不过目前继承VGroup的话,不会有
    这个问题了,但建议还是要带有**kwargs.
    ...
    @auther 巷北
    @time 2025.9.23 23:14
    怎么说呢,今天打破了原则,像github网站中提交了些文件,然后git pull了...不知道代码是否被覆盖了,所以感觉
    这样做十分不安全啊...还得检查一下这部分代码有没有影响...哎,还是不能打破原则,git提交就一直git提交,本
    地代码可能是最新的,但是不一定会记得提交...
"""


class SingleNode(RoundedRectangle):

    cycle_color = cycle(
        [
            "#FFE4E1",
            "#DDA0DD",
            "#7CFC00",
            "#FFFF77",
            "#33FFFF",
            "#F08080",
            "#5599FF",
            "#FFAA33",
            "#FFC0CB",
            "#BC8F8F",
        ]
    )

    def __init__(
        self,
        corner_radius=0.14,
        height=1.4,
        width=2.1,
        stroke_width=10,
        **kwargs,
    ):
        super().__init__(
            corner_radius=corner_radius,
            width=width,
            height=height,
            stroke_width=stroke_width,
            **kwargs,
        )

        node_normal_color = "#FFE4E1"
        self.set_stroke(color=BLACK, opacity=0.9)
        self.set_fill(color=node_normal_color, opacity=1)

        self.set_info()
        self.scale(0.7)

    def scale(self, scale_factor: float, **kwargs):
        self.remove(self.tex)
        self.set_stroke(width=scale_factor * self.stroke_width)
        self.add(self.tex)
        return super().scale(scale_factor, **kwargs)

    def get_cycle_color(self):
        # 追求的是颜色的专一性还是颜色的多样性?
        cycle_color = cycle(
            [
                "#FFE4E1 ",
                "#DDA0DD",
                "#7CFC00",
                "#FFFF77",
                "#33FFFF",
                "#F08080",
                "#5599FF",
                "#FFAA33",
                "#FFC0CB",
                "#BC8F8F",
            ]
        )
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
            "#BC8F8F": "淡棕色",
        }
        return (cycle_color, list(color_name.values()))

    def set_info(self, info="1", height=0.3, width=None):
        if hasattr(self, "tex"):
            self.remove(self.tex)
            del self.tex

        # todo 无法提供中文文本. 如果需要, 可以再添加, 只是加个判断语句就好了.
        tex = MathTex(info)

        if height is not None:
            tex.set(height=height)
        if width is not None:
            tex.set(width=width)

        if tex.height > self.height:
            tex.set(height=self.height - 0.2)
        if tex.width > self.width:
            tex.set(width=self.width - 0.2)

        tex.move_to(self.get_center())
        tex.set_color(self.stroke_color)
        self.tex = tex

        self.add(tex)
        return self

    def change_info(self, change_info="1", height=0.3, width=None):
        self.set_info(change_info, height, width)
        return self.tex

    def set_node_color(self):
        self.remove(self.tex)
        self.set_fill(color=next(SingleNode.cycle_color))
        self.add(self.tex)
        return self

    def remove_node_color(self):
        node_normal_color = "#FFE4E1"
        self.remove(self.tex)
        self.set_fill(color=node_normal_color)
        self.add(self.tex)
        return self

    def _init_index(self, index, height, direction, buff, color):
        # 解释 设计index
        index = MathTex(f"{index}")
        index.set(height=height).next_to(self, direction, buff=buff)
        index.set_color(color=color)
        self.add(index)
        self.index:MathTex = index

        return index

    def set_index(
        self,
        index=0,
        height=0.2,
        direction=DOWN,
        buff=0.1,
        color=BLACK,
    ):
        index = self._init_index(index, height, direction, buff, color)

        return index

    def remove_index(self):
        if hasattr(self, "index"):
            self.remove(self.index)

