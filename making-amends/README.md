# making-amends
This folder contains my solution to level 6 of the Trades.Exec()-game at stockfighter.io.

## Executive summary
The error messages for the order cancelling API leak some information which allows for the account names to be determined. Using account names, executions can be streamed using the websocket-API which does not require extra authentication. Using the websocket-API, executions were streamed to a text file. From this text file, some key statistics were computed for the accounts which were used to determine the outlier trading account.

My solution is divided into two parts: the data streaming script `create_data.py` and the data analysis notebook `analyze_data.ipynb`.

## `create_data.py`
It was found that the error messages for canceling orders without proper authorization contain the name to which a particular order belongs. By testing order_ids starting from 1, and using regexes to extract the account name, I was able to generate a set of all encountered account names. I did not immediately come up with a way to determine when all account names have been found, or a way to more efficiently navigate the search space of possible accounts. Hence, I kept the account-discovering while loop running for pretty much the entire duration of the level.  

Whenever a new account name is encountered, I start listening on the execution websocket for that particular account (as the websockets API doesn't require any authorization beyond the account name). In the `received_message`-callback of the websocket, I parse the execution info and write the most interesting variables into a text file `data/amends.csv`, one line at a time. While not the most scalable solution, a text file was found to be plenty good enough with less than 5MB of fill data to deal with.

For this level, and for previous Trades.Exec()-levels, I have utilized [jchristman's Stockfighter Python API](https://github.com/jchristman/Stockfighter), and a copy of the `stockfighter.py`-script can be found in this repo.

## `analyze_data.ipynb`
In this notebook, I analyze the `data/amends.csv`-file to try to detect the inside trader. Using the pandas library for dataframes in Python, I compute key statistics for the accounts, such as the profit, the net position, the total number of fills and the total number of unique orders. Of the 100 accounts, only about 10 were profitable for the investigated period. There a few clear outliers in terms of profitability. Two of them seemed like a sophisticated HFT investors with a massive number of fills, while a third outlier had an abnormally high profit per fill ratio. The latter was considered the most suspicious and was submitted as the solution.

As an extra exercise, I performed a statistical outlier detection on the set of profitable accounts using the `OneClassSVM` of the scikit-learn machine learning library. Again, the three previously mentioned accounts emerged as the outliers.
