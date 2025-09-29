from manim import (
    Mobject, VGroup, 
    RIGHT, DOWN,
    BLACK,
)
from .single_node import SingleNode
from typing import cast
from typing import Generic, TypeVar
T = TypeVar("T", bound=Mobject)
#_日志 
"""
    ...
    @auther 巷北
    @time 2025.9.21 21:25
    从SingleNode中分支出来,正在做着下一步的规划
    ...
    @auther 巷北
    @time 2025.9.21 19:31
    添加了change_info接口,明白了对象通过add添加后可能会产生的问题.
    ...
    @auther 巷北
    @time 2025.9.26 12:43
    修复了一些小bug,重新测试了一下动画,调用没太大问题.
    更名,将ListNodes更名为SequentialList
    ...
    @auther 巷北
    @time 2025.9.28 14:00
    添加了泛型,使得通过下标访问容器内部,能够明白其元素类型.
"""
#_待办
"""
无   

"""

class SequentialList(VGroup, Generic[T]):
    #_说明
    """
    @auther 巷北
    @time 2025.9.21 21:27
    根据以前打算,这部分需要有一个ListNodeAnimation类来承接动画,并且在内部实例化,但是上面那个类是个单独的类,并没有
    继承Manim底层本身的animation类,所以略微有些突兀.我自己对Animation还有没研究过,也仅仅是了解过,单纯地去继承Animation
    的话,可能把握不准,所以动画方面先搁置一下,等后续了解之后,再去写ListNodeAnimation类,然后再去连接对应的接口,方便动画
    的生成.不过,我在思考,如果为Mobject专门创建动画的话,是否需要在外面专门设置一个Animation文件夹吗?想了想,还是不用.因为
    动画是专门针对这个Mobject的,而不是所有的Mobject,只具有单一性.Animation文件夹需要接受那种实用度高的动画.所以说,动画这
    不分,还是专门放在这个文件里,只针对ListNodes使用,不对外开放接口.
    
    """
    def __init__(
        self,
        num=5,
        ref_length=None,
        infos=None,
        indexes=None,
        isindex=False,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.num = num

        self._init_listnode_grps(num, infos, ref_length)
        if isindex:
            self.indexes = self._init_listnode_index(indexes)

    def _init_listnode_grps(self, num, infos, ref_length):
        if ref_length is None:
            ref_length = 1.342 * num

        if infos is None:
            grps = [SingleNode().set_info(str(info)).set_node_color(info) for info in range(0, num)]

        else:
            grps = [SingleNode().set_info(info).set_node_color(i) for i, info in enumerate(infos)]

        self.add(*grps)
        self.arrange(RIGHT, buff = 0)
        self.set(width = ref_length - 0.2)

    def _init_listnode_index(
        self, indexes=None, height=0.2, direction=DOWN, buff=0.1, color=BLACK
    ):

        if hasattr(self, "indexes"):
            for mob in self:
                singlenode = cast(SingleNode, mob)
                singlenode.remove(singlenode.index)
                    
        if indexes is None:

            index_grps = VGroup(
                *[
                    mob.set_index(index, height, direction, buff, color)
                    for index, mob in enumerate(self)
                ]
            )

        else:
            index_grps = VGroup(
                *[
                    mob.set_index(index, height, direction, buff, color)
                    for index, mob in zip(indexes, self)
                ]
            )
        self.indexes = index_grps

        return index_grps

    def set_indexes(self, indexes = None, height=0.2, direction=DOWN, buff=0.1, color=BLACK):
        indexes = self._init_listnode_index(indexes, height, direction, buff, color)

        return indexes

    def scale_single_node_info(self, index=0, scale_factor=0.4):
        # 可.animate
        node = self[index]
        node.tex.scale(scale_factor)
        return node.tex

    def scale_nodes_infos(self: VGroup, indexes: list, scale_factors: list):
        # 可.animate
        for index, scale_factor in zip(indexes, scale_factors):
            self.scale_single_node_info(index, scale_factor)

    def change_single_node_info(self, index, info:str):
        # 不可.animate

        # 我知道了.因为添加了index,所以作为组的话,整体的重心就会下移,这样就会产生很多问题.
        # 首先,组重心下移,为什么还会影响到子对象的重心?
        tex = self[index].change_info(info)
        
        #todo 其实是设置好了,但也只是缓和了一下.修改内部相关参数,通过add可以
        # 添加,但是动画显示的话,会比较奇怪,所以无法动态改变

        # 想了想,这里还是只是提供静态改变info的方法吧,不提过.animate的方法.因为动态转换的话,
        #可以直接使用Transform或者ReplacementTransform,不用考虑位置关系.

        return tex
    
    def change_nodes_info(self, indexes: list, infos: list):
        # 不可.animate
        for index, info, in zip(indexes, infos):
            self.change_single_node_info(index, info)

    def __getitem__(self, index: int) -> T:
        return super().__getitem__(index) 



