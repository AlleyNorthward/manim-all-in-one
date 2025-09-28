from manim import *
from package.data_structure_nodes.SingleNode import SingleNode
from package.data_structure_nodes.SequentialList import SequentialList
# 修改日志
"""
    ...
        @auther 巷北
        @time 2025.9.28 11:03
        还没写完呢,也不需要写日志,但是觉得比较重要,还是在这里记录一下.两种交换方式都没问题,但都有些小问题
        整体del的,由于内部信息更新,导致每变换一次,其中两个结点颜色就会改变,可以在颜色统一的情况下使用.第二
        个方法呢,由于我传入了个info为"",导致使用become时,整个结点不可见,转化出问题.解决方式是传入".",然后
        通过scale_single_node_info()接口,缩放比例设为0.01,几乎就不可见了.
        综上来看,如果希望用彩色,就用方法二,如果是单一颜色,就用方法一.
        找了半天有没有分割子场景独立播放的方法,最后发现似乎没有.为什么有这个想法呢,因为写完Insert_Sq之后,发
        现似乎有可能还要添加MovingCode,可是的我play都分发到每一个场景中了,如果要添加MovingCode,并直接放到
        Insert_Sq中,又缺少了最初始的那个味,因为这样又不能单独播放MovingCode了.所以我才想看看有没有分割子场景
        的方法,能不能单独播放.况且,我也不一定是只有MovingCode跟着一起动,其余的参数,也会跟着一起变化的.所以
        这就比较难受了,不知道有几个一块动,哈哈...不过这些也都不是问题,因为最困难的部分是Insert_Sq,实现完了之后,
        可以选择弄些副本,这样就会好很多了...刚才又想到了一个问题,比如我有个ACreature,它在那动,然后边思考Inseret_Sq
        动画,可是我这里的Insert_Sq没有接口,返回的也不是动画,没办法一起play.也只能重新写一个Insert_Sq,在里面的
        play中添加ACreature相关动画.所以说,对于这种复合动画,有没有好的解决方案呢?
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
    
    def insert_sq(            
        self,
        position,
        elem
    ):
        # 这个position默认下标从0开始的.
        # position = position - 1 # 如果想让默认下标从q开始,可以打开这个注释

        size = len(self.array) - 1

        for i in range(size - 1, position - 1, -1): # 这里position需要减一,因为取不到,不像C++可以>=.
            self.array[i+1] = self.array[i]
        self.array[position] = elem

        return self.array

    def move_node(
        self,
        target:SingleNode,
        base:SingleNode,
        transform_time = 2
    ):
        
        base = base.save_state()
        target = target.save_state()
        self.play(
            base.animate.move_to(target.get_center()),
            target.animate.move_to(base.get_center()),
            run_time = transform_time
        )
        base.become(target.saved_state).move_to(base.saved_state)
        target.become(base.saved_state).move_to(target.saved_state)
        base.set_value(target.get_info())
        target.set_value(base.get_info())

        return target
        
    
    def insert_node(
        self,
        singlenode: SingleNode, # 待插入结点
        node_sq: SingleNode, # 线性表中结点
        insert_time = 2,
    ):
        singlenode.save_state()
        node_sq.save_state()
        self.play(
            AnimationGroup(
                singlenode.animate.move_to(node_sq.get_center()),
                FadeOut(node_sq)
            ),
            run_time = insert_time
        )
        singlenode.become(node_sq.saved_state).move_to(singlenode.saved_state)
        node_sq.become(singlenode.saved_state).move_to(node_sq.saved_state)
        node_sq.set_value(singlenode.get_info())

        # 会突然显现.一定要注意,become后,组中对象的引用,就是singlenode了,而singlenode,还在原来位置!!!
        # 一定会忘了,留个念想,这是最关键部分!
        self.remove(singlenode)
    



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
        sqlist: SequentialList[SingleNode],
        position: int,
        singlenode: SingleNode,
        transform_time = 2,
        insert_time = 2,
    ):
        # 目光别太短浅.后续这部分代码,可能会跟随展示代码一起移动,所以可能会添加许多东西.
        size = len(sqlist) - 1
        for i in range(size - 1, position - 1, -1):
            target = self.move_node(sqlist[i], sqlist[i + 1], transform_time)

        self.insert_node(singlenode, target, insert_time)





            

