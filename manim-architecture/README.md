# 简述

这里会存放manimce版本的架构模式

需要注意的是,manim本身有很多很多的拓展类,而这些需要等后续整体上规划完成之后,再分析的.所以目前考虑的类是Scene, Camera, Mobject, VMobject, CairoRenderer(Opengl先不分析,以Cairo为主), Animation.

## 为什么要考虑架构

- 之前研究manim,缺少宏观架构,只是对单一类/方法分析.
- 逐渐熟练后,发现,类中有很多函数嵌套函数的方法,搞的我也