import numpy as np
from sklearn import svm, preprocessing
import pandas as pd
from matplotlib import style

style.use("ggplot")

FEATURES = ['DE Ratio',
            'Trailing P/E',
            'Price/Sales',
            'Price/Book',
            'Profit Margin',
            'Operating Margin',
            'Return on Assets',
            'Return on Equity',
            'Revenue Per Share',
            'Market Cap',
            'Enterprise Value',
            'Forward P/E',
            'PEG Ratio',
            'Enterprise Value/Revenue',
            'Enterprise Value/EBITDA',
            'Revenue',
            'Gross Profit',
            'EBITDA',
            'Net Income Avl to Common ',
            'Diluted EPS',
            'Earnings Growth',
            'Revenue Growth',
            'Total Cash',
            'Total Cash Per Share',
            'Total Debt',
            'Current Ratio',
            'Book Value Per Share',
            'Cash Flow',
            'Beta',
            'Held by Insiders',
            'Held by Institutions',
            'Shares Short (as of',
            'Short Ratio',
            'Short % of Float',
            'Shares Short (prior ']


def build_data_set():
    data_df = pd.read_csv("key_stats_acc_perf_WITH_NA.csv")

    # data_df = data_df[:100]
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace("NaN", 0).replace("N/A", 0)

    x = np.array(data_df[FEATURES].values)  # .tolist())

    y = (data_df["Status"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    x = preprocessing.scale(x)

    z = np.array(data_df[["stock_p_change", "sp500_p_change"]])

    return x, y, z


def analysis():
    test_size = 1

    invest_amount = 10000
    total_invests = 0

    if_market = 0
    if_strat = 0

    x, y, z = build_data_set()

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(x[:-test_size], y[:-test_size])

    correct_count = 0

    for x in range(1, test_size + 1):
        if clf.predict(x[[-x]])[0] == y[-x]:
            correct_count += 1

        if clf.predict(x[[-x]])[0] == 1:
            invest_return = invest_amount + (invest_amount * (z[-x][0] / 100))
            market_return = invest_amount + (invest_amount * (z[-x][1] / 100))
            total_invests += 1
            if_market += market_return
            if_strat += invest_return

    data_df = pd.read_csv("forward_sample.csv")

    data_df = data_df.replace("N/A", 0).replace("NaN", 0)

    x = np.array(data_df[FEATURES].values)

    x = preprocessing.scale(x)

    z = data_df["Ticker"].values.tolist()
    for i in range(len(x)):
        for j in range(len(x[i])):
            if np.isnan(x[i][j]):
                x[i][j] = False
    invest_list = []
    for i in range(len(x)):
        p = clf.predict(x[[i]])[0]
        if p == 1:
            invest_list.append(z[i])

    return invest_list
