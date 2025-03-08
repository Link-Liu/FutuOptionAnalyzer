import json
from futu import OpenQuoteContext, SubType, RET_OK

def get_option_greeks(code):
    """
    获取期权的希腊字母  'TODO'
    :param code: 期权代码 'US.NVDA'
    :return: TODO
    """
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    ret_sub, err_message = quote_ctx.subscribe([code], [SubType.QUOTE], subscribe_push=False) # 是否订阅
    # 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
    if ret_sub == RET_OK:  # 订阅成功
        ret, data = quote_ctx.get_stock_quote([code])  # 获取订阅股票报价的实时数据
        if ret == RET_OK:
            all_codes = data['code'].values.tolist() # 股票代码
            all_sigma = data['implied_volatility'].values.tolist()  # 引申波幅
            all_delta = data['delta'].values.tolist() # Delta
            all_theta = data['theta'].values.tolist() # Theta
            all_rho = data['rho'].values.tolist() # Rho
            all_s = data['last_price'].values.tolist() # 正股价 / 最新价格
            all_strike_price = data['strike_price'].values.tolist() # 行权价
            print("所有股票代码：", all_codes)
            print("所有引申波幅：", all_sigma)
            print("所有delta:", all_delta)
            print("所有theta:", all_theta)
            print("所有rho:", all_rho)
            print("所有正股价:", all_s)
            print("所有行权价:", all_strike_price)
        else:
            print('error:', data)
    else:
        print('subscription failed', err_message)
    quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅

if __name__ == "__main__":
    # 传入股票代码"HK.00700"
    get_option_greeks("HK.00700")