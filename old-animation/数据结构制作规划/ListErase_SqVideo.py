from manim import *

from .VideoText import VideoText
from ..MovingCode import MovingCode
from ..ListNode import ListNode, ListNodeAnimation
from ..MyCurvedLine import MyCurvedLine

from pathlib import Path
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"

class InitBasicEraseMobject:
    # 这里本质上是先将Mobject绘制出来, 但是并未将
    # Mobject放到场景中. 所以是否会浪费时间呢?
    # 不清楚, 测试一下吧.  不用了, 分开了, 因为全部都初始化的话, 存在不知道哪个对象在哪更新的问题, 所以就分开吧.

    def __init__(
            self,
            scene: Scene,
            list_node_animation: ListNodeAnimation
    ):
        self.scene = scene
        self.list_node_animation = list_node_animation
        self.total_text = VideoText()
    
    def get_insert_nodes(self):

        """
            一开始不打算return, 但是如果想要整体移动, 发现只能一个一个地移动
            所以提供接口, 使其能够整体移动. 
            但是, 最好不要将return的对象分开操作, 本意不是这样的
            想单独访问某个对象, 只需要通过self.访问就好.
        """

        move_infos = ["1", "2", "3", "4", "5", "NULL"]
        nodes = ListNode.get_list_node_grps_with_index(self.scene, move_infos)

        self.insert_nodes = nodes[0]
        self.insert_pointer = nodes[1]
        self.insert_single_node = ListNode().set_info("6").set_node_color().next_to(self.insert_nodes, UP, 0.9)

        self.list_node_animation.save_nodes_state(self.insert_nodes)
        self.list_node_animation.save_nodes_state(self.insert_single_node)

        self.insert_curves_line1 = ListNode.get_nodes_curved_arrows(nodes[0], 4, 5)
        self.insert_curves_line2 = ListNode.get_nodes_curved_arrows(nodes[0], 3, 4)

        grps = VGroup(nodes, self.insert_single_node, self.insert_curves_line1, self.insert_curves_line2)

        return grps

    def get_erase_nodes(self, index):

        moving_infos = ["1", "2", "3", "4", "5", "6"]
        nodes = ListNode.get_list_node_grps_with_index(self.scene, moving_infos)
        self.erase_nodes = nodes[0]
        self.erase_pointer = nodes[1]

        self.erase_tex = Tex(self.total_text.CAPTION11, tex_template = TexTemplateLibrary.ctex)
        self.erase_tex.set_color(BLACK).scale(0.7)
        self.erase_tex.next_to(self.erase_nodes[index], DOWN, buff = 0.1)
        
        self.list_node_animation.save_nodes_state(self.erase_nodes)

        grps = VGroup(nodes, self.erase_tex)
        return grps
    


class ListErase_SqVideo:
    def __init__(
            self, 
            scene: Scene
    ):
        
        self.scene = scene
        self.list_node_animation = ListNodeAnimation()
        self.init = InitBasicEraseMobject(scene, self.list_node_animation)

    def first_scene(self):
        self.insert_nodes = self.init.get_insert_nodes()
        self.insert_nodes.shift(UP)

        self.erase_nodes = self.init.get_erase_nodes(1)
        self.erase_nodes.shift(DOWN*1.8)

        self.scene.play(
            Create(self.init.insert_single_node),
        )
        self.scene.play(
            FadeIn(self.init.insert_nodes)
        )

        self.scene.play(
            self.init.insert_single_node.animate.move_to([self.init.insert_nodes[0].get_center()[0], self.init.insert_single_node.get_center()[1], 0]),
            Create(self.init.erase_nodes)
        )
        self.scene.wait()
        self.scene.play(
            Write(self.init.erase_tex),
            self.init.insert_single_node.animate.move_to([self.init.insert_nodes[3].get_center()[0], self.init.insert_single_node.get_center()[1], 0])
        )
        self.scene.wait()

    def second_scene(self):
        
        self.scene.play(
            self.list_node_animation.transform_nodes(self.init.insert_nodes, 4, 5, self.init.insert_curves_line1, "NULL", "5")
        )

        self.scene.wait()

        self.scene.play(
            FadeOut(self.init.insert_curves_line1),
            self.list_node_animation.transform_nodes(self.init.insert_nodes, 3, 4, self.init.insert_curves_line2, "NULL", "4")
        )

        self.scene.wait()

        self.scene.play(
            FadeOut(self.init.insert_curves_line2),
            self.list_node_animation.insert_node(self.init.insert_nodes, 3, self.init.insert_single_node, "6")
        )
        self.scene.wait()

        

        