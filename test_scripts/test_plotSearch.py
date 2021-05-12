from MyToolKit.visualize import PlotSearch, SamePlotSearch
from matplotlib import pyplot as plt
import sys

def plot_kp():
    filename = './data/pkl/kp_1222.pkl'
    plotor = PlotSearch(filename)
    plotor.plot_detsearch(xkeys="tlats",ykeys="recall")

def plot_mixkp():
    # filename = "/home/tusimple/mix_fpn_seed8.pkl"
    # filename_t = "/home/tusimple/mix_fpn_seed8_fixbug.pkl"
    # filename = "/home/tusimple/mix_fpn_seed8_xavier.pkl"
    # filename = "/home/tusimple/xavier_int8_30w.pkl"
    filename = "./data/pkl/xavier_op_seed12_int8_30w.pkl"
    # filename = sys.argv[1]
    plotor = PlotSearch(filename)
    # tplotor = PlotSearch(filename_t)
    # print(type(plotor.data[0]))

    plotor.plot_mixsearch(xkeys="tlats", ykeys_det=["car_ap", "bigcar_ap"], ykeys_kp=["recall"], ratio=1.0)
    # tplotor.plot_mixsearch(xkeys="tlats", ykeys_det=["car_ap", "bigcar_ap"], ykeys_kp=["recall"], ratio=0.7)

def plot_mixkpbo():
    # bo save as alist
    # filename = "/home/tusimple/All_nets_at_202101212222.pkl"
    filename = "./data/pkl/All_nets_at_202103161703.pkl"
    plotor = PlotSearch(filename)
    print(type(plotor.data[0]))
    # plotor.plot_detsearch(xkeys="tlats", ykeys=["car_ap", "bigcar_ap"], )
    plotor.plot_mixsearch(xkeys="tlats", ykeys_det=["car_ap", "bigcar_ap"], ykeys_kp=["recall"], ratio=0.95)

def plot_diff_plts():
    filename_t = "./data/pkl/mix_fpn_seed8_fixbug.pkl"
    filename_x = "./data/pkl/mix_fpn_seed8_xavier.pkl"
    filename = [filename_t, filename_x]
    plotor = SamePlotSearch(filename)
    plotor.plot_mixsearch(xkeys="tlats", ykeys_det=["car_ap", "bigcar_ap"], ykeys_kp=["recall"], ratio=1.0)


if __name__ == '__main__':
    plot_diff_plts()
    plot_mixkp()
    plot_kp()
    plot_mixkpbo()

