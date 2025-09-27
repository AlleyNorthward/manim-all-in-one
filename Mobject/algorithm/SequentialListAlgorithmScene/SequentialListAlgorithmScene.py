from manim import *
from package.data_structure_nodes.SingleNode import SingleNode
from package.data_structure_nodes.SequentialList import SequentialList
# 修改日志
"""

"""

# 待办
"""

"""
class SqListScene(Scene):
    def setup(self):
        self.camera.background_color = "#cee"

    def init_sq(
        self, 
        array: list = None, 
        ref_length = None,
    ):
        if array is None:
            raise ValueError("不能为空,请传入list对象.")
        elif not isinstance(array, list):
            raise TypeError("必须是list类型对象.")
        else:
            self.array = array
        self.ref_length = ref_length

        size = len(array)
        sqlist = SequentialList(size, ref_length, infos = array)

        return sqlist
    
    # def insert_sq(            可惜,这个得到的是最终结果,我希望的是中间结果,所以没用了
    #     self,
    #     position,
    #     elem
    # ):
    #     size = len(self.array) - 1

    #     for i in range(size - 1, position - 2, -1):
    #         self.array[i+1] = self.array[i]
    #     self.array[position - 1] = elem

    #     return self.array
        
    def updating_sq(
        self,
        sqlist: SequentialList,
    ):  
        self.remove(sqlist)
        del sqlist

        new_array = self.array

        sqlist = self.init_sq(new_array, self.ref_length)
        self.add(sqlist)
    
    def insert_node(
        self,
        singlenode: SingleNode, # 待插入结点
        node_sq: SingleNode, # 线性表中结点
    ):
        self.play(
            ReplacementTransform(node_sq, singlenode)
        )


class SequentialListAlgorithmScene(SqListScene):
    # 说明
    """
        @auther 巷北
        @time 2025.9.26
        深思熟虑了一下,也想出来了个动画结点生成方式.参考模式还是之前那颗树的生成.不过,那颗树怎么生成的?
        通过manim内部的图的添加结点和树枝的思想,第一次算法递归出来整棵树,第二次算法递归出来单一结点的显示.
        换到目前的线性表上来,也是类似思想.对于一个线性表,比如[1,2,3,4,5,6],此时其代表的就是单纯的数据.我们
        可以很容易地获取这些数据,同时,也可以很容易地将这些数据赋值给SingleNode.这样,我们其实就有了抽象数据
        结点,大致如下表示方式[SingleNode(1), SingleNode(2), SingleNode(3)...].我们将对数据的操作,抽象为对
        每一个SingleNode的操作.可是,存在的问题是,如何摆放呢?
        假如用VGroup,操作其submobjects, 似乎没有用,因为manim总会选择其最后的submobjects,前面做了再多的转换,
        也没用,只会看最后一次的.那应该怎么办呢?
        想到两种方式,第一种是用VGroup承接每一次的变化,从上到下依次展示.第二种是使用save_state+become,强行
        扭转内部排列层级.
        为了避免之前混乱思想,这次写这个代码前,用plantuml好好地规划一下,要不然后面总免不了修改.
    """
    
    def Insert_Sq(
        self,
        sqlist: SequentialList,
        position: int,
        singlenode: SingleNode
    ):
        size = len(sqlist) - 1
        for i in range(size - 1, position - 2, -1):
            base = sqlist[i + 1].save_state()
            target = sqlist[i].save_state()
            self.play(
                base.animate.move_to(target.get_center()),
                target.animate.move_to(base.get_center())
            )
            base.become(target.saved_state).move_to(base.saved_state)
            target.become(base.saved_state).move_to(target.saved_state)
            print(base.get_center())
            print(target.get_center())

            # self.updating_sq(
            #     sqlist,
            # )

        # self.insert_node(
            # singlenode,
            # sqlist[position - 1]
        # )






            

