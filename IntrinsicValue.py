import yfinance as yf
import numpy as np
 
# Step 1: Download AMZN financial data
ticker = 'AMZN'
stock = yf.Ticker(ticker)
 
# Step 2: Extract Free Cash Flow (FCF) - trailing 12 months
cashflow = stock.cashflow
fcf_ttm = cashflow.loc['Operating Cash Flow'][0] - cashflow.loc['Capital Expenditure'][0]
fcf_ttm = fcf_ttm if fcf_ttm > 0 else abs(fcf_ttm)
 
# Step 3: Assumptions for DCF
growth_rate = 0.10       # 12% annual FCF growth for first 5 years
terminal_growth = 0.03   # 3% perpetual growth rate
discount_rate = 0.10     # 10% discount rate
years = 10
 
# Step 4: Forecast future FCFs
fcf_forecast = []
for i in range(1, years + 1):
    fcf = fcf_ttm * ((1 + growth_rate) ** i)
    fcf_forecast.append(fcf)
 
# Step 5: Calculate terminal value (TV)
terminal_value = fcf_forecast[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
 
# Step 6: Discount all cash flows to present value
discounted_fcfs = [fcf / ((1 + discount_rate) ** (i + 1)) for i, fcf in enumerate(fcf_forecast)]
discounted_tv = terminal_value / ((1 + discount_rate) ** years)
 
# Step 7: Add up all present values
intrinsic_value_total = sum(discounted_fcfs) + discounted_tv
 
# Step 8: Divide by number of shares
shares_outstanding = stock.info['sharesOutstanding']
intrinsic_value_per_share = intrinsic_value_total / shares_outstanding
 
# Step 9: Print result
print(f"Intrinsic value per share of {ticker}: {intrinsic_value_per_share:.2f}")
