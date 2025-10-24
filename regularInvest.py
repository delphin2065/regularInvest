# # import pandas as pd
# # import numpy as np
# # import yfinance as yf
# # import datetime as dt
# # import streamlit as st
# # from matplotlib import pyplot as plt
# # import matplotlib

# # plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
# # plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題


# # st.header('Regular Investment Plan 定期定額投資~~')
# # syb = st.text_input('個股stock_id', placeholder='0050.TW / 006201.TWO / SPY', value='006201.TWO')
# # backDate = st.number_input('回測天數', step=100, min_value=300, value=1000)
# # regCapital = st.number_input('定期投入金額', step=100, min_value=1000) 
# # invDate = st.number_input('每月第幾個交易日投入', step=1, min_value=1, value=5)
# # tax = st.number_input('交易成本', step=0.1, min_value=0.1425, value=0.1425, format="%.4f")
# # tax = tax*0.01
# # btn = st.button('回測執行')


# # if btn:
# #     endDate = dt.datetime.now()
# #     startDate = endDate - dt.timedelta(days=backDate)



# #     df = yf.Ticker(syb).history(start=startDate, end=endDate, auto_adjust=False)
# #     df['tradeDate'] = df.groupby(df.index.to_period('M')).cumcount()+1
# #     dff = df[df['tradeDate']==invDate][['Adj Close', 'Volume']].copy()
    
# #     dff['tax'] = dff['Adj Close'] * tax
# #     dff['shares'] = (regCapital/dff['Adj Close']).astype(int)
# #     dff['cum_shares'] = dff['shares'].cumsum(axis=0)
# #     dff['diff'] = dff['Adj Close'] - dff['Adj Close'].shift(1)
# #     dff['PL'] = dff['shares'].shift(1) * (dff['diff'] - dff['Adj Close'].shift(1) * dff['tax'].shift(1)) + (dff['cum_shares'].shift(1) - dff['shares'].shift(1))* dff['diff']
# #     dff['cumPL'] = dff['PL'].cumsum(axis=0)
# #     dff['CapitalValue'] = dff['cum_shares']*dff['Adj Close']
    
# #     dff.index = dff.index.date
# #     dff.index.name = 'Date'
# #     dff.rename(columns={'Adj Close':syb}, inplace=True) 
# #     dff['dd'] = np.nan

# #     hh = 0
# #     dd_list = []
# #     arr = dff['cumPL'].to_numpy()
# #     for i in range(dff.shape[0]):
# #         if arr[i] >= hh:
# #             hh = arr[i]
# #             dd_list.append(0)
# #         else:
# #             dd_list.append(arr[i]-hh)
# #     dff['DrawDown'] = dd_list
# #     dfc = dff[[syb, 'Volume', 'tax', 'shares', 'PL', 'cumPL', 'CapitalValue', 'DrawDown']].copy()
    
# #     dfc['Volume'] =  dfc['Volume'] / 10000
# #     dfc.rename(columns={'Volume':'Volume(W)'}, inplace=True)
# #     dfc.iloc[:, 4:] = dfc.iloc[:, 4:].round(1)
# #     volRng = np.linspace(dfc['Volume(W)'].min(), dfc['Volume(W)'].max(), 3)
# #     idxNum = np.linspace(0, dfc.shape[0]-1, 5).astype(int)
# #     datRng = [dfc.index[i] for i in idxNum]

# #     fig = plt.figure(figsize=(10, 8))
# #     ax = fig.add_subplot(2, 1, 1)
# #     ax.plot(dfc.index, dfc['cumPL'])
# #     ax.bar(dfc.index, dfc['DrawDown'], width=10, color='red')
# #     ax.set_title(syb + '損益折線圖')
# #     ax.set_xticks(datRng)
# #     ax.set_ylabel('cumPL / DrawDown')
# #     ax.grid(True)




# #     bx = fig.add_subplot(4, 1, 3)
# #     bx.bar(dfc.index, dfc['Volume(W)'], width=10, color='orange')
# #     bx.set_xticks(datRng)
# #     bx.set_ylabel('Volume(W)')
# #     bx.grid(True)
# #     bx.set_yticks(volRng)
    

# #     c1, c2, c3 = st.columns(3)
# #     c1.metric('cumPL',  dfc.loc[dfc.index[-1], 'cumPL'])
# #     c2.metric('totalShares', dfc.loc[:, 'shares'].sum())
    
# #     c3.metric('mDD', dfc['DrawDown'].min())

# #     dfc.rename(columns={'tax':'cost'}, inplace=True)

# #     st.pyplot(fig)  # 使用 st.pyplot(fig) 而不是 st.write(fig)
# #     st.dataframe(dfc)  # 使用 st.dataframe 更適合顯示表格



# # if __name__ == '__main__':
# #     pass
    
# import pandas as pd
# import numpy as np
# import yfinance as yf
# import datetime as dt
# import streamlit as st
# from matplotlib import pyplot as plt
# import matplotlib

# # 更完整的中文字體設定
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
# matplotlib.rcParams['axes.unicode_minus'] = False

# # 或者在每個圖表繪製前設定
# def setup_chinese_font():
#     plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
#     plt.rcParams['axes.unicode_minus'] = False


# st.header('Regular Investment Plan 定期定額投資~~')
# syb = st.text_input('個股stock_id', placeholder='0050.TW / 006201.TWO / SPY', value='006201.TWO')
# backDate = st.number_input('回測天數', step=100, min_value=300, value=1000)
# regCapital = st.number_input('定期投入金額', step=100, min_value=1000) 
# invDate = st.number_input('每月第幾個交易日投入', step=1, min_value=1, value=5)
# tax = st.number_input('交易成本', step=0.1, min_value=0.1425, value=0.1425, format="%.4f")
# tax = tax*0.01
# btn = st.button('回測執行')


# if btn:
#     endDate = dt.datetime.now()
#     startDate = endDate - dt.timedelta(days=backDate)

#     df = yf.Ticker(syb).history(start=startDate, end=endDate, auto_adjust=False)
#     df['tradeDate'] = df.groupby(df.index.to_period('M')).cumcount()+1
#     dff = df[df['tradeDate']==invDate][['Adj Close', 'Volume']].copy()
    
#     dff['tax'] = dff['Adj Close'] * tax
#     dff['shares'] = (regCapital/dff['Adj Close']).astype(int)
#     dff['cum_shares'] = dff['shares'].cumsum(axis=0)
#     dff['diff'] = dff['Adj Close'] - dff['Adj Close'].shift(1)
#     dff['PL'] = dff['shares'].shift(1) * (dff['diff'] - dff['Adj Close'].shift(1) * dff['tax'].shift(1)) + (dff['cum_shares'].shift(1) - dff['shares'].shift(1))* dff['diff']
#     dff['cumPL'] = dff['PL'].cumsum(axis=0)
#     dff['CapitalValue'] = dff['cum_shares']*dff['Adj Close']
    
#     dff.index = dff.index.date
#     dff.index.name = 'Date'
#     dff.rename(columns={'Adj Close':syb}, inplace=True) 
#     dff['dd'] = np.nan

#     hh = 0
#     dd_list = []
#     arr = dff['cumPL'].to_numpy()
#     for i in range(dff.shape[0]):
#         if arr[i] >= hh:
#             hh = arr[i]
#             dd_list.append(0)
#         else:
#             dd_list.append(arr[i]-hh)
#     dff['DrawDown'] = dd_list
#     dfc = dff[[syb, 'Volume', 'tax', 'shares', 'PL', 'cumPL', 'CapitalValue', 'DrawDown']].copy()
    
#     dfc['Volume'] =  dfc['Volume'] / 10000
#     dfc.rename(columns={'Volume':'Volume(W)'}, inplace=True)
#     dfc.iloc[:, 4:] = dfc.iloc[:, 4:].round(1)
#     volRng = np.linspace(dfc['Volume(W)'].min(), dfc['Volume(W)'].max(), 3)
#     idxNum = np.linspace(0, dfc.shape[0]-1, 5).astype(int)
#     datRng = [dfc.index[i] for i in idxNum]

#     # 在繪圖前再次確保字體設定
#     setup_chinese_font()
    
#     fig = plt.figure(figsize=(10, 8))
#     ax = fig.add_subplot(2, 1, 1)
#     ax.plot(dfc.index, dfc['cumPL'])
#     ax.bar(dfc.index, dfc['DrawDown'], width=10, color='red')
#     ax.set_title(f'{syb} 損益折線圖', fontsize=14)  # 明確設定 fontsize
#     ax.set_xticks(datRng)
#     ax.set_ylabel('cumPL / DrawDown', fontsize=12)
#     ax.grid(True)

#     bx = fig.add_subplot(4, 1, 3)
#     bx.bar(dfc.index, dfc['Volume(W)'], width=10, color='orange')
#     bx.set_xticks(datRng)
#     bx.set_ylabel('Volume(W)', fontsize=12)
#     bx.grid(True)
#     bx.set_yticks(volRng)
    
#     # 調整佈局避免文字重疊
#     plt.tight_layout()

#     c1, c2, c3 = st.columns(3)
#     c1.metric('cumPL',  dfc.loc[dfc.index[-1], 'cumPL'])
#     c2.metric('totalShares', dfc.loc[:, 'shares'].sum())
#     c3.metric('mDD', dfc['DrawDown'].min())

#     dfc.rename(columns={'tax':'cost'}, inplace=True)

#     st.pyplot(fig)
#     st.dataframe(dfc)


# if __name__ == '__main__':
#     pass

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import streamlit as st
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.font_manager as fm

# # 設定中文字體 - 適用於 Streamlit Cloud
# def setup_chinese_font():
#     # 嘗試使用 Noto Sans CJK（Streamlit Cloud 安裝的字體）
#     font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
#     try:
#         # 如果字體檔案存在，註冊它
#         if fm.findfont(fm.FontProperties(family='sans-serif')) != fm.findfont(fm.FontProperties(family='Noto Sans CJK TC')):
#             plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'Noto Sans CJK JP', 'sans-serif']
#         else:
#             plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'sans-serif']
#     except:
#         # 備用方案
#         plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'DejaVu Sans']
    
#     plt.rcParams['axes.unicode_minus'] = False

# setup_chinese_font()

st.header('Regular Investment Plan 定期定額投資~~')
syb = st.text_input('個股stock_id', placeholder='0050.TW / 006201.TWO / SPY', value='006201.TWO')
backDate = st.number_input('回測天數', step=100, min_value=300, value=1000)
regCapital = st.number_input('定期投入金額', step=100, min_value=1000) 
invDate = st.number_input('每月第幾個交易日投入', step=1, min_value=1, value=5)
tax = st.number_input('交易成本', step=0.1, min_value=0.1425, value=0.1425, format="%.4f")
tax = tax*0.01
btn = st.button('回測執行')


if btn:
    endDate = dt.datetime.now()
    startDate = endDate - dt.timedelta(days=backDate)

    df = yf.Ticker(syb).history(start=startDate, end=endDate, auto_adjust=False)
    df['tradeDate'] = df.groupby(df.index.to_period('M')).cumcount()+1
    dff = df[df['tradeDate']==invDate][['Adj Close', 'Volume']].copy()
    
    dff['tax'] = dff['Adj Close'] * tax
    dff['shares'] = (regCapital/dff['Adj Close']).astype(int)
    dff['cum_shares'] = dff['shares'].cumsum(axis=0)
    dff['diff'] = dff['Adj Close'] - dff['Adj Close'].shift(1)
    dff['PL'] = dff['shares'].shift(1) * (dff['diff'] - dff['Adj Close'].shift(1) * dff['tax'].shift(1)) + (dff['cum_shares'].shift(1) - dff['shares'].shift(1))* dff['diff']
    dff['cumPL'] = dff['PL'].cumsum(axis=0)
    dff['CapitalValue'] = dff['cum_shares']*dff['Adj Close']
    
    dff.index = dff.index.date
    dff.index.name = 'Date'
    dff.rename(columns={'Adj Close':syb}, inplace=True) 
    dff['dd'] = np.nan

    hh = 0
    dd_list = []
    arr = dff['cumPL'].to_numpy()
    for i in range(dff.shape[0]):
        if arr[i] >= hh:
            hh = arr[i]
            dd_list.append(0)
        else:
            dd_list.append(arr[i]-hh)
    dff['DrawDown'] = dd_list
    dfc = dff[[syb, 'Volume', 'tax', 'shares', 'PL', 'cumPL', 'CapitalValue', 'DrawDown']].copy()
    
    dfc['Volume'] =  dfc['Volume'] / 10000
    dfc.rename(columns={'Volume':'Volume(W)'}, inplace=True)
    dfc.iloc[:, 4:] = dfc.iloc[:, 4:].round(1)
    volRng = np.linspace(dfc['Volume(W)'].min(), dfc['Volume(W)'].max(), 3)
    idxNum = np.linspace(0, dfc.shape[0]-1, 5).astype(int)
    datRng = [dfc.index[i] for i in idxNum]

    # # 在繪圖前設定字體
    # setup_chinese_font()
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(dfc.index, dfc['cumPL'], label='累計損益')
    ax.bar(dfc.index, dfc['DrawDown'], width=10, color='red', alpha=0.5, label='回撤')
    ax.set_title(f'{syb} 損益折線圖', fontsize=14, fontweight='bold')
    ax.set_xticks(datRng)
    ax.set_ylabel('累計損益 / 回撤', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    bx = fig.add_subplot(4, 1, 3)
    bx.bar(dfc.index, dfc['Volume(W)'], width=10, color='orange')
    bx.set_xticks(datRng)
    bx.set_ylabel('成交量(萬)', fontsize=12)
    bx.grid(True, alpha=0.3)
    bx.set_yticks(volRng)
    
    plt.tight_layout()

    c1, c2, c3 = st.columns(3)
    c1.metric('累計損益',  f'{dfc.loc[dfc.index[-1], "cumPL"]:,.0f}')
    c2.metric('總股數', f'{dfc.loc[:, "shares"].sum():,.0f}')
    c3.metric('最大回撤', f'{dfc["DrawDown"].min():,.0f}')

    dfc.rename(columns={'tax':'cost'}, inplace=True)

    st.pyplot(fig)
    st.dataframe(dfc)


if __name__ == '__main__':
    pass