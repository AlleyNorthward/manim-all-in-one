import numpy as np
import matplotlib.pyplot as plt
from manim import Scene, Circle, RIGHT
from manim.renderer.cairo_renderer import CairoRenderer

# 创建一个简单的 Scene
class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.play(circle.animate.shift(RIGHT))
        self.wait(1)

# 初始化渲染器
renderer = CairoRenderer()

# 创建测试场景
scene = TestScene()
scene.setup()  # 初始化 scene 的内部状态

# 初始化渲染器与 scene 的文件写入器
renderer.init_scene(scene)

# ----------------------------
# 1. 测试 update_frame
# ----------------------------
# 更新当前帧，只渲染场景中的所有 mobjects
renderer.update_frame(scene)
frame = renderer.get_frame()
print("update_frame 输出的帧形状:", frame.shape)

# ----------------------------
# 2. 测试 save_static_frame_data
# ----------------------------
# 保存静态 mobjects（例如不动的对象）
renderer.save_static_frame_data(scene, scene.mobjects)

# ----------------------------
# 3. 测试 add_frame
# ----------------------------
# 添加当前帧到“视频流”
renderer.add_frame(frame, num_frames=5)
print("添加 5 帧完成，总时间:", renderer.time)

# ----------------------------
# 4. 测试 freeze_current_frame
# ----------------------------
# 冻结当前帧持续 2 秒
renderer.freeze_current_frame(duration=2)
print("冻结帧后的总时间:", renderer.time)

# ----------------------------
# 5. 测试 render
# ----------------------------
# render 会更新帧并直接添加到视频
renderer.render(scene, time=0, moving_mobjects=scene.mobjects)

# ----------------------------
# 6. 显示当前帧
# ----------------------------
renderer.show_frame()  # 会打开默认图片查看器显示帧

# ----------------------------
# 7. 完成场景渲染
# ----------------------------
renderer.scene_finished(scene)
