from math import log, sqrt, exp
from scipy.stats import norm
from datetime import datetime

def compCO(S, L, sigma, t, r = 0.042197):
    """"
    S: 当前股票价格/ 正股价格
    L: 行权价格
    r: 无风险利率， 默认4.2197%
    t: 期权到期时间
    T: 期权到期时间， 到期日 (t) - 当前日期
    sigma: 波动率
    """
    T = (t - datetime.now()).days / 365.0
    d1 = (log(S / L) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    C = S * norm.cdf(d1) - L * exp(-r * T) * norm.cdf(d2)
    return C

def compPO(S, L, sigma, t, r = 0.042197):
    """"
    S: 当前股票价格/ 正股价格
    L: 行权价格 / 执行价格
    r: 无风险利率， 默认4.2197%
    t: 期权到期时间
    T: 期权到期时间， 到期日 (t) - 当前日期
    sigma: 波动率
    """
    T = (t - datetime.now()).days / 365.0
    d1 = (log(S / L) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    P = L * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return P

def findXForGreaterSum(L, sigma, t, c1, p1, r=0.042197, start=1.0, step=0.1, max_iter=10000, precision=0.01, x_max_search=10000):
    """
    寻找股票价格 x 的区间 [x_min, x_max] 使得 compCO(x) + compPO(x) > c1 + p1
    参数:
        L: 行权价格
        sigma: 年化波动率
        t: 期权到期时间 (datetime 对象)
        c1: 给定的看涨期权价格
        p1: 给定的看跌期权价格
        r: 无风险利率，默认 4.2197%
        start: 搜索起始值，默认 1.0
        step: 初始步长，默认 0.1
        max_iter: 最大迭代次数，默认 10000
        precision: 最终精度，默认 0.01
        x_max_search: 搜索 x 的上限，默认 10000
    返回:
        满足条件的 x 区间 [x_min, x_max]，若未找到返回 None
    """
    # 参数检查
    if start <= 0 or step <= 0 or precision <= 0:
        raise ValueError("start, step, precision 必须为正数")
    if c1 < 0 or p1 < 0:
        raise ValueError("c1 和 p1 不能为负数")
    
    x = start
    iter_count = 0
    x_min = None
    
    # 第一阶段：粗略搜索找到满足条件的 x_min
    while iter_count < max_iter and x <= x_max_search:
        c2 = compCO(x, L, sigma, t, r)
        p2 = compPO(x, L, sigma, t, r)
        if c2 + p2 > c1 + p1:
            x_min = x
            break
        x += step
        iter_count += 1
    
    if x_min is None:
        return None  # 未找到满足条件的 x
    
    # 第二阶段：二分法精确 x_min
    left = max(start, x_min - step)
    right = x_min
    while right - left > precision:
        mid = (left + right) / 2
        c_mid = compCO(mid, L, sigma, t, r)
        p_mid = compPO(mid, L, sigma, t, r)
        if c_mid + p_mid > c1 + p1:
            right = mid
        else:
            left = mid
    x_min_precise = (left + right) / 2
    
    # 第三阶段：设置 x_max
    # 假设 compCO(x) + compPO(x) 单调递增，x_max 为搜索上限
    x_max = x_max_search
    
    return [x_min_precise, x_max]
    
if __name__ == "__main__":
    s = 111.9
    l = 160
    sigma = 51.603 / 100
    t = datetime(2025, 5, 16)
    result = compCO(s, l, sigma, t)
    print(result)
    s = 111.7
    l = 110
    t = datetime(2025, 4, 23)
    sigma = 56.901 / 100
    result = compPO(s, l, sigma, t)
    print(result)
