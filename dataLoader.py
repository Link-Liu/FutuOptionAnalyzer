import json
from futu import OpenQuoteContext, RET_OK


# 接受两个参数：stock_code（股票代码）和 strike_price（行权价格）
def get_option_greeks(stock_code, strike_price):
    # 创建OpenQuoteContext对象，与富途行情服务器建立连接
    # host='127.0.0.1'表示服务器运行在本地，port=11111是默认端口
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # 返回值ret表示请求状态，option_chain是返回的期权数据
    ret, option_chain = quote_ctx.get_option_chain(stock_code)
    if ret == RET_OK:
        data_list = []
        for item in option_chain:
            if item['strike_price'] == strike_price:
                greeks = {
                    "symbol": item['stock_code'], # 期权的股票代码
                    "implied_volatility": item['implied_volatility'], # 引申波幅
                    "delta": item['delta'], # Delta值
                    "theta": item['theta'], # Theta值
                    "rho": item['rho'], # Rho值
                    "underlying_price": item['owner_stock_price'], # 正股价格
                    "expiration_date": item['expiry_date']  # 期权到期时间
                }
                data_list.append(greeks)
        with open("option_data.json", "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)
    quote_ctx.close()

if __name__ == "__main__":
    # 传入股票代码"HK.00700"和行权价格400
    get_option_greeks("HK.00700", 400)