from MyToolKit.visualize import PlotSearch

def plot_kp():
    filename = '/home/tusimple/Projects/startup/kp_1222.pkl'
    plotor = PlotSearch(filename)
    plotor.plot_detsearch(xkeys="tlats",ykeys="recall")

def plot_mixkp():
    filename = "/home/tusimple/mixkp_enc0121.pkl"
    plotor = PlotSearch(filename)
    print(type(plotor.data[0]))
    plotor.plot_detsearch(xkeys="tlats", ykeys=["car_ap", "bigcar_ap"])

def plot_mixkpbo():
    # bo save as alist
    filename = "/home/tusimple/All_nets_at_202101212222.pkl"
    plotor = PlotSearch(filename)
    print(type(plotor.data[0]))
    plotor.plot_detsearch(xkeys="tlats", ykeys=["car_ap", "bigcar_ap"], )

if __name__ == '__main__':
    plot_mixkpbo()

