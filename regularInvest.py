import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import streamlit as st
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

class regularInvest:
  def __init__(self, syb, endDate, startDate, fee, regCapital, invDate):
    self.syb = syb
    self.endDate = endDate
    self.startDate = startDate
    self.fee = fee
    self.regCapital = regCapital
    self.invDate = invDate
    self.df = pd.DataFrame()
    self.entryDate = None
    self.entryPrice = None
    self.entryShares = 0
    self.tradeInfo = []
    self.calcuateInfo = []
    self.dfc = pd.DataFrame()
    self.calcuateFinalInfo = []

  def get_df(self):
    self.df = yf.Ticker(self.syb).history(start=self.startDate, end=self.endDate, auto_adjust=False)
    self.df.index = pd.to_datetime(self.df.index.date)
    self.df.index.name = 'Date'
    self.df.reset_index(inplace=True, drop=False)
    self.df.insert(1, 'Stock_ID', syb.upper())
    self.df = self.df[['Date', 'Stock_ID', 'Open', 'Adj Close']]



  def buy_shares(self):
    self.get_df()
    num = 0
    cnt = 0
    for index in range(1, self.df.shape[0]):
      if self.df.loc[index, 'Date'].month == self.df.loc[index-1, 'Date'].month:
        num = num + 1
      else:
        num = 1

      if num == self.invDate:
        cnt = cnt + 1
        self.entryDate = self.df.loc[index, 'Date'].date()
        self.entryPrice = self.df.loc[index, 'Open']
        self.entryShares = int(regCapital / self.entryPrice)
        self.tradeInfo.append((cnt, self.entryDate, self.entryPrice, self.entryShares))


  def calulate_pl(self):
    self.buy_shares()
    for ind in self.tradeInfo:
        ind_cnt = ind[0]
        ind_date = ind[1]
        ind_price = ind[2]
        ind_shares = ind[3]
        for index in range(self.df.shape[0]):
            if self.df.loc[index, 'Date'].date() >= ind_date:
                cal_date = self.df.loc[index, 'Date'].date()
                cal_pl = (self.df.loc[index, 'Adj Close'] - ind_price * (1 + self.fee)) * ind_shares
                self.calcuateInfo.append((cal_date, self.df.loc[index, 'Adj Close'], ind_shares, cal_pl))

        self.dfc = pd.DataFrame(self.calcuateInfo, columns=['Date', self.syb.upper(), 'Shares', 'cumPL'])
        self.dfc['Date'] = pd.to_datetime(self.dfc['Date'])
        dfg_1 = self.dfc.groupby(['Date'])[[self.syb.upper()]].mean()
        dfg_2 = self.dfc.groupby(['Date'])[['Shares', 'cumPL']].sum()
        dfg_1.reset_index(inplace=True)
        dfg_2.reset_index(inplace=True)
        self.dfc = pd.merge(dfg_1, dfg_2, on='Date', how='left')
        self.dfc['DrawDown'] = self.dfc['cumPL'] - np.maximum.accumulate(self.dfc['cumPL'])
        
    return self.dfc.round(2)

  def calculate_final_pl(self):
    self.buy_shares()
    for ind in self.tradeInfo:
      ind_cnt = ind[0]
      ind_date = ind[1]
      ind_price = ind[2]
      ind_shares = ind[3]
      cal_fee = ind_price * self.fee * ind_shares
      cal_final_pl = (self.df.loc[self.df.shape[0]-1, 'Adj Close'] - ind_price * (1 + self.fee)) * ind_shares
      self.calcuateFinalInfo.append((ind_date, ind_cnt, ind_price, self.df.loc[self.df.shape[0]-1, 'Adj Close'], ind_shares, cal_fee, cal_final_pl))

    self.dff = pd.DataFrame(self.calcuateFinalInfo, columns=['進場日期', '第n次買入', self.syb.upper(), '最近收盤價', '買入股數', '手續費', '進場後累積損益'])
    self.dff['進場日期'] = pd.to_datetime(self.dff['進場日期'])
    return self.dff.round(2)


st.header('Regular Investment Plan 定期定額投資~~')
syb = st.text_input('個股stock_id', placeholder='0050.TW / 006201.TWO / SPY', value='006201.TWO')

col1, col2 = st.columns(2)
with col1:
    choiceStartDate = st.date_input('選擇起始日期', dt.datetime.now() - dt.timedelta(days=1000))
with col2:
    choiceEndDate = st.date_input('選擇結束日期', dt.datetime.now())

regCapital = st.number_input('定期投入金額', step=100, min_value=100, value=1000) 
invDate = st.number_input('每月第幾個交易日投入', step=1, min_value=1, value=5)
fee = st.number_input('交易成本', step=0.1, min_value=0.1425, value=0.1425, format="%.4f")
fee = fee*0.01
btn = st.button('回測執行')


if btn:
    
    startDate = choiceStartDate
    endDate = choiceEndDate

   

    r = regularInvest(syb, endDate=endDate, startDate=startDate, fee=fee, regCapital=regCapital, invDate=invDate)
    dfc = r.calulate_pl()
    dfc['Date'] = dfc['Date'].dt.date
    dfc.set_index('Date', inplace=True, drop=True)
    

    c1, c2, c3, c4 = st.columns(4)
    c1.metric('cumPL',  dfc.loc[dfc.index[-1], 'cumPL'])
    c2.metric('totalShares', dfc.loc[dfc.index[-1], 'Shares'])
    c3.metric('maxDrawDown', dfc['DrawDown'].min())
    riskRewardRatio = (dfc.loc[dfc.index[-1], 'cumPL'] / abs(dfc['DrawDown'].min())).round(2) if dfc['DrawDown'].min() < 0 else 0
    c4.metric('riskRewardRatio', riskRewardRatio)


    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(dfc.index, dfc['cumPL'])
    ax.fill_between(dfc.index, dfc['DrawDown'], alpha=0.5, color='green')    
    ax.grid(True)
    ax.set_ylabel('cumPL / DrawDown')
    ax.set_xticks([dfc.index[i] for i in np.linspace(0, dfc.shape[0]-1, 4).astype(int)])
    
    dff = r.calculate_final_pl()
    dff['進場日期'] = dff['進場日期'].dt.date
    dff.set_index('進場日期', inplace=True, drop=True)
    dff.rename(columns={'最近收盤價':str(dfc.index[dfc.shape[0]-1]) + ' 收盤價'}, inplace=True)  
    
    st.pyplot(fig)  
    st.dataframe(dff,   use_container_width=True)  


if __name__ == '__main__':
    pass
    
