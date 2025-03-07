from math import log, sqrt, exp
from scipy.stats import norm
from datetime import datetime

def compCO(S, L, sigma, t, r=0.042197):
    """
    计算看涨期权价格 (Black-Scholes 模型)
    参数:
        S: 当前股票价格 (正数)
        L: 行权价格 (正数)
        sigma: 年化波动率 (正数)
        t: 期权到期时间 (datetime 对象)
        r: 无风险利率，默认 4.2197%
    返回:
        看涨期权价格
    """
    # 参数检查
    if S <= 0 or L <= 0 or sigma <= 0:
        raise ValueError("S, L, sigma 必须为正数")
    if not isinstance(t, datetime):
        raise ValueError("t 必须是 datetime 对象")
    
    T = (t - datetime.now()).days / 365.0
    if T <= 0:
        raise ValueError("到期时间 t 必须晚于当前时间")
    
    d1 = (log(S / L) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    C = S * norm.cdf(d1) - L * exp(-r * T) * norm.cdf(d2)
    return C

def compPO(S, L, sigma, t, r=0.042197):
    """
    计算看跌期权价格 (Black-Scholes 模型)
    参数:
        S: 当前股票价格 (正数)
        L: 行权价格 (正数)
        sigma: 年化波动率 (正数)
        t: 期权到期时间 (datetime 对象)
        r: 无风险利率，默认 4.2197%
    返回:
        看跌期权价格
    """
    # 参数检查
    if S <= 0 or L <= 0 or sigma <= 0:
        raise ValueError("S, L, sigma 必须为正数")
    if not isinstance(t, datetime):
        raise ValueError("t 必须是 datetime 对象")
    
    T = (t - datetime.now()).days / 365.0
    if T <= 0:
        raise ValueError("到期时间 t 必须晚于当前时间")
    
    d1 = (log(S / L) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    P = L * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return P

def findXForGreaterSum(L, sigma, t, c1, p1, r=0.042197, start=1.0, step=0.1, max_iter=10000, precision=0.01):
    """
    寻找股票价格 x，使得 compCO(x) + compPO(x) > c1 + p1
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
    返回:
        满足条件的最小 x，若未找到返回 None
    """
    # 参数检查
    if start <= 0 or step <= 0 or precision <= 0:
        raise ValueError("start, step, precision 必须为正数")
    if c1 < 0 or p1 < 0:
        raise ValueError("c1 和 p1 不能为负数")
    
    x = start
    iter_count = 0
    
    # 第一阶段：粗略搜索找到满足条件的 x
    while iter_count < max_iter:
        c2 = compCO(x, L, sigma, t, r)
        p2 = compPO(x, L, sigma, t, r)
        if c2 + p2 > c1 + p1:
            break
        x += step
        iter_count += 1
    else:
        return None  # 未找到满足条件的 x
    
    # 第二阶段：二分法提高精度
    left = max(start, x - step)  # 确保 left >= start
    right = x
    while right - left > precision:
        mid = (left + right) / 2
        c_mid = compCO(mid, L, sigma, t, r)
        p_mid = compPO(mid, L, sigma, t, r)
        if c_mid + p_mid > c1 + p1:
            right = mid
        else:
            left = mid
    
    return (left + right) / 2

# 示例使用
if __name__ == "__main__":
    expiry = datetime(2024, 12, 31)  # 到期日
    L = 100  # 行权价格
    sigma = 0.2  # 波动率
    c1 = 10  # 给定的看涨期权价格
    p1 = 5   # 给定的看跌期权价格
    
    try:
        x = findXForGreaterSum(L, sigma, expiry, c1, p1)
        if x is not None:
            print(f"找到满足条件的股票价格 x = {x:.4f}")
            print(f"验证: compCO = {compCO(x, L, sigma, expiry):.4f}, compPO = {compPO(x, L, sigma, expiry):.4f}")
        else:
            print("未找到满足条件的 x")
    except ValueError as e:
        print(f"错误: {e}")