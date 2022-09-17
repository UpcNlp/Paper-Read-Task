# 《Deep sets》

论文地址：[https://paperswithcode.com/paper/deep-sets](https://paperswithcode.com/paper/deep-sets)

代码：[DeepSets](https://github.com/manzilzaheer/DeepSets)、[pytorch-deep-sets](https://github.com/yassersouri/pytorch-deep-sets) [deepsets-digitsum](https://github.com/dpernes/deepsets-digitsum)

作者：Manzil Zaheer , Satwik Kottur, Siamak Ravanbhakhsh, Barnabás Póczos , Ruslan Salakhutdinov , Alexander J Smola

参考：[NIPS 2017《Deep Sets》论文翻译与阅读笔记](https://zhuanlan.zhihu.com/p/368357090)



**集合神经网络**：输入或输出为置换不变集（permutation invariant sets），而不是fixed dimensional vectors

**贡献**：

+ 提出一个通用的框架（DeepSets）去处理集合输入，show that the properties of this architecture are both necessary and sufficient。
+ 扩展了该架构，以允许对任意对象进行条件处理
+ 开发了一个深度网络能够处理不同大小的集合
+ 提出一种简单的参数共享方案可以对有监督和半监督场景中的集合进行一般处理
+ 对各种问题的实验证明了框架的广泛适用性



建议直接看论文解析：[NIPS 2017《Deep Sets》论文翻译与阅读笔记](https://zhuanlan.zhihu.com/p/368357090)

Deep sets 主要应用在输入数据为集合，构建了一个置换不变的框架，处理集合中的元素相同，但排列不同的情况。