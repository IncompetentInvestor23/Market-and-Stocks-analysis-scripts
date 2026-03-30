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

Note: the tickers_lse.py FTSE 100 and FTSE 250 ticker list are hardcoded and have to be manually updated quarterly (March, June, September and December), the list provided in this code may be outdated.

3.2 Stage 2 - ISA Eligibility Filter (isa_filter.py)
   Not every security listed in London can be held in an ISA. This stage removes anything that HMRC rules do not allow inside a Stocks & Shares ISA. The tool excludes:
   
   -ETFs & ETCs (Exchange Traded Funds/Commodities): these are baskets of assets, not individual companies.
   
   -Investment trust and REITs: while some are ISA-eligible, the screener conservatively focuses on direct company shares to keep the analysis clean.
   
   -Any instrument not directly listed on the LSE: for example, foreign shares not cross-listed in London.
   
What remains after this filter is a list of ordinary shares in actual operating companies that you can legally and practically hold in your ISA.

3.3 Stage 3 - Financial Health Filter (health_filter.py)
   This is the most important gate in the process. A company can look attractive on price alone but be dangerously fragile underneath. This stage make sure that the company is fundamentally solid. It scores each company out of 5 points across four dimensions:

   -Debt level (up to 2 points): measured by the Debt-to-Equity ratio, wich compares how much the company owes versus how much belongs to shareholders. A very low ratio (below 30) gets 2 points. A manageable ratio (below 50) gets 1 point. Companies with very high debt get nothing. High debt is dangerous in rising interest rate environments and can wipe out shareholders if the business hits a rough patch.

   -Liquidity (up to 1 point): measured by the Current Ratio, wich compares a company's short-term assets (cash, receivables, inventory) to its short-term debts. A ratio avobe 2 means the company could pay off everything it owes in the next 12 months twice over, that is financial comfort. Anything below 1.5 is a concern; it means the company may struggle to meet near-term obligations.

   -Profitability (up to 1.5 points): two things are checked here. First, is the company actually making money? A positive net income earns 1 point. Second, is the operating margin avobe 10%? This measures how efficiently the core business converts revenue into profit before financial engineering (interest, taxes). A healthy operating margin means the business model itself works, not just the accounting.

   -Free Cash Flow (up to 0.5 points): net profit can be manipulated through accounting choices. Free Cash Flow (FCF) is harder to fake, it is the actual cash left over after the company has paid to run and invest in its business. A positive FCF means the company is genuinely generating money it can return to shareholders or reinvest.

Minimum to pass: 3 out of 5 points. Companies that fail this filter are eliminated regardless of how cheap they look on valuation metrics.

3.4A - Value Investing Screen (value_screener.py)
   This screen looks for companies that are underpriced relative to their fundamentals. Each stock is scored out of 10 across five criteria:

   -Price-to-Earnings ratio (up to 3 points): tells you how many years of current earnings you are paying for the company. A P/E of 10 means you pay 10x the annual profit. Anything below 15 is considered value territory, below 10 is genuinely cheap. High P/E ratios (avobe 20) suggest the market is pricing in a lot of future growth, fine for growth investing but not for value.

   -Price-to-Book ratio (up to 2 points): book value is the net worth of the company on paper, what you would theoretically recover if it were liquidated. Buying a company below its book value (P/B < 1) is the classic "margin of safety", you are paying less than the accounting value of the assets. P/B below 1.5 is still reasonable. Very high P/B scores nothing.

   -Dividend Yield (up to 1.5 points): a company that returns cash to shareholders via dividends is signalling financial confidence. A yield above 3% of the share price earns full marks on this criterion. This is not the main focus of the value screen but is a positive signal.

   -Return on Equity (up to 2 points): ROE measures how efficiently a company uses shareholders money to generate profit. A 20% ROE means the company earns 20p for every 1£ of equity, excellent. ROE is a sign of a durable competitive advantage. Below 10% suggests a mediocre business.

   -Earnings Growth (up to 1.5 points): a value stock is not necessarily a declining one. If a cheap company is also growing its earnings, thats the best of both worlds, you buy low and growth does the rest. Earnings growth above 5% per year earns full marks here.

The result is a ranked list of the top 5 value stocks: companies that combine chepness on multiple metrics with solid fundamentals.

3.4B - Dividend Investing Screen (dividend_screener.py)
   -This screen looks for companies that are reliable, generous payers of dividends: companies with a long track record of paying and growing their dividend. Each stock is scored out of 10 across four criteria:

   -Dividend Yield (up to 3 points): the annual dividend divided by the share price. A yield between 5% and 10% earns maximum points, it is high enough to be genuinely attractive as income. A yield above 10% is treated with suspicion: yields that high often signakl that the market expects the dividend to be cut (a "dividend trap"). A yield between 3% and 5% is good, below 3% scores lower.

   -Payout Ratio (up to 2.5 points): this is the percentage of profits paid out as dividends. A company paying out 40% of its earnings is in a very comfortable position, it keeps 60% to reinvest and has plenty of buffer if profits fall. A payout ratio above 70% is worrying: one bad year could force a dividend cut. The screener rewards conservative payout ratios and penalises unsustainable ones.

   -Dividend Growth (up to 2 points): a dividend that grows every year is far more valuable that a static one, it protects your income against inflation. Companies growing their dividend by more than 5% annually earn full marks here. This criterion also identifies management confidence: you do not raise your dividend if you think things are going to get worse.

   - Free Cash Flow Coverage (up to 2.5 points): this is the most rigorous dividend sustainability check. Does the company generate enough real cash, not accounting profit, but actual cash to pay its dividend? The tool compares the total FCF to the total cash it pays out in dividends to all shareholders. A coverage ratio above 2x means the dividend is well protected. Below 1x means the company is paying out more in dividends than it earns in cash, a red flag that a cut may be coming.

The result is a ranked list of the top 5 dividend stocks: companies combining an attractive and sustainable income with a solid financial foundation.

3.5 What the output tells you: the tool produces two CSV files, one for each strategy. Each row is a company, and the columns include:

   -Ticker: the stock market code.

   -Name: the company name.

   -Price: the current share price in pence.

   -Score: the overall ranking score (out of 10).

   -Key ratios: P/E, P/B, ROE, Yield, Payout, FCF Coverage... depending on the strategy.

   -Factors: a plain-English summary of the two or three things that drove the score.
   
