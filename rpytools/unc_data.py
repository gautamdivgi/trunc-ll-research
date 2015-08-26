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
unc_flow_cdf = {"type": "cdf", \
					 "tag": "UNC_FLOW_ALL", \
					 "xlabel": "Flow size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 2.5e4], \
					 "ylim": [0, 1], \
					 "xticks": [0, 0.5e4, 1e4, 1.5e4, 2e4, 2.5e4], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

unc_flow_ccdf = {"type": "ccdf", \
					 "tag": "UNC_FLOW_ALL", \
					 "xlabel": "Flow size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1e1, 1e10], \
					 "ylim": [5e-7, 1.0], \
					 "xticks": [1e2, 1e4, 1e6, 1e8, 1e10], \
					 "yticks": [1e-6, 1e-4, 1e-2, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

unc_slen_cdf = {"type": "cdf", \
					 "tag": "UNC_SLEN_ALL", \
					 "xlabel": "Session length [seconds]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 450], \
					 "ylim": [0, 1], \
					 "xticks": [0, 100, 200, 300, 400, 450], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

unc_slen_ccdf = {"type": "ccdf", \
					 "tag": "UNC_SLEN_ALL", \
					 "xlabel": "Session length [seconds]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [1, 1e5], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [1, 1e1, 1e2, 1e3, 1e4, 1e5], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "Data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}
