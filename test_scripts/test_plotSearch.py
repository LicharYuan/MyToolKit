from MyToolKit.visualize import PlotSearch

def plot_kp():
    filename = '/home/tusimple/Projects/startup/kp_1222.pkl'
    plotor = PlotSearch(filename)
    plotor.plot_detsearch(xkeys="tlats",ykeys="recall")

if __name__ == '__main__':
    plot_kp()

