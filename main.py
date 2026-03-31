# src/main.py
"""
LSE ISA Value & Dividend Screener.
Description: analyse LSE stocks available on ISA accounts,
filter by financial health and generates top 15 for Value and Dividend investing.
"""

import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import os
import sys

# Add actual directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tickers_lse import get_lse_tickers
from isa_filter import filter_isa_stocks
from health_filter import filter_healthy_stocks
from value_screener import get_top15_value
from dividend_screener import get_top15_dividend

def fetch_stock_data(ticker):
    """
    Obtains fundamental data from a stock.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            'Ticker': ticker,
            'info': info,
            'fetch_time': datetime.now()
        }
    except Exception as e:
        print(f"Error with {ticker}: {str(e)[:50]}")
        return None

def save_results(value_top15, dividend_top15, output_dir='../data/output'):
    """
    Save results to a csv file.
    """
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Save top 15 value
    if value_top15:
        df_value = pd.DataFrame(value_top15)
        value_file = f"{output_dir}/value_top15_{timestamp}.csv"
        df_value.to_csv(value_file, index=False)
        print(f"\n Value top15 saved: {value_file}")

    # Save top 15 dividend
    if dividend_top15:
        df_div = pd.DataFrame(dividend_top15)
        div_file = f"{output_dir}/dividend_top15_{timestamp}.csv"
        df_div.to_csv(div_file, index=False)
        print(f"\n Dividend top15 saved: {div_file}")

    # Save file with static timestamp (last analysis)
    if value_top15:
        pd.DataFrame(value_top15).to_csv(f"{output_dir}/value_top15_latest.csv", index=False)
    if dividend_top15:
        pd.DataFrame(dividend_top15).to_csv(f"{output_dir}/dividend_top15_latest.csv", index=False)

def main():
    """
    Main function of the screener.
    """
    print("=" * 70)
    print("LSE ISA VALUE & DIVIDEND SCREENER")
    print("=" * 70)
    print("\n PROCESS:")
    print("  1. Obtain LSE tickers")
    print("  2. Filter ISA availability")
    print("  3. Filter financial health")
    print("  4. Analyse Value investing (top 15)")
    print("  5. Analyse Dividend investing (top 15)")
    print("=" * 70)

    # STEP 1: Obtain tickers
    print("\n STEP 1: Loading LSE tickers...")
    tickers = get_lse_tickers()
    print(f"  Total: {len(tickers)} tickers")

    # STEP 2: Obtain data for each ticker
    print("\n STEP 2: Downloading fundamental data...")
    print(f"  This will take approximately {len(tickers) * 0.5 / 60:.1f} minutes")

    all_stocks = []
    for i, ticker in enumerate(tickers, 1):
        print(f"  [{i:3d}/{len(tickers)}] {ticker:<10}...", end=" ", flush=True)

        data = fetch_stock_data(ticker)
        if data:
            all_stocks.append(data)
            print("succeed")
        else:
            print("failed")

        # Pause to respect request rate limits
        time.sleep(0.3)

    print(f"\n Data obtained: {len(all_stocks)}/{len(tickers)} stocks")

    # STEP 3: ISA Filter
    print("\n STEP 3: Filtering ISA availability...")
    isa_stocks = filter_isa_stocks(all_stocks)

    # STEP 4: Financial health filter
    print("\n STEP 4: Filtering financial health...")
    healthy_stocks = filter_healthy_stocks(isa_stocks)

    if len(healthy_stocks) == 0:
        print("\n No healthy stocks found")
        return

    # STEP 5: Value analysis
    print("\n STEP 5: Analysing for Value Investing...")
    value_top15 = get_top15_value(healthy_stocks)

    # STEP 6: Dividend analysis
    print("\n STEP 6: Analysing for Dividend Investing...")
    dividend_top15 = get_top15_dividend(healthy_stocks)

    # STEP 7: Save results
    print("\n STEP 7: Saving results...")
    save_results(value_top15, dividend_top15)

    # Final summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"\n Summary:")
    print(f"  -Total LSE stocks: {len(tickers)}")
    print(f"  -Obtained data: {len(all_stocks)}")
    print(f"  -ISA available: {len(isa_stocks)}")
    print(f"  -Financial health: {len(healthy_stocks)}")
    print(f"\n  Top 15 Value generated")
    print(f"\n  Top 15 Dividend generated")
    print(f"\n  Check the 'data/output' directory for the CSV")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Process interrupted by user")
    except Exception as e:
        print(f"\n Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n Press ENTER to exit...")
    input()
