from rpytools import azuall as azuall
from rpytools import azucatm as azucatm
from rpytools import azucatd as azucatd
from rpytools import azucath as azucath
from rpytools import web_files as wb
from rpytools import unc_data as unc
from rpytools import sim_files as sim

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
Distribution list
Changing loglogistic legend to T-LL as per the recommendations of Dr. Chlebus - 08/03/2014
The loglogistic is really just a special case of T-LL, hence there is no need to present
it separately. Presenting it as T-LL also shows the heavy-tailed nature of T-LL in special cases
"""
dist_map = {"LOGLOGISTIC": \
					{"legend": "T-LL", "ext": "ll"}, \
				"TRUNCLL": \
					{"legend": "T-LL", "ext": "tll"}, \
				"LOGN": \
					{"legend": "LOGN", "ext": "lgn"}, \
				"TPARETO": \
					{"legend": "TP", "ext": "tp"} \
			  }

cdf_tag = "_ecdf"
ccdf_tag = "_ccdf"
plot_dir = "plots"
dist_replace_string = "%%%dist-replace%%%"

sim_dataset_list = (sim.run1_cdf, sim.run1_ccdf, sim.run2_cdf, sim.run2_ccdf, sim.run3_cdf, sim.run3_ccdf)

unc_dataset_list = (unc.unc_flow_cdf, \
						  unc.unc_flow_ccdf, \
						  unc.unc_slen_cdf, \
						  unc.unc_slen_ccdf)


web_dataset_list = (wb.calgary_cdf, \
						  wb.calgary_ccdf, \
						  wb.clarknet_cdf, \
						  wb.clarknet_ccdf, \
						  wb.nasa_cdf, \
						  wb.nasa_ccdf, \
						  wb.sask_cdf, \
						  wb.sask_ccdf, \
						  wb.ftp_fsiz_cdf, \
						  wb.ftp_fsiz_ccdf, \
						  wb.ftp_flsiz_cdf, \
						  wb.ftp_flsiz_ccdf, \
						  wb.ftp_xtime_cdf, \
						  wb.ftp_xtime_ccdf, \
						  wb.showme_cdf, \
						  wb.showme_ccdf, \
						  wb.twa_cdf, \
						  wb.twa_ccdf, \
						  wb.w98_cdf, \
						  wb.w98_ccdf)

azu_dataset_list = (azuall.slen_all_cdf, \
					 azuall.slen_all_ccdf, \
					 azuall.bin_all_cdf, \
					 azuall.bin_all_ccdf, \
					 azuall.bout_all_cdf, \
					 azuall.bout_all_ccdf, \
					 azuall.to_bin_all_cdf, \
					 azuall.to_bin_all_ccdf, \
					 azuall.to_bout_all_cdf, \
					 azuall.to_bout_all_ccdf, \
					 azuall.tslen_all_cdf, \
					 azuall.tslen_all_ccdf, \
					 azuall.tbin_all_cdf, \
					 azuall.tbin_all_ccdf, \
					 azuall.tbout_all_cdf, \
					 azuall.tbout_all_ccdf, \
					 azucatm.slen_all_cdf, \
					 azucatm.slen_all_ccdf, \
					 azucatm.bin_all_cdf, \
					 azucatm.bin_all_ccdf, \
					 azucatm.bout_all_cdf, \
					 azucatm.bout_all_ccdf, \
					 azucatm.tslen_all_cdf, \
					 azucatm.tslen_all_ccdf, \
					 azucatm.tbin_all_cdf, \
					 azucatm.tbin_all_ccdf, \
					 azucatm.tbout_all_cdf, \
					 azucatm.tbout_all_ccdf, \
					 azucath.slen_all_cdf, \
					 azucath.slen_all_ccdf, \
					 azucath.bin_all_cdf, \
					 azucath.bin_all_ccdf, \
					 azucath.bout_all_cdf, \
					 azucath.bout_all_ccdf, \
					 azucath.tslen_all_cdf, \
					 azucath.tslen_all_ccdf, \
					 azucath.tbin_all_cdf, \
					 azucath.tbin_all_ccdf, \
					 azucath.tbout_all_cdf, \
					 azucath.tbout_all_ccdf, \
					 azucatd.slen_all_cdf, \
					 azucatd.slen_all_ccdf, \
					 azucatd.bin_all_cdf, \
					 azucatd.bin_all_ccdf, \
					 azucatd.bout_all_cdf, \
					 azucatd.bout_all_ccdf, \
					 azucatd.tslen_all_cdf, \
					 azucatd.tslen_all_ccdf, \
					 azucatd.tbin_all_cdf, \
					 azucatd.tbin_all_ccdf, \
					 azucatd.tbout_all_cdf, \
					 azucatd.tbout_all_ccdf)

dataset_list = unc_dataset_list
# dataset_list = azu_dataset_list
# dataset_list = web_dataset_list
# dataset_list = sim_dataset_list
