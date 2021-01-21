from MyToolKit.visualize import PlotSearch

def plot_kp():
    filename = '/home/tusimple/Projects/startup/kp_1222.pkl'
    plotor = PlotSearch(filename)
    plotor.plot_detsearch(xkeys="tlats",ykeys="recall")

def plot_mixkp():
    filename = "/home/tusimple/mixkp_enc0121.pkl"
    plotor = PlotSearch(filename)
    # print(plotor.data)
    plotor.plot_detsearch(xkeys="tlats", ykeys=["car_ap", "bigcar_ap", "bus_ap"])

if __name__ == '__main__':
    plot_mixkp()

