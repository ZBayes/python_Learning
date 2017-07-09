# 处理缺失数据
## 摘要
海量的数据中可能存在缺失数据，这会对数据分析带来很大困难。在数据量较大的情况下，我们无法逐一地对数据的缺失性进行批量检验和补充，此时就需要利用特定工具和算法进行批量地、自动化地填充。本文利用Python语言作为工具，以拉格朗日插值法为例解决数据缺失的问题。

## Abstract
There always exists the problem of missing data, which may be a big challange for us researcher. However, in most cases, we can't detect all the missing data and try to fix them because the volume of data. Therefore, paticular tools and algorithm is needed to solve that problem automatically. In this blog, Python is used as an excellent to detect the missing data and to fixing it with the help of Lagrange Function. 

## 数据缺失问题
在数据记录、数据传输、数据存储等过程中都可能出现问题，这就很可能导致我们手上的数据存在各种问题，其中常见的一种就是数据缺失，因为某种原因，该位置本应该有数据却没有，用具有缺失的数据集进行计算时，很可能会导致诸如计算移位（转为顺序表时数据会被顺延插入而导致移位）、数据异常（部分计算中可能会将缺失数据默认转为0）、程序报错（无法计算空数值）等问题，所以在数据预处理阶段需要对缺失的数据进行严格处理。

## 数据缺失的常见处理方法
- 将整条数据删除。这种方法的优势就是简单，但是删除整条数据会导致该条数据的其他位置数据无法被使用，如果数据缺失比较严重，此时删除数据将会导致数据集中的数据量严重减少而无法完成后续实验。
- 填充数据。在数据缺失比例较小的情况下，运用特定算法，分析缺失数据位置附近的数据的特点，根据特点来对该位置的数据进行填充。

为了保证数据的价值，删除数据不是最好的选择，所以填充数据成为解决数据缺失问题的主要方法。

## 常用的数据填充方法
|方法|描述|
|--|--|
|平均数、中位数、众数插补|根据该属性下属性的特性，用该属性下的平均数、中位数、众数进行填充|
|固定值插补|和第一种方法类似，用一个固定值批量地进行插补和填充|
|最近邻插补|用缺失数据该位置附近的数值，用该数值填充缺失数据|
|回归|用缺失数据附近的数值进行回归，根据回归结果估计缺失数据的值|
|插值法|利用特定算法建立插值函数f(x)，缺失值所在位置x1的值由f(x1)表示|

## 插值法——拉格朗日插值
插值法目前已经十分丰富，诸如拉格朗日插值、牛顿插值、Hermite插值、分段插值等，本文重点介绍拉格朗日插值法。

### 拉格朗日插值法
两点能确定一条直线，一次函数，三点能确定一条抛物线，二次函数，以此类推，一般地，平面上的n个点，能够用唯一的一个(n-1)次函数连起来。

**定理**：平面坐标系下，存在n个点，任意两点连线不与x轴垂直，则有唯一的(n-1)次函数，能通过这n个点。  
**不太严格的证明**：设n个点的坐标分别为(x1,y1),(x2,y2),...,(xn,yn)。
设有(n-1)次函数，y=L(x)=a_0+a_1*x+a_2*x^2+...+a_n-1*x^(n-1)
通过将n个点带入，联立方程组直接可以发现，有唯一解（涉及线性方程组解的存在性、唯一性的条件和证明等我都略过了，反正就是能有唯一解233333）。最后解出来的拉格朗日函数如下：
![拉格朗日函数图片](http://upload.wikimedia.org/math/7/1/c/71c9d5496cd18131bf73d1402477c003.png?_=6833391)
其中，
![l函数](http://upload.wikimedia.org/math/9/9/a/99a8f9408d532d4713380f898affe049.png?_=6833391)
这个穿过各个点的函数，就叫做拉格朗日函数。拉格朗日插值的假设是，要估计的值均在拉格朗日函数上，于是对缺失的位置x0，其估计值为L(x0)。

### 拉格朗日插值法的实现
本文以网上下载到的Brent原油价格为例（数据来源eia，共7700多条数据），实现数据的插值。
语言：Python2.7

从下图可以看出其中存在部分数据缺失：  
![数据缺失展示](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/20170709-1.png)

首先，当然是导入需要的包。pandas是常见的用于对数据进行操作和分析的包；patplotlib是python中常见的用于进行数据可视化的包，而lagrange则是对应的拉格朗日函数。
```python
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange # import lagrange function
```

现在定义一个函数，该函数能够处理缺失值，如此一来当我们需要填充缺失值时直接调用即可。
```python
def ployinterp_column(s,n,k=3):
    # using lagrange function on interpolation
    # s: inputdata(column vector), n: the location(index) of paticular number, k: order of langrange func. 
    y=s[list(range(n-k,n))+list(range(n+1,n+1+k))] # choose the data you need to construct L-func. 
    y=y[y.notnull()] # eliminate the Nan data
    if k==1:
        result=sum(y)/len(y) # when k is equal to 1, this method is equal to the average method 
    else:
        temp=y.index-1
        y_index=y.index-(y.index-1)[1]  # to generate the 'x' to construct L-func. 
        result=lagrange(y_index,list(y))(k+1) # construct the L-func and get the estimator
    return result
```

需要详细解释一下，输入值有3个第一个是指待处理的数据集（要求是列向量），n是值第n个位置为空，需要处理。k表示拉格朗日插值的阶数，即需要填充的位置前后分别取k个数构建拉格朗日函数，默认为3。剩下的看注释吧，很详细了。

如今，我们只需要调用这个函数就可以了，遍历整个数据集，鉴定每个位置的值是否为空，对数据为空的位置，调用ployinterp_column函数就行。下面是具体的实现代码。
```python
for i in data.columns:
    for j in range(len(data)):
        if (data[i].isnull())[j]:
            data[i][j]=ployinterp_column(data[i],j)
```

在我的文档中，还有一段用于测试缺失数据是否处理彻底的代码，和上面一段类似，我就不展开说了。

最后，通过绘图的方式来看看插值后结果有没有异常~没问题的话，就可以导出了（呃，不知道为啥，填充之后我发现的数据集存储大小变大了很多）。
```python
plt.plot(data.Num,data.Price)
plt.show()

data.to_csv('data_preprocessed.csv')
```

绘制的图如下，可以看到油价的升降和实际合理，没有出现异常，就当做过了吧。
![result_pic](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/20170709-2.png)

### 拉格朗日插值的优缺点
优点：对非线性序列的插值估计较为准确，因为默构造的是次数较高的函数。
缺点：构建插值函数后，对函数边缘位置的估计准确率下降很快，出现强烈的振荡现象（如下图所示），所以在对某个缺失值进行补充时，用该数据左右两边尽可能相同数量的数据构建拉格朗日插值函数，估计结果会更加准确；另外对具有明显线性性、平稳性的序列，也会有一定误差（此时，推荐用1阶的拉格朗日插值甚至是回归插值会比较好）。  
![震荡](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/20170709-3.jpg)

### 补充
1. 关于拉格朗日插值法的详细解释，可以看参考文献[2]，很详细而且很清楚，图文并茂，存在性和唯一性和我的证明有些不同，大家看喜欢哪种吧。
2. 本文的代码是参考了文献[1]的，但是实验发现文献[1]在某些情况计算会出现异常，异常主要体现在插值后的结果非大或者非常小，反正就和实际结果的数量级差别很大，原因和构建拉格朗日函数时用的x，即自变量有关，作者使用的x直接是Nmu列，即数量标识列，我用的则是简单粗暴的从1开始算的列，对应需要跳的，我也跟着跳了，例如用2001,2002,2003,2005,2006,2007位置的值来构建拉格朗日函数估计缺失值2004对应的值时，2006其实也是空，那在构建的时候需要取消2006，则我用的自变量就是1,2,3,5,7，这样能够有效避免上述我提到的问题。

#### 参考文献
[1] 张良均等，Python数据分析与挖掘实战，机械工业出版社
[2] Angel_Kitty，拉格朗日插值法(图文详解)，http://www.cnblogs.com/ECJTUACM-873284962/p/6833391.html