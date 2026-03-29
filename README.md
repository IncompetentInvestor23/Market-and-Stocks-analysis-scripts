# Market-and-Stocks-analysis-scripts
This repository contains the Python scripts that I use for different market and stock analysis using Yahoo Finance.

1. market_ath_diff.py : returns the current price change from ATH of the SP500, Nasdaq and FTSE100.
2. gold_ftse_signal.py : it fetches the closing prices of gold futures and the FTSE100, calculaltes the daily returns of each and computes the rolling 30-day correlation between them. That single number, ranging from -1 to +1, tells you what kind of market regime you are in. A correlation of -1 means that gold and the FTSE100 move in opposite directions (pure crisis mode). A correlation of 0 means the two assets are moving indepently of each other, the panic is fading. A correlation of +1 means they move together, liquidity is back in the system.

Note: This gold FTSE100 correlation should be only screened after a drawdown of at least -35% from ATH of the FTSE100.

3. main.py (using tickers_lse, isa_filter, health_filter, value_screener and dividend_screener) : this tool is an automated stock screener designed for UK retail investors who hold shares inside an ISA (Individual Savings Account). Its goal is simple: scan the London Stock Exchange (LSE), eliminate companies that do not meet a minimum quality threshold, and present two shortlists of five stocks each: one for value investing and one for dividend investing.
All data is pulled in real time from Yahoo Finance, so every time I run it I get a fresh analysis based on current market prices and the latest company financials.
The four stages of analysis: the screener works as a funnel. Every stock on the FTSE 100 and FTSE 250 enters at the top, and only those that pass all four stages make it to the final recommendations.

3.1 Stage 1 - Universe: FTSE 100 & FTSE 250 (tickers_lse.py)
   The starting universe is made up of approximately 200 companies listed on the LSE, covering the 100 largest (FTSE 100) and the next 250 largest (FTSE 250) by market capitalisation.

3.2 Stage 2 - ISA Eligibility Filter (isa_filter.py)
   Not every security listed in London can be held in an ISA. This stage removes anything that HMRC rules do not allow inside a Stocks & Shares ISA. The tool excludes:
   -ETFs & ETCs (Exchange Traded Funds/Commodities): these are baskets of assets, not individual companies.
   -Investment trust and REITs: while some are ISA-eligible, the screener conservatively focuses on direct company shares to keep the analysis clean.
   -Any instrument not directly listed on the LSE: for example, foreign shares not cross-listed in London.
What remains after this filter is a list of ordinary shares in actual operating companies that you can legally and practically hold in your ISA.

3.3 Stage 3 - Financial Health Filter (health_filter.py)
   
