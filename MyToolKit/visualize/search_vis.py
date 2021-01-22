from MyToolKit.utils import  load_pkl, save_to_json
import numpy as np
from matplotlib import pyplot as plt
import time 

class PlotSearch(object):
    _print = True
    def __init__(self, saved_pkl, sort=True):
        self.data = load_pkl(saved_pkl)
        if sort and isinstance(self.data, dict):
            self.data = self._sort_data_byKey(self.data)

    @staticmethod
    def _sort_data_byKey(data):
        # in some case will shuffle data
        return sorted(data.items(), key=lambda x: x[0])
        

    @staticmethod    
    def plot(x, y, xlabel="latency", ylabel='AP', data=None, save_name='time'):
        fig, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.scatter(x, y, picker=True)
        pick_history = []

        def onpick(event):
            ind = event.ind
            if data is not None:
                if isinstance(data, np.ndarray):
                    print('onpick scatter:', ind, np.take(x, ind), np.take(y, ind), np.take(data, ind))
                    pick_history.extend(np.take(data, ind))
                elif isinstance(data, dict):
                    for ele in ind:
                        key = "Net_ID%d"%(ele)
                        print('onpick scatter:', ele, np.take(x, ind), np.take(y, ind), data[key])    
                        pick_history.append(data[key])
                elif isinstance(data, list):
                    for ele in ind:
                        print('onpick scatter:', ele, np.take(x, ele), np.take(y, ele), data[ele])
                        pick_history.append(data[ele])
                else:
                    print("Not support ", type(data))
            else:
                print('onpick scatter:', ind, np.take(x, ind), np.take(y, ind))
        fig.canvas.mpl_connect('pick_event', onpick)
        if save_name:
            save_name = time.strftime("%Y%m%d%H%M%S") if save_name=='time' else save_name
            plt.savefig("./{}.jpg".format(save_name))

        return pick_history
    
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
                        fig_save_name=None,
                        record=True,
                        record_path='./'

                        ):
        """ Plot latency-performance curve for DetSearch.
        It's format is : {"Net_ID": {"Eval": {},  "Lat":{} , ...  } }
        Return numpy """
        latency = []
        performance = []

        if isinstance(self.data, dict):
            data_items = self.data.items() 
        elif isinstance(self.data, list):
            if isinstance(self.data[0], tuple):
                # sort dict
                data_items = self.data 
            elif isinstance(self.data[0], dict):
                # re-sampler save format
                data_items = enumerate(self.data)
            else:
                raise TypeError("check data and element type")

        for net_id, net_info in data_items:
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
        record_history = PlotSearch.plot(latency, performance, str(xkeys), str(ykeys), self.data, fig_save_name)
        plt.show()
        if record:
            print("Recoding the point you have choosen (Number: {}) to {}".format(len(record_history),"./"))
            save_to_json(record_path, record_history)
