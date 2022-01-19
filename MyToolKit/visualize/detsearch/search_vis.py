from MyToolKit.utils import  load_pkl, save_to_json
import numpy as np
from matplotlib import pyplot as plt
import time 

class NotCoveredDict(dict):
    """if the key is conflict, it wont convert original data """
    def not_covered_update(self, d):
        d_keys = d.keys()
        origin_keys = self.keys()
        for key in d_keys: 
            if key in origin_keys:
                new_key = key + "_new"
                d[new_key] = d.pop(key)
        return super().update(d)

class PlotSearch(object):
    _print = True
    def __init__(self, saved_pkl, sort=True):
        self.data = load_pkl(saved_pkl)
        if sort and isinstance(self.data, dict):
            self.data = self._sort_data_byKey(self.data)

    @staticmethod
    def _sort_data_byKey(data):
        # sort by ID, after sort the data become to list, for plot pick data
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

    def _preprocess_data(self):
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
        return data_items

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

        data_items = self._preprocess_data()
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
    
    def plot_mixsearch(self, res_key= "eval_res" , 
                        xkeys="tlats", 
                        ykeys_det=["car_ap", "bigcar_ap"],
                        ykeys_kp = ["recall"],
                        ratio = 0.7,
                        fig_save_name=None,
                        record=True,
                        record_path='./'
                        ):
        assert ratio >=0 and ratio <=1
        latency = []
        performance = []
        data_items = self._preprocess_data()
        for net_id, net_info in data_items:
            res = net_info[res_key]
            xdata = self._get_mkeys(net_info, xkeys)
            ydata_det = self._get_mkeys(res, ykeys_det)
            ydata_kp = self._get_mkeys(res, ykeys_kp)
            # print(ydata_kp, ydata_det)
            ydata = ydata_det * ratio + ydata_kp * (1-ratio)
            if xdata is not None and ydata is not None:
                latency.append(xdata)
                performance.append(ydata)

        if len(latency) == 0:
            exit_info = "###########\n NO DATA \n  0A0  \n###########"
            exit(exit_info)

        latency = np.array(latency)
        performance = np.array(performance)
        record_history = PlotSearch.plot(latency[:20], performance[:20], str(xkeys), str(ykeys_det+ykeys_kp)+str(ratio), self.data, fig_save_name)
        plt.show()
        if record:
            print("Recoding the point you have choosen (Number: {}) to {}".format(len(record_history),"./"))
            save_to_json(record_path, record_history)


class SamePlotSearch(PlotSearch):
    """Plot Multi PKL input for SAME PKL .
    Some latency test on Mobile and some test on 2080 Ti. 
    """
    def __init__(self, saved_pkl, **kwargs):
        assert isinstance(saved_pkl, list)
        self.nums_pkl = len(saved_pkl)
        assert self.nums_pkl == 2, "current not support > 3 "
        self.saved_pkl = saved_pkl
        platf = kwargs.pop("platf", None)
        self._pkl_id = range(self.nums_pkl) if platf else platf
        self._build_data()

    def _build_data(self):
        self.data = NotCoveredDict()
        for spkl in self.saved_pkl:
            data = load_pkl(spkl)
            self.data.not_covered_update(data)
    
    
    @staticmethod    
    def plot(x, y, x_new, y_new, xlabel="latency", ylabel='AP', data=None, save_name='time', x1lim=[4, 15], x2lim=[50, 200]):
        fig, ax = plt.subplots()
        ax_new = ax.twinx()
        # ax.set_xlabel(xlabel)
        ax.set_xlabel("Performance")
        # ax.set_ylabel(ylabel)
        ax.set_ylabel("Latency")
        # ax.set_xlim(x1lim[0], x1lim[1])
        ax.set_ylim(x1lim[0], x1lim[1])
        # ax_new.set_xlim(x2lim[0], x2lim[1])
        ax_new.set_ylim(x2lim[0], x2lim[1])
        ax_new.scatter(y_new, x_new, color='green', label="Xavier")
        ax.scatter( y, x, label="RTX 2080Ti")            
        ax.legend(loc=2)
        ax_new.legend(loc=1)
        
    def plot_mixsearch(self, res_key= "eval_res" , 
                        xkeys="tlats", 
                        ykeys_det=["car_ap", "bigcar_ap"],
                        ykeys_kp = ["recall"],
                        ratio = 0.7,
                        fig_save_name=None,
                        x1lim=[4, 15],
                        x2lim=[50, 200],
                        ):
        assert ratio >=0 and ratio <=1
        latency = []
        new_latency = []
        performance = []
        new_performance = []
        data_items = self._preprocess_data()
        for net_id, net_info in data_items:
            res = net_info[res_key]
            xdata = self._get_mkeys(net_info, xkeys)
            ydata_det = self._get_mkeys(res, ykeys_det)
            ydata_kp = self._get_mkeys(res, ykeys_kp)
            # print(ydata_kp, ydata_det)
            ydata = ydata_det * ratio + ydata_kp * (1-ratio)
            if xdata is not None and ydata is not None:
                if "new" in net_id:
                    new_latency.append(xdata)
                    new_performance.append(ydata)
                else:
                    latency.append(xdata)
                    performance.append(ydata)

        if len(latency) == 0:
            exit_info = "###########\n NO DATA \n  0A0  \n###########"
            exit(exit_info)

        latency = np.array(latency)
        performance = np.array(performance)
        new_latency = np.array(new_latency)
        new_performance = np.array(new_performance)
        SamePlotSearch.plot(latency, performance, new_latency, new_performance,
            str(xkeys), str(ykeys_det+ykeys_kp)+str(ratio), self.data, fig_save_name, x1lim, x2lim)
        plt.show()