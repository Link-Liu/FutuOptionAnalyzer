from math import log, sqrt, exp
from scipy.stats import norm
from datetime import datetime


def compCO(S, L, sigma, t, t_assume, r=0.042197):
    """"
    S: 正股价格
    L: 行权价格
    r: 无风险利率， 默认4.2197%
    t: 期权到期时间 (can be datetime or string)
    t_assume: 计算日期
    T: 期权到期时间， 到期日 (t) - 假定日期
    sigma: 波动率
    """
    if isinstance(t, str):
        t1 = datetime.strptime(t, '(%Y, %m, %d)')
    else:  # Assume t is a datetime object
        t1 = t
    T = (t1 - t_assume).days / 365.0
    d1 = (log(S / L) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    C = S * norm.cdf(d1) - L * exp(-r * T) * norm.cdf(d2)
    return C

def compPO(S, L, sigma, t, t_assume, r=0.042197):
    """"
    S: 正股价格
    L: 行权价格
    r: 无风险利率， 默认4.2197%
    t: 期权到期时间 (can be datetime or string)
    t_assume: 计算日期
    T: 期权到期时间， 到期日 (t) - 假定日期
    sigma: 波动率
    """
    if isinstance(t, str):
        t1 = datetime.strptime(t, '(%Y, %m, %d)')
    else:  # Assume t is a datetime object
        t1 = t
    T = (t1 - t_assume).days / 365.0
    d1 = (log(S / L) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    P = L * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return P


def findXForGreaterSum(LC, LP, sigmaC, sigmaP, tC, tP, t_assume, thetaC, thetaP, c1, p1, profit,ratio, r=0.042197, start=1.0, step=0.1,
                           max_iter=10000, precision=0.01, x_max_search=10000):
        """
        寻找两个交点 x,使得 compCO(x, L, sigma, t, r) + compPO(x, L, sigma, t, r) == c1 + p1
        注：若 compCO + compPO 关于 x 呈现 U 型（即有一个负的极小值）时，
             则此方程可能有两个解，此时对于 x < x_lower 和 x > x_upper 都有
             compCO(x) + compPO(x) > c1 + p1,
             返回 [x_lower, x_upper] 即中间区间为违背条件，否则返回 None
        参数:
          S0:现在正股价
          L: 行权价格
          sigma: 年化波动率
          t_assume: 卖出时间(datetime 对象)
          tC:call到期时间
          tP:put到期时间
          c1: 给定的看涨期权价格
          p1: 给定的看跌期权价格
          r: 无风险利率, 默认 4.2197%
          start: 搜索起始值, 默认 1.0
          step: 初始步长, 默认 0.1
          max_iter: 最大迭代次数, 默认 10000
          precision: 二分法精度, 默认 0.01
          x_max_search: 搜索 x 的上限, 默认 10000
        返回:
          找到两个交点时返回 [x_lower, x_upper]，否则返回 None
        """
        # 定义目标函数 f(x) = compCO + compPO - (c1 + p1)
        def f(x):
            TC = (tC - t_assume).days / 365.0
            TP = (tP - t_assume).days / 365.0
            return compCO(x, LC, sigmaC, tC,t_assume, r) + compPO(x, LP, sigmaP, tP,t_assume, r) - (c1 + p1) + TC*thetaC +TP*thetaP - (profit/ratio)

        roots = []
        x_prev = start
        f_prev = f(x_prev)
        x = start + step
        iterations = 0

        while x <= x_max_search and iterations < max_iter:
            f_curr = f(x)
            if f_prev * f_curr < 0:
                # 使用二分法求根
                low, high = x - step, x
                while high - low > precision:
                    mid = (low + high) / 2
                    if f(low) * f(mid) <= 0:
                        high = mid
                    else:
                        low = mid
                root = (low + high) / 2
                roots.append(root)
                # 如果找到两个根，则退出循环
                if len(roots) == 2:
                    break
            x_prev = x
            f_prev = f_curr
            x += step
            iterations += 1

        return roots if roots else None

if __name__ == '__main__':
    S0 = float(input("Enter current stock price: "))
    t_assume = datetime.strptime(input('Enter selling date(2025,12,31):'), '%Y,%m,%d')
    profit = float(input('Enter profit:'))
    ratio = float(input('Enter ratio:'))

    LC = 140
    LP = 120
    sigmaC = 0.56
    sigmaP = 0.62
    thetaC = -0.0023
    thetaP = -0.0074
    tC = datetime(2025, 5, 2)
    tP = datetime(2025, 5, 10)

    result = findXForGreaterSum(LC, LP, sigmaC, sigmaP, tC, tP, t_assume, thetaC, thetaP,
                               compCO(S0, LC, sigmaC, tC, datetime.now()),
                               compPO(S0, LP, sigmaP, tP, datetime.now()),
                               profit, ratio)
    print(result)