# Stocktwits-Scalper
A consistantly profitable bot that checks for and scalps pump and dump schemes on the popular stock trading media site Stocktwits


WARNING: This repository should not be used as investment advice, and I am not liable for any money lost using this program

This python script takes advantage of hysteria created when popular stocktwits user mrinvestorpro (https://stocktwits.com/mrinvestorpro) announces to his followers that he is investing in a stock. A buy alert post from mrinvestorpro triggers massive, immediate rises in stock prices, often as high as 20%. The problem is, these rises in price happen instantaneously and much too quickly for a human to buy before the price peaks and ultimately sells off back to its previous levels in a matter of seconds.

This script uses the stocktwits API and Alpaca brokerage to detect when mrivestorpro is tweeting and quickly buy and sell the stock for a small profit if it catches his alert tweet soon enough. The script checks for a new tweet every 18 seconds (rate limit for stocktwits API). If a it finds a new tweet, it checks how long ago it was posted. If it was posted less than 6 seconds ago, the script checks if its contents meet the criteria for a buy alert. If it does, the script buys the stock with Alpaca, and simulataneously sets a 3% take profit limit order and stop loss. The script is set to only buy if it catches the tweet within 6 seconds, because any longer and the chances of profit decrease significantly due to the speed of the spike and drop in stock price.

Alpaca is an API based brokerage platform that can be found here: https://alpaca.markets/
Alpaca is used in this project for its speed and simplicity.

I encourage you not to invest any money that you would be disappointed to lose.

Feel free to use this to make some money on the side, as I have. If you know of a clever way to beat the stocktwits API rate limit and would like to contribute, just let me know.
