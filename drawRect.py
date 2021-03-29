import os
import time
import json
import threading
from tqdm import tqdm
import os.path as osp
import cv2 as cv
from argparse import ArgumentParser


def draw_txt(img, txtfile, output):
    img = cv.imread(img)

    data = []
    file = open(txtfile, 'r')
    lines = file.readlines()
    for id in range(len(lines)):
        data.append([float(i) for i in lines[id].split()])
        # yolo.txt
        weight = img.shape[1]
        height = img.shape[0]
        w = int(float(data[id][3]) * weight)
        h = int(float(data[id][4]) * height)
        x = int(float(data[id][1]) * weight - w / 2)
        y = int(float(data[id][2]) * height - h / 2)

        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5, 5, 0)

        a = data[id][0]  # 类别名称
        font = cv.FONT_HERSHEY_SIMPLEX  # 定义字体
        cv.putText(img, '{}'.format(a), (x, int(y - h / 2)), font, 0.5, (0, 0, 0), 4)

    cv.imwrite(output, img)
    file.close()


def draw_json(img, jsonfile, output):
    name = osp.split(img)[1]
    img = cv.imread(img)

    file = open(jsonfile)
    file_dict = json.load(file)
    for img_info in file_dict['images']:
        if img_info['file_name'] == name:
            for anno_info in file_dict['annotations']:
                if anno_info['image_id'] == img_info['id']:
                    x = int(anno_info['bbox'][0])
                    y = int(anno_info['bbox'][1])
                    h = int(anno_info['bbox'][3])
                    w = int(anno_info['bbox'][2])

                    cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2, 2, 0)

                    a = anno_info['category_id']  # 类别名称
                    font = cv.FONT_HERSHEY_SIMPLEX  # 定义字体
                    cv.putText(img, '{}'.format(a), (int(x + w / 2), y), font, 0.5, (0, 0, 0), 2)
                    # 图像，文字内容，坐标(右上角坐标) ，字体，大小，颜色，字体厚度

            cv.imwrite(output, img)
            break
        # else:
        #     print('img or json not exsit')


def Dyolo(input, output):
    # load images and labels
    imgpath = osp.join(input, 'imgs')
    labelpath = osp.join(input, 'labels')

    # match img with label
    if osp.isdir(imgpath) and osp.isdir(labelpath):
        imgs = sorted(os.listdir(imgpath))
        labels = sorted(os.listdir(labelpath))

        if not osp.exists(output):
            os.makedirs(output, exist_ok=True)

        with tqdm(total=len(imgs), desc='Imgs', leave=True, ncols=100, unit='img', unit_scale=True) as pbar:
            # with tqdm(total=len(imgs), ncols=100) as pbar:
            for img_name in imgs:
                # time.sleep(2)
                Tlabel = img_name.replace(osp.splitext(img_name)[1], '.txt')
                if Tlabel in labels:
                    txt = osp.join(labelpath, Tlabel)
                    img = osp.join(imgpath, img_name)
                    outputpath = osp.join(output, img_name)
                    draw_txt(img, txt, outputpath)
                else:
                    print('%s is not exist', Tlabel)
                    break
                pbar.update(1)


def Dcoco(input, output):
    # load images and labels
    imgpath = input
    labelpath = osp.join(osp.dirname(imgpath), 'annotations')

    # match img with label
    if osp.isdir(imgpath) and osp.isdir(labelpath):
        imgs = sorted(os.listdir(imgpath))
        if not osp.exists(output):
            os.makedirs(output, exist_ok=True)

        dir_inner = os.listdir(labelpath)
        for f in dir_inner:
            if osp.split(imgpath)[1] in f:
                jsonfile = osp.join(labelpath, f)

        with tqdm(total=len(imgs), desc='Imgs', leave=True, ncols=100, unit='img', unit_scale=True) as pbar:
            for img_name in imgs:
                # time.sleep(2)
                img = osp.join(imgpath, img_name)
                outputpath = osp.join(output, img_name)
                draw_json(img, jsonfile, outputpath)
                pbar.update(1)


def Draw():
    parser = ArgumentParser()
    parser.add_argument('--input', type=str, help='root path of labels and imgs for yolo, and path of imgs for coco')
    parser.add_argument('--Dstyle', type=str, help='style of dataset')
    parser.add_argument('--output', type=str, help='output pic file (or folder)')

    args = parser.parse_args()

    if args.Dstyle == 'yolo':
        Dyolo(args.input, args.output)
    elif args.Dstyle == 'coco':
        Dcoco(args.input, args.output)


if __name__ == '__main__':
    Draw()
