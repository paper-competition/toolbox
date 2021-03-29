import json
import os
import os.path as osp
import time
from tqdm import tqdm
from argparse import ArgumentParser
import toCOCO

parser = ArgumentParser()
parser.add_argument('--filename', type=str, help='path of json')
parser.add_argument('--imgpath', type=str, help='path of img')
parser.add_argument('--save', type=str, help='path for saving json')
args = parser.parse_args()

COCO_DICT = ['images', 'annotations', 'categories']
IMAGES_DICT = ['file_name', 'height', 'width', 'id']
ANNOTATIONS_DICT = ['image_id', 'iscrowd', 'area', 'bbox', 'category_id', 'id']
CATEGORIES_DICT = ['id', 'name']
YOLO_CATEGORIES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ]


def main():
    file = open(args.filename)
    json_list = json.load(file)

    categories_dict = toCOCO.generate_categories_dict(YOLO_CATEGORIES)
    imgname = sorted(os.listdir(args.imgpath))
    images_dict = toCOCO.generate_images_dict(imgname, args.imgpath)

    # with tqdm(total=len(json_list), desc='Imgs', leave=True, ncols=100, unit='img', unit_scale=True) as pbar:
    id = 0
    annotations_dict = []
    for key in json_list:
        image_id = int(osp.splitext(key)[0])
        akey = json_list[key]
        alabel = akey['label']
        ax = akey['left']
        ay = akey['top']
        ah = akey['height']
        aw = akey['width']

        for no in range(len(alabel)):
            bbox = [int(ax[no]), int(ay[no]), int(aw[no]), int(ah[no])]
            category_id = int(alabel[no]) + 1
            area = int(ah[no]) * int(aw[no])
            # dict = {'image_id': image_id, 'iscrowd': 0, 'area': area, 'bbox': bbox, 'category_id': category_id,
            #         'id': id}
            dict = {'image_id': image_id, 'iscrowd': 0, 'area': area, 'bbox': bbox, 'category_id': 1,
                    'id': id}
            annotations_dict.append(dict)
            id = id + 1

        # pbar.update(1)

    content = {COCO_DICT[0]: images_dict, COCO_DICT[1]: annotations_dict, COCO_DICT[2]: categories_dict}
    # print(content)
    toCOCO.save_json(content, args.save)


if __name__ == '__main__':
    main()
