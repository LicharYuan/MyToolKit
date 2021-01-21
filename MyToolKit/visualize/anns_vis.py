from matplotlib import pyplot as plt
import matplotlib.patches as patches

def plot_poly(polys, ax, c='b'):
    for poly in polys:
        poly_patch = np.zeros((len(poly)//2, 2))
        for i, ele in enumerate(poly):
            poly_patch[i//2][i%2] = ele
        poly_patch = patches.Polygon(poly_patch, linewidth=1,edgecolor=c,facecolor='none')
        ax.add_patch(poly_patch)

def plot_rect(rect, ax, rformat='xyxy', c='r'):
    if rformat == 'xyxy':
        x1, y1, x2, y2 = rect
        w , h = x2 - x1, y2 - y1
    elif rformat == 'xywh':
        x1, y1, w, h = rect
    else:
        raise NotImplementedError
    rect_patch = patches.Rectangle((x1, y1), w, h, linewidth=1,edgecolor=c,facecolor='none')
    ax.add_patch(rect_patch)

def plot_kp(scatter_list, ax, rformat='invs', c='r'):
    if rformat == 'invs':
        for point in scatter_list:
            plt.scatter(point[0], point[1])

def plot_bbox_mask_ann(gt_bboxes, gt_masks, ax):
    """plot all bboxes and masks, TODO:check empty input"""
    for gt_bbox in gt_bboxes:
        plot_rect(gt_bbox, ax)
    for gt_mask in gt_masks:
        plot_poly(gt_mask, ax)

def plot_kp_ann(gt_kp, ax):
    for kp in gt_kp:
        plot_kp(kp, ax)

if __name__ == '__main__':
    import numpy as np
    array = np.array
    img_path = '/home/tusimple/15868081278807080543.jpg'
    img = plt.imread(img_path)
    fig,ax = plt.subplots(1)
    ax.imshow(img)
    ann =  {'ts': 1577772830225191424, 'image_url': '/mnt/truenas/datasets_addon/v3/5e94c538c3cda0ae6342f69e/raw/15868081278807080543.jpg', 'w': 2048, 'h': 1152, 
        'gt_keypoint': [array([[1.14132214e+03, 9.40956826e+02, 0.00000000e+00],
       [1.10609572e+03, 1.00912147e+03, 1.00000000e+00],
       [1.68357601e+03, 1.01592046e+03, 1.00000000e+00],
       [1.64903506e+03, 9.48008909e+02, 0.00000000e+00]]), array([[1.77147167e+03, 5.62508467e+02, 0.00000000e+00],
       [1.76302838e+03, 5.87565389e+02, 0.00000000e+00],
       [1.99449518e+03, 5.87788762e+02, 1.00000000e+00],
       [1.94852946e+03, 5.61678451e+02, 1.00000000e+00]]), [], [], [], [], array([[192.4759552,  81.6195456,   0.       ],
       [137.8074624,  84.7726848,   1.       ],
       [209.6254976,  86.4874368,   1.       ],
       [259.8504448,  82.4864256,   1.       ]]), [], [], [], [], []], 'task_id': '5e94c538c3cda0ae6342f69e', 
       'gt_bbox': [[995.8488064, 153.74880000000002, 1779.0056448, 1017.7527168], [1754.3596032, 293.7704832, 2002.5597952, 588.4804224], 
       [1148.0920064, -13.4995968, 1447.6814336, 299.3942016], [522.8128256, 24.1208064, 561.1593728, 51.2105472], [545.9990528, 24.5673216, 571.7121024, 48.3825024],
        [493.2743168, -37.9459584, 549.9394048, 27.7318656], [128.3690496, -21.744345600000003, 274.6208256, 86.7529728], [252.9490944, -17.4112128, 310.4987136, 43.6747392], 
        [80.2023424, 42.943564800000004, 89.80992, 59.3284608], [62.1289472, 44.563046400000005, 70.024192, 61.138368], [43.29472, 46.2776832, 52.141056, 63.9962496], 
        [11.6187136, 47.8971648, 19.894272, 65.615616]], 
        'dataset_id': '2019-12-31-14-12-09', 'sensor': '/camera4/image_color/compressed', 
        'gt_class': ['bigcar', 'car', 'bigcar', 'car', 'car', 'bigcar', 'bigcar', 'bigcar', 'traffic-cone', 'traffic-cone', 'traffic-cone', 'traffic-cone']}


    det = [[1.0759070e+03, 1.6627689e+02, 1.7540730e+03, 1.0913433e+03, 9.8701560e-01]]

    kp = array([[[1.08456311e+03, 8.69914062e+02, 2.45817825e-01, 0.00000000e+00],
        [1.11022302e+03, 1.02534570e+03, 2.62316763e-01, 1.00000000e+00],
        [1.68604248e+03, 1.03211792e+03, 5.49791276e-01, 1.00000000e+00],
        [1.53629810e+03, 8.64935669e+02, 4.17951681e-02, 0.00000000e+00]]])


    for bbox in ann['gt_bbox']:
        plot_rect(bbox, ax)

    for bbox in det:
        plot_rect(bbox[:4], ax, c='b')

    # plot_kp_ann(ann['gt_keypoint'], ax)    

    plt.show()





