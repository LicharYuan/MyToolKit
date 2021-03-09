from MyToolKit.visualize import PlotSearch

def plot_kp():
    filename = '/home/tusimple/Projects/startup/kp_1222.pkl'
    plotor = PlotSearch(filename)
    plotor.plot_detsearch(xkeys="tlats",ykeys="recall")

def plot_mixkp():
    filename = "/home/tusimple/mixkp_enc0224.pkl"
    # filename = "/home/tusimple/mixkp_enc0224_id2.pkl"
    filename = "/home/tusimple/fpn_0302.pkl"
    # filename = "/home/tusimple/fpn_seed0_0302.pkl"
    filename = "/home/tusimple/mix_fpn_seed8.pkl"
    filename = "/home/tusimple/mix_fpn_seed8_fixbug.pkl"
    plotor = PlotSearch(filename)
    print(type(plotor.data[0]))


    plotor.plot_mixsearch(xkeys="tlats", ykeys_det=["car_ap", "bigcar_ap"], ykeys_kp=["recall"], ratio=1.0)

def plot_mixkpbo():
    # bo save as alist
    filename = "/home/tusimple/All_nets_at_202101212222.pkl"
    plotor = PlotSearch(filename)
    print(type(plotor.data[0]))
    plotor.plot_detsearch(xkeys="tlats", ykeys=["car_ap", "bigcar_ap"], )



if __name__ == '__main__':
    plot_mixkp()
    # plot_mixkpbo()

