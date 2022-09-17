**Improving Fake News Detection by Using an Entity-enhanced Framework to Fuse Diverse Multimodal Clues**

​		现有的多模态FID方法大多只是对图像的基本语义进行初步建模，作为文本的补充，忽略了多模态假新闻的特点。为了弥补这一遗漏，该论文探索了多模态假新闻中的三种有价值的文本图像相关性，它们提供了多种多模态线索，分别是：

​		（1）文本和图像具有不一致的实体，简单的将图像作为特征来对文本进行补充，无法发现这种不一致性。

​		（2）文本和图像通过重要特征而相互增强。比如文本讲述主要线索，图片中的实体可以作为文本内容中的关键线索。

​		（3）图片中的嵌入文本作为原文本的补充，用图片的嵌入文本来传播虚假信息，原文本内容只是对所述事件的评论。

​		多模态数据混合还面临一个挑战，就是图片处理模型只能提取一部分图片特征，而文本处理模型可以提取更高层次的语义特征，这两种特征融合过程中存在语义鸿沟。因此这篇论文创造性的从图片中提取了人物或地点实体，以及视觉概念作为更高层次的语义特征提取，以此来适配图片和文本更高层次语义特征的融合。基于上述内容，论文提出了一个叫做EM-FEND (Entity-enhanced Multimodal FakE News Detection) 的框架。在多模态特征提取阶段，该框架可以提取图片中的实体信息和图片中嵌入的文本，以及纯新闻文本中的实体信息。在多模态特征融合阶段，框架对对多模态假新闻中的三种交叉模态相关行进行建模，以融合不同的多模态线索进行检测，具体表现为：①框架对原文本和嵌入文本进行了拼接，作为新的文本；②框架通过  co-attention transformers 来对文本实体、图片实体还是有图片特征进行交互增强；③框架通过计算文本实体和图片实体的相关性来衡量实体不一致性。最后，在分类阶段，将融合的多模态特征用于区分假新闻和真实新闻 。

​		现有研究存在两个主要缺陷：①他们没有同时考虑这三种跨模态相关性，完全忽略了原始文本和嵌入文本之间的文本互补；②基于图像的基本语义特征对跨模态相关性进行建模，忽略了与新闻相关的高级视觉语义。所以论文显式提取视觉实体，并基于多模态实体建模多模态不一致性和交互增强。

​		EM-FEND包括三个模块，用于融合不同的多模态线索进行假新闻检测：①多模态特征提取：提取文本和视觉信息实体、图像中的嵌入文本和视觉CNN特征；② 多模态特征融合：建模三种类型的跨模态相关性，包括实体不一致性、相互增强和互补；③分类：使用获得的多模态表征来执行二进制分类。模型架构如下图所示：

![image-20220914151727655](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914151727655.png)

**1 多模态特征抽取**

**1.1 文本输入**

​		框架通过识别文本中相应的专有名词来显式提取人物实体PT和位置实体LT。为了更好地理解新闻事件，框架使用词性标记提取所有名词作为一般文本上下文CT。

**1.2 图像输入**

​		视觉CNN特征：与已有的工作相同，框采用VGG19来提取视觉特征。但不同之处在于，该框架对给定数据集上的预训练VGG19进行微调，以灵活地捕获来自特定数据源的图像的低级特征，以帮助检测。考虑到图像中的不同区域可能显示不同的模式，框架将原始图像分割为7×7个区域，然后获得相应的视觉特征序列HV=[r1，…，rn]，n=49，其中ri表示图像中第i个区域的特征。 

​		视觉实体：框架提取了四种类型的视觉实体：①名人和地标；② 组织；③ 引人注目的视觉概念，如暴力、血腥和灾难；④一般对象和场景。他们使用了公共APIs3来检测视觉实体，而不是重新实现这些模型。最后，获得了人物实体PV、位置实体LV和其他与新闻相关的视觉概念，并将其作为更一般的图像上下文CV。

​		嵌入文本：框架通过OCR模型提取输入图像的嵌入文本O。

**2 多模态特征融合**

**2.1 文本补充**：框架将原始文本T和嵌入文本O输入到由[SEP]分隔的预训练的BERT，即![image-20220914150442167](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914150442167.png)，然后获得文本特征![image-20220914150455153](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914150455153.png)，其中wi表示合成文本中第i个单词的特征，n表示合成文本的长度。

**2.2 相互增强**

​		文本和图像可以通过彼此对齐分别发现重要特征。框架使用具有视觉实体的文本特征和视觉CNN特征之间的多模态共同注意Transformer来模拟不同视觉水平的多模态对齐。

​		（1）多模态共同注意力Transformer（Multimodal Co-attention Transformer，MCT）：框架使用双流Transformer同时处理文本和视觉信息，并修改标准查询条件键值注意里机制，以开发多模态共同注意力Transformer模块。来自每个模态的查询被传递到另一模态的多头注意力块，因此该变换器层产生图像增强的文本特征和文本增强的视觉特征。

​		（2）文本特征和视觉实体之间的MCT （MCT between Textual Features and Visual Entities）。在获得视觉实体![image-20220914151524032](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914151524032.png)之后，框架使用预训练的BERT来获得它们的嵌入![image-20220914151345612](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914151345612.png)。框架使用多模态共同注意力Transformer来融合对齐的词和视觉实体的特征，即框架将文本特征HT和视觉实体特征HV E输入架构图中的第一个共同注意力 Transformer中，获得由视觉实体增强的文本表示![image-20220914151436425](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914151436425.png)和文本增强视觉实体表示![image-20220914151450185](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914151450185.png)，然后对后者应用平均运算，获得视觉实体![image-20220914151510418](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914151510418.png)的最终表示。

​		（3）文本特征和视觉CNN特征之间的MCT。视觉CNN特征用于捕捉全局低级视觉特征。框架为第二个共同注意力Transformer输入![image-20220914152451264](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914152451264.png)和视觉CNN特征![image-20220914152539278](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914152539278.png)，获得由视觉实体和视觉CNN特征增强的文本表示![image-20220914152607243](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914152607243.png)和文本增强视觉表示![image-20220914152620840](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914152620840.png)，然后在对上述特征进行平均运算，以分别获得文本和图像的最终表示，即![image-20220914152646953](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914152646953.png)。

**2.3 实体不一致性度量**

​		框架将t和v定义为文本和视觉实体的特征向量。对于带有Tp和Vp的新闻帖子，跨模态实体相似度计算公式为 

![image-20220914153601781](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914153601781.png)

​		其中p（v）表示视觉实体v的概率。对于缺乏文本或视觉实体的新闻，框架将相似度设置为1，以表示没有关于假新闻检测的多模态不一致性的有效线索。类似地，框架计算跨模态位置相似度![image-20220914153732082](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914153732082.png)和上下文相似度![image-20220914153741959](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914153741959.png)，然后将它们连接起来形成实体一致性特征![image-20220914153752617](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914153752617.png)。 

​		最后，框架将文本xt的最终表示、视觉实体xve的最终表示，图像xv的最终表示和多模态实体一致性特征xs连接起来，以获得最终多模态表示 

![image-20220914153835293](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914153835293.png)

**3 分类**

​		最后对xm做一个全连接层和Softmax，利用二元交叉损失函数作为损失函数，预测新闻为真或假。

![image-20220914154235106](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914154235106.png)

![image-20220914154243525](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220914154243525.png)