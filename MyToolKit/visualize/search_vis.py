from MyToolKit.utils import  load_pkl
import numpy as np
from matplotlib import pyplot as plt
import time 

class PlotSearch(object):
    _print = True
    def __init__(self, saved_pkl):
        self.data = load_pkl(saved_pkl)

    @staticmethod    
    def plot(x, y, xlabel="latency", ylabel='AP', data=None, save_name='time'):
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.scatter(x, y, picker=True)

        def onpick(event):
            ind = event.ind
            if data is not None:
                if isinstance(data, np.ndarray):
                    print('onpick scatter:', ind, np.take(x, ind), np.take(y, ind), np.take(data, ind) )
                elif isinstance(data, dict):
                    # key = "Best" if ind==0 else "Net_ID%d"%(ind-1)
                    if isinstance(ind, (np.ndarray, list)):
                        for ele in ind:
                            key = "Net_ID%d"%(ele)
                            print('onpick scatter:', ind, np.take(x, ind), np.take(y, ind), data[key])    
                    else:
                        key = "Net_ID%d"%(ind)
                        print('onpick scatter:', ind, np.take(x, ind), np.take(y, ind), data[key])
            else:
                print('onpick scatter:', ind, np.take(x, ind), np.take(y, ind))
        fig.canvas.mpl_connect('pick_event', onpick)
        if save_name:
            save_name = time.strftime("%Y%m%d%H%M%S") if save_name=='time' else save_name
            # time.strftime()
            plt.savefig("./{}.jpg".format(save_name))
        plt.show()
    
    @staticmethod
    def _get_mkeys(res, keys):
        assert isinstance(res, dict)
        try:
            if isinstance(keys, (list, tuple)):
                vals = np.array([res[key] for key in keys])
            elif isinstance(keys, (str)):
                vals = np.array(res[keys])
            else:
                print("ValueError:", f"Got {type(keys)}")
            return np.mean(vals)
        except KeyError:
            print(f"Try to get {keys} from {res.keys()}")
        

    def plot_detsearch(self, res_key= "eval_res" , 
                        xkeys="tlats", 
                        ykeys=["car/pick_up/emergency_ap", "bigcar_ap", "bus_ap"],
                        ):
        """ Plot latency-performance curve for DetSearch.
        It's format is : {"Net_ID": {"Eval": {},  "Lat":{} , ...  } }
        Return numpy """
        latency = []
        performance = []
        for net_id, net_info in self.data.items():
            res = net_info[res_key]
            xdata = self._get_mkeys(net_info, xkeys)
            ydata = self._get_mkeys(res, ykeys)
            if xdata is not None and ydata is not None:
                latency.append(xdata)
                performance.append(ydata)

        if len(latency) == 0:
            exit_info = "###########\n NO DATA \n  0A0  \n###########"
            exit(exit_info)

        latency = np.array(latency)
        performance = np.array(performance)
        PlotSearch.plot(latency, performance, str(xkeys), str(ykeys), self.data)

def main():
    filename = '/home/tusimple/Projects/startup/reid_mxnet_1218.pkl'
    plotor = PlotSearch(filename)
    plotor.plot_detsearch(ykeys="best_acc")



