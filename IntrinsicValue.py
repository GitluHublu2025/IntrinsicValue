import yfinance as yf
import numpy as np

def calculate_intrinsic_value(ticker, growth_rate=0.10, terminal_growth=0.03, discount_rate=0.10, years=10):
    """
    Calculates the intrinsic value per share using a DCF model.

    Args:
        ticker (str): Stock ticker symbol.
        growth_rate (float): Annual FCF growth rate for the initial period.
        terminal_growth (float): Perpetual growth rate for the terminal value.
        discount_rate (float): Discount rate.
        years (int): Number of years for the initial growth period.

    Returns:
        float: Intrinsic value per share.
    """
    # Step 1: Download AMZN financial data
    stock = yf.Ticker(ticker)

    # Step 2: Extract Free Cash Flow (FCF) - trailing 12 months
    cashflow = stock.cashflow
    # Using .iloc[0] to access the first column to avoid FutureWarning
    fcf_ttm = cashflow.loc['Operating Cash Flow'].iloc[0] - cashflow.loc['Capital Expenditure'].iloc[0]
    fcf_ttm = fcf_ttm if fcf_ttm > 0 else abs(fcf_ttm)


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
    shares_outstanding = stock.info.get('sharesOutstanding', 1) # Default to 1 to avoid division by zero
    intrinsic_value_per_share = intrinsic_value_total / shares_outstanding

    return intrinsic_value_per_share

# Example usage:
ticker = 'AMZN'
intrinsic_value = calculate_intrinsic_value(ticker)
print(f"Intrinsic value per share of {ticker}: {intrinsic_value:.2f}")
