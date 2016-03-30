from stockfighter import Stockfighter
import re

def execution_ticker(execution):
    try:
        account = execution['account']
        direction = execution['order']['direction']
        id_curr = execution['order']['id']
        fills = execution['order']['fills']
        for fill in fills:
            ts = fill['ts']
            price = fill['price']
            q = fill['qty']
            row = map(str, [account, direction, id_curr, ts, price, q])
            f.write(','.join(row) + '\n')
            f.flush()
    except Exception, e:
        print 'Could not parse execution data', str(e)

#Insert your info here
venue = ''
account = ''
stock = ''
fighter = Stockfighter(venue, account)
open_sockets = set()
p = re.compile('[A-Z]{2,}\d+')
i = 1
fname = 'data/amends.csv'
f = open(fname, 'wb')
f.write('account,direction,id,ts,price,qty\n')
f.flush()
while True:
    try:
        fighter.cancel(stock, i)
    except Exception, e:
        msg = str(e)
        matches = p.findall(msg)
        if len(matches) > 0:
            acc_tmp = matches[0]
            if acc_tmp not in open_sockets:
                open_sockets.add(acc_tmp)
                print 'Found new account: ', acc_tmp, ', total accounts: ', len(open_sockets)
                Stockfighter(venue, acc_tmp).execution_stock_ticker(execution_ticker, stock)
    i += 1  