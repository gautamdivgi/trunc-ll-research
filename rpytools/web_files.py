"""
Plot data for each of the data sets analyzed
Main contents per entry

type: cdf or ccdf
tag: Data set tag
xlim: X-axis limit
ylim: Y-axis limit
xticks: X-ticks
yticks: Y-ticks
xlabel: X-axis label
ylabel: Y-axis label
legend1: Legend for the data
legend2: Legend for the fit
loc: Location of the legend

"""

"""
Azure wireless - ALL category
"""
calgary_cdf = {"type": "cdf", \
					 "tag": "CALGARY", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 5e4], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e4, 2e4, 3e4, 4e4, 5e4], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

calgary_ccdf = {"type": "ccdf", \
					 "tag": "CALGARY", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [0, 1e8], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [10, 1e3, 1e5, 1e7, 1e8], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

clarknet_cdf = {"type": "cdf", \
					 "tag": "CLARKNET", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 1e5], \
					 "ylim": [0, 1], \
					 "xticks": [0, 2e4, 4e4, 8e4, 1e5], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

clarknet_ccdf = {"type": "ccdf", \
					 "tag": "CLARKNET", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [10, 1e8], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [10, 1e2, 1e4, 1e6, 1e8], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

nasa_cdf = {"type": "cdf", \
					 "tag": "NASA", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 5e5], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e5, 2e5, 3e5, 4e5, 5e5], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

nasa_ccdf = {"type": "ccdf", \
					 "tag": "NASA", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [10, 1e7], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [10, 1e2, 1e4, 1e6, 1e7], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

sask_cdf = {"type": "cdf", \
					 "tag": "SASK", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 5e4], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e4, 2e4, 3e4, 4e4, 5e4], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

sask_ccdf = {"type": "ccdf", \
					 "tag": "SASK", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e8], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [10, 1e3, 1e5, 1e7, 1e8], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

ftp_fsiz_cdf = {"type": "cdf", \
					 "tag": "FTP_FILE_SIZE", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 1.5e5], \
					 "ylim": [0, 1], \
					 "xticks": [0, 2.5e4, 5e4, 1e5, 1.5e5], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

ftp_fsiz_ccdf = {"type": "ccdf", \
					 "tag": "FTP_FILE_SIZE", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e9], \
					 "ylim": [5e-6, 1.0], \
					 "xticks": [1e1, 1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

ftp_flsiz_cdf = {"type": "cdf", \
					 "tag": "FTP_FLOW_SIZE", \
					 "xlabel": "Flow size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 2e5], \
					 "ylim": [0, 1], \
					 "xticks": [0, 5e4, 9e4, 1.3e5, 1.7e5, 2e5], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

ftp_flsiz_ccdf = {"type": "ccdf", \
					 "tag": "FTP_FLOW_SIZE", \
					 "xlabel": "Flow size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e9], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [1e1, 1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

ftp_xtime_cdf = {"type": "cdf", \
					 "tag": "FTP_XFER_TIME", \
					 "xlabel": "Transfer times [seconds]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 20], \
					 "ylim": [0, 1], \
					 "xticks": [0, 4, 8, 12, 16], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

ftp_xtime_ccdf = {"type": "ccdf", \
					 "tag": "FTP_XFER_TIME", \
					 "xlabel": "Transfer times [seconds]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e-2, 1e7], \
					 "ylim": [5e-6, 1.0], \
					 "xticks": [1e-2, 1, 1e2, 1e4, 1e6, 1e7], \
					 "yticks": [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

showme_cdf = {"type": "cdf", \
					 "tag": "SHOWME", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 2e4], \
					 "ylim": [0, 1], \
					 "xticks": [0, 4e3, 8e3, 1.2e4, 1.6e4, 2e4], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

showme_ccdf = {"type": "ccdf", \
					 "tag": "SHOWME", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e5], \
					 "ylim": [1e-3, 1.0], \
					 "xticks": [1e1, 1e2, 1e3, 1e4, 1e5], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

twa_cdf = {"type": "cdf", \
					 "tag": "TWA", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 8e5], \
					 "ylim": [0, 1], \
					 "xticks": [0, 2e5, 4e5, 6e5, 8e5], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

twa_ccdf = {"type": "ccdf", \
					 "tag": "TWA", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e7], \
					 "ylim": [1e-3, 1.0], \
					 "xticks": [1e1, 1e2, 1e4, 1e6, 1e7], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}


w98_cdf = {"type": "cdf", \
					 "tag": "W98", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 2e4], \
					 "ylim": [0, 1], \
					 "xticks": [0, 4e3, 8e3, 1.2e4, 1.6e4, 2e4], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

w98_ccdf = {"type": "ccdf", \
					 "tag": "W98", \
					 "xlabel": "File size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e7], \
					 "ylim": [5e-6, 1.0], \
					 "xticks": [1e1, 1e2, 1e4, 1e6, 1e7], \
					 "yticks": [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}
