## 2022.10.13
done:算子配置和数据绑定


## 2022.10.14
done:
不同的算子渲染兼容问题
某些算子拖拽不进去问题
算子类型和输入框匹配问题
优化算子配置，增加新字段：condition_field_wrap

issue:
  1.级联算子渲染有问题，例如intersection
  2.列表怎么输入？格式规范？
  3.json怎么输入？格式规范？

## 10.17
验证算子的渲染和数据校验关系，重新配置算子config，解决算子多层关系渲染问题。

issue:
删除算子的时候，配置没有从configJson里面删除，，，，done



1.

![image-20221017162037046](C:\Users\song\AppData\Roaming\Typora\typora-user-images\image-20221017162037046.png)

工作流可以拖进两个data_transform_2:先拖一个data_transform_1，然后再拖一个data_transform_2,然后删掉data_transform_1,
再拖进来一个data_transform,就会变成data_transform_2,从而导致他们两个共用同一个configJson，





2.工作流保存按钮权限问题：时有时无，原因：vuex中的项目详情没有做持久化 done

![image-20221017164320935](C:\Users\song\AppData\Roaming\Typora\typora-user-images\image-20221017164320935.png)



3.federatedSample无法保存bug

7.HeteroFeatureSelection需要重新配置，要有级联





隐匿求交接口：李澍楠，赵豪杰

![image-20221107102835949](C:\Users\song\AppData\Roaming\Typora\typora-user-images\image-20221107102835949.png)



![image-20221121162652791](C:\Users\song\AppData\Roaming\Typora\typora-user-images\image-20221121162652791.png)

![](https://img-blog.csdnimg.cn/fa978e0142744704b2602a9d8b9999ef.png)

![image-20221121162935848](C:\Users\song\AppData\Roaming\Typora\typora-user-images\image-20221121162935848.png)

![image-20221121162843513](C:\Users\song\AppData\Roaming\Typora\typora-user-images\image-20221121162843513.png)

