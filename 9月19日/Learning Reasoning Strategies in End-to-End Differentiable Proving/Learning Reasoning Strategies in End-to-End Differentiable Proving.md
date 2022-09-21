# 《Learning Reasoning Strategies in End-to-End Differentiable Proving》

作者：P Minervini, S Riedel, P Stenetorp，Edward Grefenstette， Tim Rocktäschel

代码：[uclnlp/ctp](https://github.com/uclnlp/ctp)

数据集：[CLUTRRS](https://github.com/facebookresearch/clutrr) Countries、Kinship、Nations、UMLS(在代码中存在)

**挑战**

+ 神经网络与基于规则的系统融合，使得模型具备可解性，鲁棒性、data efficient, 但存在计算复杂性高（computational complexity ），搜索空间大的问题

**贡献**

+ 在NTPS（Neural Theorem Provers）的基础上，提出CTPS（Conditional theorem Provers），学习一个优化的规则选择策略。

## **1.问题定义**

参考论文NTPS

![](images/define1.png)

![](images/define2.png)

## **2.End-to-End Differentiable Proving（端到端的可微证明）**

这里的可微可以理解成可细分的，即可以将一个规则细分为多个规则

✔**问题1**:backward chaining （BC）是什么？反向传播链？

从目标（goal）反推，通过规则链寻找支持事实的证据。所以backward chaining 指从目标反推，支持事实的规则链

> NTPS:this algorithm works backward from the goal, chaining through rules to find known facts supporting the proof.

![](images/process.png)

给定一个查询或目标$G$，首先在给定知识图谱中进行事实匹配（可以理解为1 hop?），如果失败，则考虑所有的规则$H:-B$，$H$表示结果，$B$表示前提。

✔问题2：如何理解?

> H can be unified with the query $G$ resulting in a substitution for the variables contained in H

$$
KB(knowledge\ Base) = \{facts,rule\},\ facts = \{p(RICK,BETH) ,\ p(BETH,MORTH)\},\ rule=\{g(X,Y):-p(X,Z),P(Z,Y)\}
$$

$p$ 表示关系$parent$, $g$表示关系$grandparent$。目标$G=g(RICK,MORTY)$能够通过规则$g(X,Y)$证明，即：将$X$使用$RICK$替换，即将$Y$使用$MORTY$替换，之后递归证明子目标：$p(RICK,Z),p(Z,MORTY)$,将$Z$使用$BETH$进行替换。

![](images/example1.png)

![](images/example2.png)

问题3：如何理解Neural Theorem Provers？

![](images/ntps.png)

从论文NTPS中可知，$S(proof\ state)\ =(\psi,\rho)$,

算法理解：$function\ or()$ 表示将目标$G$进行分解，其中d表示递归的深度，即规则链的长度，S表示

## **3.Conditional Proving Strategies**

### 3.1Differentiable Goal Reformulation（目标细分）

NTPS使用一个固定 规则集将目标细分，不适合大型数据集，因此提出：基于神经网络动态生成最小规则集





















