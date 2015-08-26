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
run1_cdf = {"type": "cdf", \
					 "tag": "SIM_R1", \
					 "xlabel": "Simulated file size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 1e7], \
					 "ylim": [0, 1], \
					 "xticks": [0, 2e6, 4e6, 6e6, 8e6, 1e7], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "RUN1 data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

run1_ccdf = {"type": "ccdf", \
					 "tag": "SIM_R1", \
					 "xlabel": "Simulated file size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [0, 1e9], \
					 "ylim": [5e-4, 1.0], \
					 "xticks": [10, 1e3, 1e5, 1e7, 1e9], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "RUN1 data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

run2_cdf = {"type": "cdf", \
					 "tag": "SIM_R2", \
					 "xlabel": "Simulated file size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 2e5], \
					 "ylim": [0, 1], \
					 "xticks": [0, 5e4, 1e5, 1.5e5, 2e5], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "RUN2 data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

run2_ccdf = {"type": "ccdf", \
					 "tag": "SIM_R2", \
					 "xlabel": "Simulated file size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [0, 1e8], \
					 "ylim": [5e-4, 1.0], \
					 "xticks": [10, 1e3, 1e5, 1e7, 1e8], \
					 "yticks": [1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "RUN2 data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}

run3_cdf = {"type": "cdf", \
					 "tag": "SIM_R3", \
					 "xlabel": "Simulated file size [bytes]", \
					 "ylabel": "$P(X \leq x)$", \
					 "xlim": [0, 180], \
					 "ylim": [0, 1], \
					 "xticks": [0, 30, 60, 90, 120, 150, 180], \
					 "yticks": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], \
					 "legend1": "RUN3 data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 4}

run3_ccdf = {"type": "ccdf", \
					 "tag": "SIM_R3", \
					 "xlabel": "Simulated file size [bytes]", \
					 "ylabel": "$P(X > x)$", \
					 "xlim": [0, 1e7], \
					 "ylim": [5e-5, 1.0], \
					 "xticks": [1e-2, 1e0, 1e2, 1e4, 1e6, 1e7], \
					 "yticks": [1e-4, 1e-3, 1e-2, 1e-1, 1], \
					 "legend1": "RUN3 data", \
					 "legend2": "%%%dist-replace%%%", \
					 "loc": 3}
