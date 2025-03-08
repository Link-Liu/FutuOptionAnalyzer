import json
from futu import OpenQuoteContext, SubType, RET_OK
import time


def get_code_list(num, code, start, end):
    """
    获取股票代码列表
    :param num: 股票代码数量
    :return: 股票代码列表
    """
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret2, data2 = quote_ctx.get_option_chain(code, start, end)
    code = []
    if ret2 == RET_OK:
        for i in range(num):
            data2['code'][i]
    else:
        print('error:', data2)
    time.sleep(2)
    quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
    return code

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
            all_codes = data['code'].values # 股票代码
            all_sigma = data['implied_volatility']  # 引申波幅
            all_delta = data['delta'].values # Delta
            all_theta = data['theta'].values # Theta
            all_rho = data['rho'].values # Rho
            all_s = data['last_price'].values # 正股价 / 最新价格
            all_strike_price = data['strike_price'].values # 行权价
        else:
            print('error:', data)
    else:
        print('subscription failed', err_message)
    quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅
    return all_codes, all_sigma, all_delta, all_theta, all_rho, all_s, all_strike_price

def save_json(filename, num, code, start, end):
    codes = get_code_list(20, code, start, end)
    for code in codes:
        all_codes, all_sigma, all_delta, all_theta, all_rho, all_s, all_strike_price = get_option_greeks(code)
        data_entry = {  
            "query_code": code,
            "all_codes": list(all_codes),
            "implied_volatility": list(all_sigma),
            "delta": list(all_delta),
            "theta": list(all_theta),
            "rho": list(all_rho),
            "last_price": list(all_s),
            "strike_price": list(all_strike_price)
        }
        with open(filename, "a", encoding="utf8") as f:
            json.dump(data_entry, f, ensure_ascii=False, indent=4)
            f.write("\n")


if __name__ == "__main__":
    # 传入股票代码"HK.00700"
    get_option_greeks("HK.00700")
    save_json("option_greeks.json",20, "HK.00700", "2021-01-01", "2021-01-31")