from manim import Scene, Circle, Animation, RIGHT
from manim.renderer.cairo_renderer import CairoRenderer
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)

renderer = CairoRenderer()
scene = TestScene()
scene.render()

renderer.update_frame(scene)

frame = renderer.get_frame()
print(frame.shape)

plt.imshow(frame)  # 如果 float 0~1 可以直接显示
plt.axis("off")
plt.show()

print(renderer.camera.frame_center)