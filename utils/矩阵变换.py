from manim import *
# 思考一下，哪些是暴露出来的接口，供用户输入
# 我现在只想输入mobject，变换矩阵，分段数目，分段位置
# 然后直接输出变换后的mobject，而且不改变输入的mobject

def apply_matrix(points, matrixes, steps, about_point = ORIGIN):
    for index, matrix in enumerate(matrixes):
        matrixes[index] = np.array(matrix)
        matrix = np.array(matrix)

        if matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = matrix
            matrixes[index] = new_matrix
        elif matrix.shape != (3, 3):
            raise ValueError("不是三阶矩阵.")
        
    for matrix, step in zip(matrixes, steps):
        for index, point in enumerate(points[step[0]:step[1]], start=step[0]):
            points[index] = np.dot(point - about_point, matrix.T) + about_point

def change_mobject_flexible(mob:Mobject, matrixes, start = 0, end = 0.5, N = 16):
    # 本来想使用start，end来增添随机性，但现在不可行了。
    # start和end只能为0/0.5或0.5/1
    # 因为最后还是需要对mob.points操作，但是问题就在这里
    # 对半操作没问题，可是如果选择部分，或者自定义选择，就产生问题
    # 因为mob.points操作的是手柄和锚点，内部有一定关系，
    # 随意操作会产生问题。
    # 为了避免问题，只能将start、end定义为上面的数
    # 不过，我们可以通过对矩阵的操作或者细分，来达到控制效果。
    isup = False
    if start == 0:
        isup = True

    new_mob = mob.copy()
    t_vals = np.linspace(start, end, N)
    points = np.array([new_mob.point_from_proportion(t) for t in t_vals])

    parts = len(matrixes) # 4  5
    points_length = len(points) # 20 32

    if_info = round(points_length/parts, 0)
    step = []
    steps = []

    for i in range(points_length + 1):
        if i % if_info == 0:
            step.append(i)
        
        if len(step) == 2:
            
            steps.append(tuple(step))
            step.clear()
            step.append(i)

    print(points_length)
    apply_matrix(points, matrixes, steps, about_point = mob.get_center())

    smooth_path = VMobject().set_points_smoothly(points).match_style(mob)

    if isup:
        new_mob.set_points(
            new_mob.points[16:]
        )
    else:
        new_mob.set_points(
            new_mob.points[:16]
        )

    mobject = VGroup(smooth_path, new_mob)
    return mobject


class Test(Scene):
    def construct(self):
        circle = Circle().set_fill(opacity=1)
        matrixes = [
            [[1, 0],
             [0, 0.9]],
             [[1, 0],
              [0, 0.8]],
             [[1, 0],
              [0, 0.7]],
              [[1, 0],
               [0, 0.6]],
               [[1, 0],
                [0, 0.5]],
                [[1, 0],
                 [0, 0.4]]
        ]
        changed_circle = change_mobject_flexible(circle, matrixes, N = 16, start = 0.5, end = 1)
        self.add(changed_circle)

%manim $_RF Test

