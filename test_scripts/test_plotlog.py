import argparse
from MyToolKit.visualize import plot_log
def main():
    parser = argparse.ArgumentParser("Plot log")
    parser.add_argument("--log", help="the log path", type=str)
    parser.add_argument("--keys", help="the plot key", type=str, nargs='+')
    parser.add_argument("--save", help="save the fig path", type=str, default='./')
    args = parser.parse_args()
    print(args.keys)
    plot_log(args.log, args.keys, savepath=args.save)

if __name__ == '__main__':
    main()
