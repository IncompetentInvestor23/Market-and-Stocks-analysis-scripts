# Market-and-Stocks-analysis-scripts
This repository contains the Python scripts that I use for different market and stock analysis using Yahoo Finance.

1. market_ath_diff.py returns the current price change from ATH of the SP500, Nasdaq and FTSE100.
2. gold_ftse_signal.py it fetches the closing prices of gold futures and the FTSE100, calculaltes the daily returns of each and computes the rolling 30-day correlation between them. That single number, ranging from -1 to +1, tells you what kind of market regime you are in. A correlation of -1 means that gold and the FTSE100 move in opposite directions (pure crisis mode). A correlation of 0 means the two assets are moving indepently of each other, the panic is fading. A correlation of +1 means they move together, liquidity is back in the system.

Note: This gold FTSE100 correlation should be only screened after a drawdown of at least -35% from ATH of the FTSE100.
