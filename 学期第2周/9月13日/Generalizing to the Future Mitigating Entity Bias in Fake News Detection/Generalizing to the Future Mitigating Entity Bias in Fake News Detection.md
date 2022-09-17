**Generalizing to the Future: Mitigating Entity Bias in Fake News Detection**
**（通过缓解虚假新闻监测中的实体偏差来提高模型在未来预测中的泛化能力）**

1. 概述

​		真实的虚假新闻检测系统一般都是基于过去的新闻数据训练模型，来检测未来数据中的假新闻。但是，在传统的FID模型训练过程中，模型往往会针对新闻中的某些实体对新闻的真实性进行预测。随着时间推移，一些实体在早期的新闻中可能会增加新闻的真实性，但是在未来却会降低新闻的真实性，因此训练好的模型在未来新闻预测工作中的泛化能力往往会大幅降低。

​		这篇论文提出了一种消除实体偏颇的方法，并提出了一个实体去偏假新闻检测框架 Entity Debiasing Framework （ENDEF）。论文从因果的角度来缓解模型学习中的实体偏差问题，在训练阶段对训练集中所蕴含实体偏差显式建模，并在测试阶段直接移除实体相关支路，削弱实体对预测结果的影响，从而实现实体去偏条件下的新闻真实性预测。如下图所示：

![image-20220913214447086](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214447086.png)

2. 实体去偏假新闻检测框架ENDEF

![image-20220913214546920](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214546920.png)

​		设一则新闻 P 里包含 n 个token，定义为

![image-20220913214623555](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214623555.png)

​		同时该新闻包含 m 个实体：

![image-20220913214636294](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214636294.png)

​		模型同时建模两个因果路径，一个是从实体到标签：![image-20220913214720823](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214720823.png)

​		另一个是从实体到新闻内容再到标签：

![image-20220913214731331](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214731331.png)

​		在训练阶段，依据这两个部分的概率预测为：

![image-20220913214745679](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214745679.png)

​		采用交叉熵进行整个框架的训练：

![image-20220913214759211](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214759211.png)

​		并且使用一个辅助损失，应用额外的监督训练在基于实体的模型上。

![image-20220913214813282](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214813282.png)

​		因此，总的训练流程包含两个损失函数：

![image-20220913214833209](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220913214833209.png)

​		在训练过程中，基于实体的模型重点关注于提供的实体来检测假新闻，从而很好地适应训练集中的实体偏差。同时，它通过使用两个模块捕捉分别基于实体和非基于实体不同的信号，使假新闻检测器能够学习到较少的偏颇信息。在推理阶段，为了减缓实体偏差从而实现更好的泛化能力，关键是移除实体直接的影响。所以，直接使用不包含基于实体的模型输出的结果作为推理阶段的预测。

3. 展望

​		（1）将无偏模型适配到未来的新闻环境；

​		（2）探索不同时间段新闻之间的共性特征。