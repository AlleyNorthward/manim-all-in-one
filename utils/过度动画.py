from manim import(
    VGroup, Dot, 
    Write, Unwrite,
    DOWN, UP, RIGHT, 
    GREEN_A,
    Scene,
)
def dot_transition_animation(
        scene: Scene, 
        color = GREEN_A,
        scale_factor = 6,
        dot_offset = 0.1,
        count = 80,
        up_direction = UP*2,
        down_direction = DOWN*2,
        duration = 4,
        run_time = 2, 
):
    count = int(round(count / 2, 0))
    s = VGroup(*[
        Dot().shift(i*dot_offset*RIGHT).scale(scale_factor).set_color(color)
        for i in range(-count, count)
    ])

    s2 = s.copy()
    s2.invert()

    s.shift(up_direction)
    s2.shift(down_direction)

    scene.play(
        Write(s),
        Write(s2),
        run_time = run_time 
    )

    scene.wait(duration)

    scene.play(
        Unwrite(s),
        Unwrite(s2),
        run_time = run_time
    )
