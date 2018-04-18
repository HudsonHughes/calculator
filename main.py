from get_klines import *
import json
from date_conversion import *
from binance.client import Client
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import glob
import tkinter
import csv
from table import *

min_color_int = 0
max_color_int = 16777215

currs = ["XVG","EOS","ADA","GRS","TRX","XRP","ONT","ELF","XLM","WAN","PPT","BNB","ICX","NEO","NCASH","LTC","OMG","IOTA","CMT","VEN","CTR","DLT","WTC","GTO","AION","POA","LRC","SUB","ZIL","ZRX","IOST","NANO","BLZ","STORM","WPR","XEM","BAT","POE","LEND","SNT","XMR","CDT","BRD","QTUM","DGD","BCC","LINK","POWR","ETC","LSK","AST","TRIG","MDA","QSP","QLC","DASH","FUN","STEEM","OST","ENJ","FUEL","RLC","KNC","WABI","BTS","MCO","VIBE","MTH","APPC","NEBL","REQ","SNGLS","AMB","GVT","TNT","STRAT","BQX","BTG","RPX","AE","CND","TNB","MANA","MOD","MTL","SALT","ENG","HSR","CHAT","WAVES","ARK","BNT","KMD","ZEC","WINGS","EVX","BCPT","NULS","RDN","ARN","PIVX","VIB","YOYO","SNM","ICN","RCN","DNT","OAX","ADX","SYS","LUN","INS","STORJ","EDO","GXS","BCD","NAV","VIA","XZC"]
currs_data = np.array([])
def epoch2human(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(int(epoch)/1000.0))

def find_exchange_record (name):
	files = glob.glob('exchanges/*' + name + '*')
	return files[0]

def get_np_from_path (path):
	return np.genfromtxt(path, delimiter='\t')[:, 2:-1]

def rlerp(v, mn, mx):
	if(mn == mx):
		return 0
	return (v - mn) / (mx - mn)

currs=['GRS']
for curr in currs:
	arr = get_np_from_path(find_exchange_record(curr))
	arr = np.clip(arr, 0.00000000000001, np.finfo('d').max)
	arr=arr[:200,:11]

	rows = np.shape(arr)[0]
	cols = np.shape(arr)[1]
	root = tkinter.Tk()
	headers=[
		'Open Time',
		'Open',
		'High',
		'Low',
		'Close',
		'Volume',
		'Close Time',
		'Q A V',
		'Number of trades',
		'T B B A V',
		'T B Q A V',
	]
	table = Table(root, headers, column_minwidths=[110]*12, date_cols=[0, 6])
	table.pack(padx=10, pady=10)

	colors = np.chararray(arr.shape, itemsize=7)
	maxs = np.amax(arr, axis=0)
	mins = np.amin(arr, axis=0)
	for c in range(cols):
		for r in range(rows):
			colors[r,c] = str('#' + '{0:06X}'.format(int(rlerp(arr[r, c], mins[c], maxs[c]) * max_color_int)))

	table.set_colors(colors)
	table.set_data(arr)




	root.update()
	root.geometry("%sx%s" % (root.winfo_reqwidth(), 250))

	root.mainloop()





	exit()

# fetch 1 minute klines for the last day up until now
symbol = "KCS-BTC"
start = "1 Dec, 2017"
end = "1 Jan, 2018"
interval = "30"



for curr in currs:
	print(curr)
	klines = get_historical_klines(curr + "ETH", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
	print(len(klines))
	data = np.array(klines)

	# x = (data[:,0].astype(np.int64)) / 1000
	# x = x - 25200
	# secs = mdate.epoch2num(x)
	# y = data[:,5].astype(np.float64)

	# fig, ax = plt.subplots()
	#
	# # Plot the date using plot_date rather than plot
	# ax.plot_date(secs, y)
	#
	# # Choose your xtick format string
	# date_fmt = '%d-%m-%y %H:%M:%S'

	# Use a DateFormatter to set the data to the correct format.
	# date_formatter = mdate.DateFormatter(date_fmt)
	# ax.xaxis.set_major_formatter(date_formatter)
	#
	# # Sets the tick labels diagonal so they fit easier.
	# fig.autofmt_xdate()
	#
	# plt.show()

	for k in klines:
		k.insert(0, epoch2human(k[0]))
		k.insert(1, epoch2human(k[7]))
	# open a file with filename including symbol, interval and start and end converted to seconds
	with open(
	    "exchanges/Kucoin_{}_{}_{}-{}.json".format(
	        curr+"-ETH",
	        interval,
	        date_to_seconds(start),
	        date_to_seconds(end)
	    ),
	    'w' # set file write mode
	) as f:
		for row in klines:
			line = ""
			for cell in row:
				line = line + str(cell) + "\t"
			f.write(line + "\n")



	# # fetch 30 minute klines for the last month of 2017
	# klines = get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
	#
	# # fetch weekly klines since it listed
	# klines = get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")