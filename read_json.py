import json
import os
import os.path as osp
import cv2
from tqdm import tqdm
from argparse import ArgumentParser


def cutimg(path, cutpath, key, left, top, height, width, label):
    img = cv2.imread(osp.join(path, key))    #, -1
    imgH=img.shape[0]   #高度
    imgW=img.shape[1]
    save_path = osp.join(cutpath, "{0}".format(label))  # 保存的路径

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # 裁剪图像,图像左上角的坐标(起始坐标)
    xmax = left + width
    ymax = top + height
    if left < 0:
        left = 0
    if top < 0:
        top = 0
    if xmax > imgW:
        xmax = imgW
    if ymax > imgH:
        ymax = imgH

    imgCrop = img[top:ymax, left:xmax]
    # print(imgCrop)
    img_path = save_path + '/' + "{0}_{1}_{2}_{3}_{4}".format(osp.splitext(key)[0], left, top, height, width) + osp.splitext(key)[1]
    cv2.imwrite(img_path, imgCrop)

def main():
    parser = ArgumentParser()
    parser.add_argument('--filename', type=str, help='path of json')
    parser.add_argument('--imgpath', type=str, help='path of img')
    parser.add_argument('--cutpath', type=str, help='path for saving imgs')

    args = parser.parse_args()

    file = open(args.filename)
    json_list = json.load(file)

    with tqdm(total=len(json_list), desc='Imgs', leave=True, ncols=100, unit='img', unit_scale=True) as pbar:
        for key in json_list:
            akey = json_list[key]
            alabel = akey['label']
            ax = akey['left']
            ay = akey['top']
            ah = akey['height']
            aw = akey['width']

            for no in range(len(alabel)):
                cutimg(args.imgpath, args.cutpath, key, int(ax[no]), int(ay[no]), int(ah[no]), int(aw[no]), int(alabel[no]))
            # print(key)

            pbar.update(1)

if __name__ == '__main__':
    main()



