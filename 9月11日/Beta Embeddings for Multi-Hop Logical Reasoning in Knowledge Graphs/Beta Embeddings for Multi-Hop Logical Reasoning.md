# 《Beta Embeddings for Multi-Hop Logical Reasoning in Knowledge Graphs》

代码：[https://github.com/snap-stanford/KGReasoning](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fsnap-stanford%2FKGReasoning)（包含三种模型，`BetaE`，`Query2box`，`GQE`）

数据集（已下载）：[FB15k]，[FB15k-237、NELL995](https://github.com/wenhuchen/KB-Reasoning-Data)

数据集介绍：[FB15K-237知识图谱数据集的介绍与分析，Freebase](https://norstc.blog.csdn.net/article/details/120125762)，[常用知识图谱数据集FB15K,YAGO,WN18](https://blog.csdn.net/a493823882/article/details/121024510)

原文：[https://arxiv.org/pdf/2010.11465.pdf](https://links.jianshu.com/go?to=https%3A%2F%2Farxiv.org%2Fpdf%2F2010.11465.pdf)

参考博客：https://blog.csdn.net/weixin_44965520/article/details/115550357

问题：

+ KG的规模很大，每跳一步候选答案集的候选答案数量便指数增长，因此通过跳转来寻找答案不现实；
+ 绝大多数的现实世界的KG根本不完全，缺少很多边（关系），因此跳转可能都跳不动，根本无法找到答案

贡献：BetaE是第一个可以在大型异构知识图谱上处理**所有逻辑操作符号**（包括存在、交、或、非，之前主要是无法处理逻辑“非”）的方法，它具有embedding类方法的**隐含归纳关系**的能力、并且可以**建模实体语义的不确定性**，极大的增强了真实世界知识图谱上多跳推理的可拓展性和处理能力。



使用$\beta$分布对entity embedding 进行建模，并提出了relation projection、Intersection、Negation的计算方法。详细建模过程将[参考博客](https://blog.csdn.net/weixin_44965520/article/details/115550357)

![](https://upload-images.jianshu.io/upload_images/13563778-869780a9e7cb41a7.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)



+ 
+ 问题1：如何从输入数据得到计算图？输入的就是计算图吗？
+ 问题2：如何从节点的表征得到实体名称？，相似度计算，然后排序？

