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
slen_all_cdf = {"type": "cdf", \
					 "tag": "SLEN_CATH", \
					 "xlabel": "Session length [seconds]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 12000], \
					 "ylim": [0, 1], \
					 "xticks": [0, 3000, 6000, 9000, 12000], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

slen_all_ccdf = {"type": "ccdf", \
					 "tag": "SLEN_CATH", \
					 "xlabel": "Session length [seconds]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [0, 1e5], \
					 "ylim": [5e-4, 1.0], \
					 "xticks": [1, 1e1, 1e2, 1e3, 1e4, 1e5], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

bin_all_cdf = {"type": "cdf", \
					 "tag": "BIN_CATH", \
					 "xlabel": "Inbound traffic [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 4e7], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e7, 2e7, 3e7, 4e7], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

bin_all_ccdf = {"type": "ccdf", \
					 "tag": "BIN_CATH", \
					 "xlabel": "Inbound traffic [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [10, 1e10], \
					 "ylim": [5e-4, 1.0], \
					 "xticks": [10, 1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

bout_all_cdf = {"type": "cdf", \
					 "tag": "BOUT_CATH", \
					 "xlabel": "Outbound traffic [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 8e6], \
					 "ylim": [0, 1], \
					 "xticks": [0, 2e6, 4e6, 6e6, 8e6], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

bout_all_ccdf = {"type": "ccdf", \
					 "tag": "BOUT_CATH", \
					 "xlabel": "Outbound traffic [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [10, 1e9], \
					 "ylim": [5e-4, 1.0], \
					 "xticks": [10, 1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

tslen_all_cdf = {"type": "cdf", \
					 "tag": "TSLEN_CATH", \
					 "xlabel": "Total network access time [seconds]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 4e4], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e4, 2e4, 3e4, 4e4], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

tslen_all_ccdf = {"type": "ccdf", \
					 "tag": "TSLEN_CATH", \
					 "xlabel": "Total network access time [seconds]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1, 1e7], \
					 "ylim": [1e-3, 1.0], \
					 "xticks": [1, 1e2, 1e4, 1e6], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

tbin_all_cdf = {"type": "cdf", \
					 "tag": "TBIN_CATH", \
					 "xlabel": "Total inbound traffic [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 3e8], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e8, 2e8, 3e8], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

tbin_all_ccdf = {"type": "ccdf", \
					 "tag": "TBIN_CATH", \
					 "xlabel": "Total inbound traffic [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e3, 1e10], \
					 "ylim": [1e-3, 1.0], \
					 "xticks": [1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

tbout_all_cdf = {"type": "cdf", \
					 "tag": "TBOUT_CATH", \
					 "xlabel": "Total outbound traffic [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 3e7], \
					 "ylim": [0, 1], \
					 "xticks": [0, 1e7, 2e7, 3e7], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

tbout_all_ccdf = {"type": "ccdf", \
					 "tag": "TBOUT_CATH", \
					 "xlabel": "Total outbound traffic [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e2, 5e9], \
					 "ylim": [1e-3, 1.0], \
					 "xticks": [1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}
