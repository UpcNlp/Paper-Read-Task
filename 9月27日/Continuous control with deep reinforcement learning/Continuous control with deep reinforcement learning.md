# 《Continuous control with deep reinforcement learning》

作者：Timothy P. Lillicrap, Jonathan J. Hunt

代码：

参考：[Actor Critic](https://www.jianshu.com/p/9632f10bc590)，

贡献：提出的一种用于输出确定性动作的算法，它解决了Actor-Critic 神经网络每次参数更新前后都存在相关性，导致神经网络只能片面的看待问题这一缺点。同时也解决了DQN不能用于连续性动作的缺点。

## 1.Actor-Critic网络

以下内容来自：[Actor-Critic 2](https://www.jianshu.com/p/555c46348fb4)

>  ![V_\pi(s)](https://math.jianshu.com/math?formula=V_%5Cpi(s))代表使用actor ![\pi](https://math.jianshu.com/math?formula=%5Cpi)在遇到某一状态s后，接下来使用actor![\pi](https://math.jianshu.com/math?formula=%5Cpi)一直玩到游戏结束的cumulated reward的期望值。
>  ![Q_\pi(s,a)](https://math.jianshu.com/math?formula=Q_%5Cpi(s%2Ca))代表使用actor ![\pi](https://math.jianshu.com/math?formula=%5Cpi)在遇到某一状态s后，强制使用a，接下来使用actor![\pi](https://math.jianshu.com/math?formula=%5Cpi)一直玩到游戏结束的cumulated reward的期望值。
>
> ![](https://upload-images.jianshu.io/upload_images/2635859-45844c7824937537.png?imageMogr2/auto-orient/strip|imageView2/2/w/755/format/webp)

没太看明白，需要补充**actor-critic, Policy Gradients， TD 和 MC**的内容。





