**Improving Fake News Detection of Influential Domain via Domain- and Instance-Level Transfer**

**1 引言**

​		涉及多领域的虚假新闻检测模型总是会出现跷跷板现象，即这些模型在某些领域上的检测效果提升是以损害其他领域上的检测表现为代价的。同时，由于缺乏目标导向设计，所以很难引导多领域模型去提高其在特定目标领域的性能。在这篇论文中，作者致力于跨领域虚假新闻检测，即使用其他领域的新闻来提高模型在一个确定目标领域的检测性能，这种方式相比于多领域模型，能够在目标领域带来额外的收益。

![image-20220922092227477](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922092227477.png)

​		为了解决跨领域虚假新闻检测问题，作者引入了两个观点：迁移领域级别的知识和迁移实例级别的知识。按照这个想法，作者提出了一个领域和实例级别的虚假新闻检测迁移框架DITFEND。

​		为了迁移领域级别的知识，作者从元学习的角度出发，使用多领域的数据去训练了一个通用模型。这个模型包含通用知识，并且能快速的适配到特定领域。为了迁移实例级别的知识，作者首先训练了一个领域适应性语言模型，该模型由目标领域赋予特征。为了衡量源领域中每一个实例对于目标领域的贡献，作者引入了领域适应性语言模型困惑度这个指标来量化这些实例转化能力。最后，为了让模型在特定领域获得较高的性能表现，作者用目标域的实例和源域的加权实例来调整通用模型。

​		这篇论文的贡献：（1）首次研究了目标域多源的跨域假新闻检测的重要性。（2）提出了一个领域和实例级的迁移框架来提高目标领域的假新闻检测。（3）在英文和中文实词假新闻数据集上评估了DITFEND，实验证明了DITFEND的有效性。

**2 相关工作**

​		虚假新闻检测分为基于社交上下文的方法和基于内容的方法两类。有人使用一个领域的知识去辅助预测特定领域的虚假新闻，有人直接结合多领域的知识进行跨领域预测，但性能都不好。作者基于元学习的方法，提出了一个虚假新闻检测框架，做迁移学习。

**3 DITFEND：用于检测假新闻的域和实例级转移**

**3.1 问题声明**

​		跨领域虚假新闻检测是一个目标域![image-20220922101558414](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922101558414.png)和N个源域的集合![image-20220922101621485](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922101621485.png)。每一个领域都有一个新闻集合。对于一则新闻P，用一个标签[CLS]和[SEP]进行额外的填充，然后被编码为m个token![image-20220922101820790](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922101820790.png)，并生成相应的词嵌入向量e。将目标领域的嵌入向量标记为![image-20220922101954750](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922101954750.png)，其他源领域的标记为![image-20220922102006715](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102006715.png)。

​		框架的核心就是使用来自所有领域的新闻去训练一个目标适配性的虚假新闻检测器。该过程被分为三个阶段。在第一阶段，作者通过所有领域的新闻训练了一个通用模型，该模型能减缓跷跷板现象。在第二阶段，作者评估并且量化了源域实例的转化能力。在第三阶段，作者将通用模型迁移到特定领域。

![image-20220922102305006](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102305006.png)

**3.2 通用模型训练**

​		对于领域等级的迁移，作者借助元学习的优势，训练了一个通用模型![image-20220922102413726](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102413726.png)来聚合所有领域的知识。

​		在每一轮迭代参数更新中，作者抽取一批训练任务![image-20220922102516158](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102516158.png)，并且对于每一个训练任务![image-20220922102536893](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102536893.png)，作者将它们拆分为两个不相交的集合：一个支持结集合![image-20220922102602243](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102602243.png)以及一个查询集合![image-20220922102617958](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102617958.png)。模型使用支持集合的样本进行训练，并使用支持集合样本的交叉熵损失得到反馈。

![image-20220922102724029](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102724029.png)

​		其中![image-20220922102740908](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102740908.png)是当前支持集合中的数据表编号。并且使用![image-20220922102841006](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922102841006.png)通过梯度下降优化当前任务![image-20220922105955649](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922105955649.png)的参数。

![image-20220922110001040](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110001040.png)

![image-20220922110013886](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110013886.png)是当前模型训练任务![image-20220922110024874](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110024874.png)的优化参数。

​		接下来使用查询集合![image-20220922110047722](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110047722.png)中的样本对模型进行测试。通过![image-20220922110110794](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110110794.png)的损失对模型进行优化。

​		![image-20220922110145361](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110145361.png)

![image-20220922110209921](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110209921.png)是当前查询集合中的数据表编号。

​		在![image-20220922110236057](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110236057.png)上的测试误差被看做是元学习过程的训练误差。

​		在训练过程结束之后，对参数![image-20220922110327786](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110327786.png)进行更新：![image-20220922110336338](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110336338.png)

​		β是元学习过程的学习率，通用模型训练具体算法如下所示：

![image-20220922110416059](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922110416059.png)

**3.3 可迁移性度量**

​		为了赋予语言模型以目标领域的知识，作者在目标领域上执行掩蔽语言建模任务，以得到一个领域自适应的语言模型。这个训练语言模型的第二阶段可以为基于语言模型的后续任务带来显著的性能改进。而且作者利用领域自适应语言模型来评估源实例的可迁移性。

**领域适应性语言模型训练。**用![image-20220922112305183](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112305183.png)表示目标领域T的一个新闻数据集，其中![image-20220922112337999](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112337999.png)是数据集![image-20220922112345568](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112345568.png)中包含n个tokens的新闻。作者使用与训练BERT模型相同的掩码规则去对![image-20220922112424584](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112424584.png)生成掩码。训练的目标就是语言模型对掩码的预测所得的损失最小化。![image-20220922112510290](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112510290.png)

其中![image-20220922112520935](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112520935.png)是语言模型的参数。执行完特定领域掩码语言模型任务之后，就可以认为为语言模型赋予了目标领域里有效的知识。

**困惑度。**困惑度是一个衡量语言模型预测句子性能好坏的指标。作者从另一个角度来使用困惑度这一指标-一个语言模型越能预测一个句子，这个句子就越符合语言模型中所赋予的知识。因此，计算语言模型在给定样本上的困惑度来量化样本的可迁移性是很直观的，也就是说，困惑度越低说明可迁移性越强。

让![image-20220922113328824](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113328824.png)表示源数据集，让包含m个tokens的![image-20220922113349831](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113349831.png)表示![image-20220922113410070](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113410070.png)中的一则新闻，使用[CLS]和[SEP]对tokens进行填充。![image-20220922113459264](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113459264.png)是通过mask句子中的一个单词所生成的掩码句子。

![image-20220922113530170](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113530170.png)

目标适应性语言模型用于预测[MASK]位置正确的单词![image-20220922113739416](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113739416.png)。![image-20220922113751463](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113751463.png)

在计算了句子中所有单词的概率之后，整个句子上困惑度的计算如下所示。

![image-20220922113835591](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113835591.png)

为了表示目标适应性语言模型应用在不同领域上的差异，作者计算了不同领域适应性语言模型在源实例上的困惑度。并且进行了展示。

![image-20220922113954934](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922113954934.png)

图中可以看出，针对中文和英文数据集有明显的差异。

元领域的可迁移性被通过以下公式量化![image-20220922114109865](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922114109865.png)。

w表示样本的可迁移性指标。通过这种方式，作者对源实例的可转移性进行量化，也就是说，对具有较低困惑度的样本赋予更大的权重。

**3.4 目标领域适配**

​		在上一部分中，作者为源域中的每个样本赋予了一个权重值来表示它的可迁移性。为了充分利用源域样本，作者基于可迁移性做了一个重新平衡，与目标域样本一起训练通用模型。

​		作者使用经过元学习训练的通用模型，并且通过以下方式使模型的交叉熵损失最小化：

![image-20220922112059321](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112059321.png)

其中y是真实标签，![image-20220922112110281](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112110281.png)是预测到的标签，![image-20220922112123719](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220922112123719.png)是上一节中所获取的实例的可迁移性指数。

