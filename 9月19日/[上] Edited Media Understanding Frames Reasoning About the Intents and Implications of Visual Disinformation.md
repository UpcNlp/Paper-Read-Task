**Edited Media Understanding Frames: Reasoning About the Intents and Implications of Visual Disinformation**

**2 Edited Media Understanding Frames的定义与任务概述**

​		对于一个给定的编辑![微信图片_20220919194046](images\微信图片_20220919194046.png)（其中IS表示原图片，IE表示编辑后的图片），作者把Edited media understanding frame![微信图片_20220919194201](C:\Users\WangZhenqi\OneDrive\桌面\images\微信图片_20220919194201.png)定义为一个类型化维度和极性赋值的集合：（1)physical P（Is -> IE) 表示IS到IE之间的变化；（2)intent N（E->IE)：指IS到IE之间是否存在不好的意图；（3)implication M（E->IE)：表示编辑者将如何通过IE去误导人们；（4)mental state S（IE->si)：表示IE是否会影响si的情绪；（5)effect E（IE->si)：表示IE对于si的影响。假设框架可以被分类为有害和无害两极I∈{+， -}，每个机型I都可以被原因y解释，并且每个原因都有一个基本原理r所支持。

​		所以，相应的模型就会有以下输入：（1）一个原图片IS，一个被修改过的图片IE；（2）用边界框框出来的一些重要主题；（3）一个与F(*)相关的开放性问题q；（4）一系列表示图片中的主体是被引入还是被修改的注解框ai∈IE，以及一个表示背景是否被修改的true/false标签。

​		一个模型必须预测极性分类I‘∈{+, -}，极性结果的解释y'，以及基本原理r‘。

**3 EMU：一个Edited Media Understanding Frames语料库**

​		收集图片编辑：作者从Reddit社区收集了八千对图片编辑，并手工整理出来了超过100个在PS比赛帖子里经常出现的术语，然后他们筛选了十万个包含一到两个术语的帖子，从帖子里手机到了两万个图像对。此外，作者使用一个对象探测器去确保每张图片至少出现了一个人物。

​		注解图像编辑：作者找了一群众包工人去标注图片编辑中的主要主题并用自然语言回答开放性得问题，每张图片有三个众包工人去独立标记。众包工人首先会从被编辑的图片中按顺序看到一组由Mask R-CNN标记出来的人物边界框，并且要求选择重要的人物。一旦众包工人选择了人物，他们就需要从第2部分所讲的五个维度去给出分类标签，并且为五个维度提供一个随意的回答。最后，作者从众包工人所识别的图片中区分出图片中的那些实体是引入的，哪些实体是被修改过的。

**4 建模Edited Media Understanding Frames**

**4.1 PELICAN模型**

​		作者通过图传播原理去建模图片区域的重要性。作者问题中提到的主体为根节点，在修改图像中对所有区域建立一个有向图，然后在对图进行拓扑排序。拓扑排序之后，就获得了区域的位置嵌入。位置潜入可以使模型选择性的注意到重要的图像区域。另一方面，作者对原图像中应用了不同的位置嵌入策略，并且没有使用图传播。这种独立的嵌入方式捕获了归纳偏差，即编辑的内容比来源更重要。

**4.2 模型细节与Transformer集成**

​		作者使用主干网络提取器φ从IS和IE中分别抽取N个区域即[s1,...,sN]=φ(IS)，[e1,...,eN]=φ(IE)，然后将语言表示与[s1,...,sN]和[e1,...,eN]相加，输入Transformer主干T，即[z1...zN+L]=T([s1,...,sN],[e1,...,eN],[x1...xL])。

**4.2.1 基于拓扑排序的优先级嵌入**（这一部分实在是没看懂...）

​		Transformer需要在每个图像区域和单词中添加位置嵌入，使其能够区分哪个区域是哪个区域。于是作者将拓扑顺序加入到了[e1,...,eN]中。

​		图的定义：作者对编辑过的图像中的图像区域的图定义如下：作者首先寻找一个种子区域s∈{e1...eN}。让G=(V,E)，其中每个v∈V代表某个ri∈φ(IE)的元数据，为简单起见，定义为vi∈m(IE)。

​		令vi = {x1, y1, x2, y2, si, li}，其中，x1, y1, x2, y1代表ri的边界框，si∈{1, 0}表示ri是否是IE的主体，li∈{引入，改变}表示ri的标签。作者以迭代的方式建立图：对于每个迭代，都定义一条边e = {v, u}; u∈V：∀v∈m(IE), ∀u∈V, E = E ∪(u, v) ∈E0 
​		作者将E0定义为边(u，v)的集合，其中u和v在符号上是相似的。作者定义了三种情况：如果si∈ui∧s j∈v j，如果li∈ui=l j∈v j，以及如果x1，y1，x2，y2∈ui和x3，y3，x4，y4∈ui重叠，其中重叠的百分比由标准的相交-相合来定义。
​		( min{x4, x2} - max{x3, x1})/(min{y4, y2} - max{y3, y1})
​		作者将传出的边的数量限定为3条，并通过只允许通往未见过的图像区域的边来防止循环。在有三个以上可能的边的情况下，作者按照上一段定义的顺序添加边，并通过最大重叠度打破重叠关系。
​		为了产生嵌入，作者在有向图上运行拓扑排序，给每个图像区域分配一个嵌入，然后根据有序索引给每个图像区域分配一个嵌入。对于在有向无环图和源图像中缺失的图像区域，嵌入被清零。为了生成文本和分类标签，作者将嵌入附在编码器-解码器结构的输入上。