from manim import *
from package.data_structure_nodes.SingleNode import SingleNode
from package.data_structure_nodes.SequentialList import SequentialList
# 修改日志
"""

"""

# 待办
"""

"""

class SequentialListAlgorithm:
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
    pass
