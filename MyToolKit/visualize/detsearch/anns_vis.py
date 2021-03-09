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
        for i,point in enumerate(scatter_list):
            x, y, vis = point
            marker = 'o' if vis<=0.1 else 'x'
            color =  ['red', 'green', 'blue', 'orange'] # left-front, left-back, right-back, right-front
            ax.scatter(x,y , marker=marker, s=10, color=color[i])

def plot_bbox_mask_ann(gt_bboxes, gt_masks, ax):
    """plot all bboxes and masks, TODO:check empty input"""
    for gt_bbox in gt_bboxes:
        plot_rect(gt_bbox, ax)
    for gt_mask in gt_masks:
        plot_poly(gt_mask, ax)

def plot_kp_ann(gt_kp, ax):
    for kp in gt_kp:
        if len(kp) == 0:
            continue
        plot_kp(kp, ax)

if __name__ == '__main__':
    import numpy as np
    array = np.array
    img_path = '/home/tusimple/1545794562917336093.jpg'
    img = plt.imread(img_path)
    fig,ax = plt.subplots(1)
    ax.imshow(img)
    ann =   {'dataset_id': 'unknow', 'gt_keypoint': [[], array([[136.34372123, 192.70775646,   1.        ],
       [143.19588945, 194.05519718,   1.        ],
       [158.17176226, 193.83062373,   0.        ],
       [148.49395766, 192.25860955,   0.        ]]), [], array([[ 15.84641151, 177.57652352,   1.        ],
       [ 15.80120133, 175.27689135,   0.        ],
       [  0.42973943, 175.42061836,   0.        ],
       [  0.42973943, 177.57652352,   0.        ]]), []], 
       'image_url': '/mnt/truenas/datasets_addon/v3/5c4187c2dbdbe00001f4dddb/raw/1545794562917336093.jpg', 
       'ts': 'unknow', 'h': 1024, 'gt_class': ['bigcar', 'car', 'bigcar', 'bigcar', 'bigcar'], 
       'w': 576, 'gt_bbox': [[178.80180520421055, 168.3204830067451, 197.73356894315793, 190.55325489192154], 
                            [135.1428257684211, 178.11048199027454, 159.0194531705264, 194.2797706340393], 
                            [87.47682352505264, 155.76033538610207, 100.64428905094739, 174.26518794507723], 
                            [0.3907103258947527, 149.1129611658877, 16.666375868631597, 177.82243144670542], 
                            [-5.131112965389446, 153.8615668377267, 5.900171458021077, 189.64959236925927]], 
       'task_id': '5c4187c2dbdbe00001f4dddb', 'sensor': 'unknow'}

    det = [[1.0759070e+03, 1.6627689e+02, 1.7540730e+03, 1.0913433e+03, 9.8701560e-01]]

    kp = array([[[1.08456311e+03, 8.69914062e+02, 2.45817825e-01, 0.00000000e+00],
        [1.11022302e+03, 1.02534570e+03, 2.62316763e-01, 1.00000000e+00],
        [1.68604248e+03, 1.03211792e+03, 5.49791276e-01, 1.00000000e+00],
        [1.53629810e+03, 8.64935669e+02, 4.17951681e-02, 0.00000000e+00]]])


    for bbox in ann['gt_bbox']:
        plot_rect(bbox, ax)

    # for bbox in det:
    #     plot_rect(bbox[:4], ax, c='b')
    print(type(ann))
    plot_kp_ann(ann['gt_keypoint'], ax)    

    plt.show()





