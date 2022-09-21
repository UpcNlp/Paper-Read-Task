**Reinforcement Subgraph Reasoning for Fake News Detection**

**1 引言**

​		在本文中，作者做出了以下技术贡献：
​		（1）提出了一种新型的子图推理框架，用于假新闻检测，通过增强假新闻检测模型的泛化能力和辨别能力，实现了优越的可解释性，提高了准确性。
​		（2）设计了一个分层路径感知核图注意网络，通过对多个异质子图进行细粒度建模，准确检测出假新闻。
​		（3）引入了一种基于课程的优化方法，该方法逐渐增加学习难度，确保收敛到一个更好的解决方案 的学习难度，并确保端到端的训练。

**2 方法**

**2.1 问题的提出**

​		对于一个给定新闻文章的传播网络G，子图建模预测新闻的一个标签y，并且输出了一组子图![image-20220921091201959](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921091201959.png)，这些子图对于预测很重要。

​		**模型输入**。输入的传播网络用![image-20220921091248734](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921091248734.png)表示，其中![image-20220921091321714](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921091321714.png)表示节点集合，同时![image-20220921091329749](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921091329749.png)表示边的集合。按照事实核查的范式，作者考虑了数据的两个部分：新闻文章的主张（claims）和来自社交媒体用于验证主张的证据。如下图Fig.2（a)所示。

![image-20220921090856107](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921090856107.png)

​		待验证的主张是新闻文章的内容。作者用全文本和关键细节来表示主张。文档级别的claim d∈C是一个表示整篇新闻文章节点，句子级别的claim c∈C是一个表示新闻中标题或一个句子的节点。d通过边与句子级别的claims相连。

​		**证据**。用于验证的证据来自推特。作者以微博检索的传统模式去构建证据图。尤其是社交帖子，用户和关键词这三种证据节点的主要类型。帖子P包含推文，推文的回复，或者新闻文章的转推。帖子与回复和转推关系相连。用户U用它们在数据集中的特征来表示，比如粉丝数量，用户参与一个假新闻讨论的次数。用户也与推文回复和转推关系相连接。关键词K由主题模型抽取得到。并且与共现性相关联。 四种类型的节点：claims、帖子、用户和关键词，是根据Fig.2（a)展示的关系相互连接的。构建传播网络G的更多细节在附录中给出。

​		**模型输出**。对于一个给定的传播网络G，可以输出以下内容：一个关于新闻是fake或者real的标签y。一个子图集合![image-20220921092903997](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921092903997.png)用来表示预测出标签y的原因。每一个![image-20220921093008410](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921093008410.png)都是对于虚假新闻检测非常重要的连接子图。

**2.2 子图推理框架**

​		为了通过子图对新闻文章的标签y进行预测，作者提出了一个虚假新闻检测的子图推理框架[ Subgraph reasoning framework for Fake News Detection (SureFact) ]，该框架的数学形式如下所示：

![image-20220921095806771](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921095806771.png)

​		该框架包含两个模块，如下图Fig.2（b)所示。

![image-20220921090856107](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921090856107.png)

​		强化子图生成模块通过使虚假新闻检测的的准确率达到最大来评估重要子图的分布概率![image-20220921090012598](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921090012598.png)。这个模块可以在子图已经存在有真实根据的标签上抽取G的关键部分。此外，它过滤了噪声，并且在接下来可能的后续步骤中进行细粒度建模。

​		细粒度子图建模模块使用作者提出的分层路径感知核心图注意力网络[ Hierarchical Path-aware Kernel Graph ATtention networks (HP-KGAT) ]来学习概率![image-20220921090511408](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921090511408.png)，该模块能够通过集成异构的路径信息来有效的预测标签y，并且对子图内和子图间的关系进行联合建模。

​		最终，作者开发了一个基于课程的优化方法去以一种端到端的方式优化上述两个模块。优化的核心是逐渐增加学习难度，并且确保两个模型的端到端细化。

**2.3 强化子图生成**

​		子图生成的关键是在没有子图事实根据标签的情况下学习![image-20220921094812699](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921094812699.png)。我们通过使虚假新闻检测的期望准确率最大化来生成子图，这种方式可以使用强化学习来实现。作者把衡量预测准确率的奖励函数表示为![image-20220921095546283](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921095546283.png)。作者使用强化学习来直接优化第一个模块的原因如下所述：

![image-20220921095756394](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921095756394.png)

公式2可以从公式1和公式3推导出来。在公式2中，左侧表示期望准确率，右侧表示子图生成的期望奖励。这表明，当作者根据公式3去设置子图生成的奖励R时，他们可以使用强化学习去优化子图生成模型，并且获得虚假新闻检测最优的期望准确率。接下来，作者介绍了他们用于优化奖励的子图生成方法。他首先介绍了如何通过预定义的种子节点去生成一个子图，尤其是作者定义了一个马尔科夫决策过程并且设计了一个子图生成的策略网络。随后作者有介绍了如何在没有预定义的种子节点的情况下将这个方法扩展到多图生成。

**2.4 细粒度子图建模**

​		在生成了子图![image-20220921103040661](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921103040661.png)之后，作者通过在子图上进行细粒度的建模来监测假新闻。这一部分的关键就是通过有效的建模多种异构子图来准确的评估![image-20220921103148256](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921103148256.png)。作者通过扩展核心土注意力网络来实现了这个目标，即使用一各机遇和的注意力机制去聚合有意义的线索，并且被证明是事实核查一个有效的方式。 然而，它是为具有一种类型的节点（文本）的单一图设计的。作者将KGAT扩展到分层路径感知核图注意网络（HP-KGAT)，它整合了异质路径信息，并在节点和子图层面分层应用核注意力来共同建模图间和子图内的连接。接下来，作者介绍了如何对子图内的关系进行建模，如何对子图间的关系进行建模，以及如何结合这两个层次来估计标签y的概率分布![image-20220921103927840](C:\Users\WangZhenqi\AppData\Roaming\Typora\typora-user-images\image-20220921103927840.png)。

**2.5 基于课程的优化**
		子图生成和细粒度建模是紧密纠缠在一起的。理想情况下，子图生成模块将提取信息子图，细粒度建模模块可以利用这些子图来验证新闻的真实性。然而，由于生成策略在开始时并非最佳，最初生成的子图可能是无信息的，并将噪音传播到细粒度子图建模，导致两个模块的参数都不理想。为了应对这一挑战，作者提出了一个基于课程的优化策略。课程学习的基本思想是，从一个简单的任务开始，逐渐增加难度，这通常会导致收敛到更好的解决方案。按照这个思路，作者首先通过提供直接的监督信号，即重要子图的伪标签来提供一个简单的任务。由于两个模块是解耦的，只需要执行监督学习而不是RL，所以学习难度很低。然后，作者通过基于课程的联合优化逐渐增加两个模块之间的合作，最终实现端到端的训练。

