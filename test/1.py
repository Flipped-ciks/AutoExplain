# 列表中有若干个整数
d = [27,28,30]  

# 用于存储每个质因子的最大次数
yzinfo = {}  

# 记录因子次数的函数
def jlyz(yz, cs):
    if yz in yzinfo:
        if cs > yzinfo[yz]:   # 保留最大次数
            yzinfo[yz] = cs
    else:
        yzinfo[yz] = cs

# 统计整数 x 的质因子
def tjyz(x):
    yz, cs = 2, 0
    while x > 1:
        if x % yz == 0:
            cs += 1           # 因子次数累加
            x = x // yz
        else:
            if cs > 0:
                jlyz(yz, cs)
            yz, cs = yz + 1, 0
    # 处理最后一个因子
    # if cs > 0:
    #     jlyz(yz, cs)

# 遍历列表中的每个整数，统计质因子
for i in d:
    tjyz(i)

# 计算最小公倍数
gbs = 1
for i in yzinfo:
    gbs *= i ** yzinfo[i]

# 输出结果
print('列表', d, '中所有元素的最小公倍数为：', gbs)
print('因子信息：', yzinfo)
