"""
Data sets file - the file for the paths to all data sets
"""

"""
Individual files - along with any custom tags
Every file entry is a dictionary with 2 mandatory fields
tag: unique tag
filename: The entire path to the file

An optional properties dictionary can also be added  - but any processing logic
needs to consider the possibility that the properties may not exist.
"""

"""
Azure wireless files - ALL
"""
AzuSlenAll = {"tag": "SLEN_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/slen/all", \
				  "description": "Session length - ALL"}
AzuBinAll = {"tag": "BIN_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/bin/all", \
				  "description": "Inbound session traffic - ALL"}
AzuBoutAll = {"tag": "BOUT_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/bout/all", \
				  "description": "Outbound session traffic - ALL"}
AzuToBinAll = {"tag": "TO_BIN_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/to_inb/all", \
				  "description": "Inbound traffic for timed out sessions"}
AzuToBoutAll = {"tag": "TO_BOUT_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/to_outb/all", \
				  "description": "Outbound traffic for timed out sessions"}
AzuTSlenAll = {"tag": "TSLEN_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/tslen/all", \
				  "description": "Sum of all sessions per user - ALL"}
AzuTBinAll = {"tag": "TBIN_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/tinb/all", \
				  "description": "Sum of all inbound traffic per user - ALL"}
AzuTBoutAll = {"tag": "TBOUT_ALL", \
				  "filename": "/home/gautam/research/ml_data/azu/toutb/all", \
				  "description": "Sum of all outbound traffic per user - ALL"}



"""
Azure wireless files - CATM
"""
AzuSlenCatm = {"tag": "SLEN_CATM", \
				  "filename": "/home/gautam/research/ml_data/azu/slen/catm", \
				  "description": "Session length - CATM"}
AzuBinCatm = {"tag": "BIN_CATM", \
				  "filename": "/home/gautam/research/ml_data/azu/bin/catm", \
				  "description": "Inbound session traffic - CATM"}
AzuBoutCatm = {"tag": "BOUT_CATM", \
				  "filename": "/home/gautam/research/ml_data/azu/bout/catm", \
				  "description": "Outbound session traffic - CATM"}
AzuTSlenCatm = {"tag": "TSLEN_CATM", \
				  "filename": "/home/gautam/research/ml_data/azu/tslen/catm", \
				  "description": "Sum of all sessions per user - CATM"}
AzuTBinCatm = {"tag": "TBIN_CATM", \
				  "filename": "/home/gautam/research/ml_data/azu/tinb/catm", \
				  "description": "Sum of all inbound traffic per user - CATM"}
AzuTBoutCatm = {"tag": "TBOUT_CATM", \
				  "filename": "/home/gautam/research/ml_data/azu/toutb/catm", \
				  "description": "Sum of all outbound traffic per user - CATM"}


"""
Azure wireless files - CATD
"""
AzuSlenCatd = {"tag": "SLEN_CATD", \
				  "filename": "/home/gautam/research/ml_data/azu/slen/catd", \
				  "description": "Session length - CATD"}
AzuBinCatd = {"tag": "BIN_CATD", \
				  "filename": "/home/gautam/research/ml_data/azu/bin/catd", \
				  "description": "Inbound session traffic - CATD"}
AzuBoutCatd = {"tag": "BOUT_CATD", \
				  "filename": "/home/gautam/research/ml_data/azu/bout/catd", \
				  "description": "Outbound session traffic - CATD"}
AzuTSlenCatd = {"tag": "TSLEN_CATD", \
				  "filename": "/home/gautam/research/ml_data/azu/tslen/catd", \
				  "description": "Sum of all sessions per user - CATD"}
AzuTBinCatd = {"tag": "TBIN_CATD", \
				  "filename": "/home/gautam/research/ml_data/azu/tinb/catd", \
				  "description": "Sum of all inbound traffic per user - CATD"}
AzuTBoutCatd = {"tag": "TBOUT_CATD", \
				  "filename": "/home/gautam/research/ml_data/azu/toutb/catd", \
				  "description": "Sum of all outbound traffic per user - CATD"}


"""
Azure wireless files - CATH
"""
AzuSlenCath = {"tag": "SLEN_CATH", \
				  "filename": "/home/gautam/research/ml_data/azu/slen/cath", \
				  "description": "Session length - CATH"}
AzuBinCath = {"tag": "BIN_CATH", \
				  "filename": "/home/gautam/research/ml_data/azu/bin/cath", \
				  "description": "Inbound session traffic - CATH"}
AzuBoutCath = {"tag": "BOUT_CATH", \
				  "filename": "/home/gautam/research/ml_data/azu/bout/cath", \
				  "description": "Outbound session traffic - CATH"}
AzuTSlenCath = {"tag": "TSLEN_CATH", \
				  "filename": "/home/gautam/research/ml_data/azu/tslen/cath", \
				  "description": "Sum of all sessions per user - CATH"}
AzuTBinCath = {"tag": "TBIN_CATH", \
				  "filename": "/home/gautam/research/ml_data/azu/tinb/cath", \
				  "description": "Sum of all inbound traffic per user - CATH"}
AzuTBoutCath = {"tag": "TBOUT_CATH", \
				  "filename": "/home/gautam/research/ml_data/azu/toutb/cath", \
				  "description": "Sum of all outbound traffic per user - CATH"}

AzureWirelessSet = (AzuSlenAll, AzuBinAll, AzuBoutAll, AzuToBinAll, AzuToBoutAll, AzuTSlenAll, AzuTBinAll, AzuTBoutAll, \
						  AzuSlenCatm, AzuBinCatm, AzuBoutCatm, AzuTSlenCatm, AzuTBinCatm, AzuTBoutCatm, \
						  AzuSlenCatd, AzuBinCatd, AzuBoutCatd, AzuTSlenCatd, AzuTBinCatd, AzuTBoutCatd, \
						  AzuSlenCath, AzuBinCath, AzuBoutCath, AzuTSlenCath, AzuTBinCath, AzuTBoutCath)

"""
Web Files
"""
Calgary = {"tag": "CALGARY", \
			  "filename": "/home/gautam/research/ml_data/web_files/calgary", \
			  "description": "Web server files from the University of Calgary"}
ClarkNet = {"tag": "CLARKNET", \
				"filename": "/home/gautam/research/ml_data/web_files/clarknet", \
				"description": "Web server files from the Clark Net ISP"}
FlowSize = {"tag": "FTP_FLOW_SIZE", \
				"filename": "/home/gautam/research/ml_data/web_files/flow_size", \
				"description": "FTP flow sizes"}
FtpSize = {"tag": "FTP_FILE_SIZE", \
			  "filename": "/home/gautam/research/ml_data/web_files/ftp_size", \
			  "description": "FTP file sizes"}
FtpTime = {"tag": "FTP_XFER_TIME", \
			  "filename": "/home/gautam/research/ml_data/web_files/ftp_time", \
			  "description": "FTP file transfer durations"}
Nasa = {"tag": "NASA", \
		  "filename": "/home/gautam/research/ml_data/web_files/nasa", \
		  "description": "Web server files from NASA"}
Sask = {"tag": "SASK", \
		  "filename": "/home/gautam/research/ml_data/web_files/saskatchewan", \
		  "description": "Web server files from the university of Saskatchewan"}
ShowMe = {"tag": "SHOWME", \
			 "filename": "/home/gautam/research/ml_data/web_files/showme", \
			 "description": "ShowMe mobile web data set"}
Twa = {"tag": "TWA", \
		 "filename": "/home/gautam/research/ml_data/web_files/twa", \
		 "description": "TWA mobile web data set"}
W98 = {"tag": "W98", \
		 "filename": "/home/gautam/research/ml_data/web_files/w98", \
		 "description": "World cup 98 web server files"}

WebFilesSet = (Calgary, ClarkNet, FlowSize, FtpSize, FtpTime, Nasa, Sask, ShowMe, Twa, W98)

"""
UNC Data set - flows
"""
Flow13 = {"tag": "UNC_FLOW_13", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_13", \
			 "description": "Flow sizes for april 13 2005"}
Flow14 = {"tag": "UNC_FLOW_14", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_14", \
			 "description": "Flow sizes for april 14 2005"}
Flow15 = {"tag": "UNC_FLOW_15", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_15", \
			 "description": "Flow sizes for april 15 2005"}
Flow16 = {"tag": "UNC_FLOW_16", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_16", \
			 "description": "Flow sizes for april 16 2005"}
Flow17 = {"tag": "UNC_FLOW_17", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_17", \
			 "description": "Flow sizes for april 17 2005"}
Flow18 = {"tag": "UNC_FLOW_18", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_18", \
			 "description": "Flow sizes for april 18 2005"}
Flow19 = {"tag": "UNC_FLOW_19", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_19", \
			 "description": "Flow sizes for april 19 2005"}
Flow20 = {"tag": "UNC_FLOW_20", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_20", \
			 "description": "Flow sizes for april 20 2005"}
FlowAl = {"tag": "UNC_FLOW_ALL", \
			 "filename": "/home/gautam/research/ml_data/unc/flows/flow_all", \
			 "description": "Flow sizes"}

"""
UNC Data set - session length
"""
Slen13 = {"tag": "UNC_SLEN_13", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_13", \
			 "description": "Session length for april 13 2005"}
Slen14 = {"tag": "UNC_SLEN_14", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_14", \
			 "description": "Session length for april 14 2005"}
Slen15 = {"tag": "UNC_SLEN_15", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_15", \
			 "description": "Session length for april 15 2005"}
Slen16 = {"tag": "UNC_SLEN_16", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_16", \
			 "description": "Session length for april 16 2005"}
Slen17 = {"tag": "UNC_SLEN_17", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_17", \
			 "description": "Session length for april 17 2005"}
Slen18 = {"tag": "UNC_SLEN_18", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_18", \
			 "description": "Session length for april 18 2005"}
Slen19 = {"tag": "UNC_SLEN_19", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_19", \
			 "description": "Session length for april 19 2005"}
Slen20 = {"tag": "UNC_SLEN_20", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_20", \
			 "description": "Session length for april 20 2005"}
SlenAl = {"tag": "UNC_SLEN_ALL", \
			 "filename": "/home/gautam/research/ml_data/unc/seslen/day_all", \
			 "description": "Session length"}

"""
UNC Data set - flow count
"""
Fcnt13 = {"tag": "UNC_FCNT_13", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_13", \
			 "description": "Flow count per session for april 13 2005"}
Fcnt14 = {"tag": "UNC_FCNT_14", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_14", \
			 "description": "Flow count per session for april 14 2005"}
Fcnt15 = {"tag": "UNC_FCNT_15", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_15", \
			 "description": "Flow count per session for april 15 2005"}
Fcnt16 = {"tag": "UNC_FCNT_16", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_16", \
			 "description": "Flow count per session for april 16 2005"}
Fcnt17 = {"tag": "UNC_FCNT_17", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_17", \
			 "description": "Flow count per session for april 17 2005"}
Fcnt18 = {"tag": "UNC_FCNT_18", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_18", \
			 "description": "Flow count per session for april 18 2005"}
Fcnt19 = {"tag": "UNC_FCNT_19", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_19", \
			 "description": "Flow count per session for april 19 2005"}
Fcnt20 = {"tag": "UNC_FCNT_20", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_20", \
			 "description": "Flow count per session for april 20 2005"}
FcntAl = {"tag": "UNC_FCNT_ALL", \
			 "filename": "/home/gautam/research/ml_data/unc/fcount/day_all", \
			 "description": "Flow count"}

"""
UNC Data set - Flow inter arrivals
"""
Nter13 = {"tag": "UNC_NTER_13", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_13", \
			 "description": "Flow interarrival across sessions for april 13 2005"}
Nter14 = {"tag": "UNC_NTER_14", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_14", \
			 "description": "Flow interarrival across sessions for april 14 2005"}
Nter15 = {"tag": "UNC_NTER_15", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_15", \
			 "description": "Flow interarrival across sessions for april 15 2005"}
Nter16 = {"tag": "UNC_NTER_16", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_16", \
			 "description": "Flow interarrival across sessions for april 16 2005"}
Nter17 = {"tag": "UNC_NTER_17", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_17", \
			 "description": "Flow interarrival across sessions for april 17 2005"}
Nter18 = {"tag": "UNC_NTER_18", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_18", \
			 "description": "Flow interarrival across sessions for april 18 2005"}
Nter19 = {"tag": "UNC_NTER_19", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_19", \
			 "description": "Flow interarrival across sessions for april 19 2005"}
Nter20 = {"tag": "UNC_NTER_20", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_20", \
			 "description": "Flow interarrival across sessions for april 20 2005"}
NterAl = {"tag": "UNC_NTER_ALL", \
			 "filename": "/home/gautam/research/ml_data/unc/interses/day_all", \
			 "description": "Flow interarrival"}


"""
UNC Data set - Flow intra arrivals
"""
Ntra13 = {"tag": "UNC_NTRA_13", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_13", \
			 "description": "Flow intra-arrival per session for april 13 2005"}
Ntra14 = {"tag": "UNC_NTRA_14", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_14", \
			 "description": "Flow intra-arrival per session for april 14 2005"}
Ntra15 = {"tag": "UNC_NTRA_15", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_15", \
			 "description": "Flow intra-arrival per session for april 15 2005"}
Ntra16 = {"tag": "UNC_NTRA_16", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_16", \
			 "description": "Flow intra-arrival per session for april 16 2005"}
Ntra17 = {"tag": "UNC_NTRA_17", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_17", \
			 "description": "Flow intra-arrival per session for april 17 2005"}
Ntra18 = {"tag": "UNC_NTRA_18", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_18", \
			 "description": "Flow intra-arrival per session for april 18 2005"}
Ntra19 = {"tag": "UNC_NTRA_19", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_19", \
			 "description": "Flow intra-arrival per session for april 19 2005"}
Ntra20 = {"tag": "UNC_NTRA_20", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_20", \
			 "description": "Flow intra-arrival per session for april 20 2005"}
NtraAl = {"tag": "UNC_NTRA_ALL", \
			 "filename": "/home/gautam/research/ml_data/unc/intrases/day_all", \
			 "description": "Flow intra-arrival"}

UncSet = (FlowAl, SlenAl)

SimR1 = {"tag": "SIM_R1", \
			 "filename": "/home/gautam/research/ml_data/rff_sim/run1", \
			 "description": "D1=U(1.0,10^6) D2=LGN(0.0,1.0) g=0.3 nu=0.001 initial nodes=60 total=10000"}
SimR2 = {"tag": "SIM_R2", \
			 "filename": "/home/gautam/research/ml_data/rff_sim/run2", \
			 "description": "D1=calgary.txt D2=LGN(0.0,1.0) g=0.3 nu=0.001 initial nodes=5 total=10000"}
SimR3 = {"tag": "SIM_R3", \
			 "filename": "/home/gautam/research/ml_data/rff_sim/run3", \
			 "description": "D1=LGN(1.0,2.0) D2=EXP(1/20.0) g=0.5 nu=0.2 initial nodes=20 total=20000"}

SimSet = (SimR1, SimR2, SimR3)

"""
All the data sets together
"""
AZURE_SET = 0
WEBFILE_SET = 1
UNC_SET = 2
SIM_SET = 3
DATASETS = (AzureWirelessSet, WebFilesSet, UncSet, SimSet)
#DATASETS = (SimSet)
