import os
import json


def load_json(path):
	with open(path, 'r') as f:
		json_dict = json.load(f)
		return json_dict

def coco2yolo(json_dict,save_path):
	categories=[i['id'] for i in json_dict['categories']]

	for i in json_dict['images']:
		W,H=i['width'],i['height']
		file_name=i['file_name']
		image_id=i['id']
		print(image_id)
		string=''
		for j in json_dict['annotations']:
			#print(j['category_id'])
			if j['image_id']==image_id:
				x,y,w,h=j['bbox']
				x_c,y_c=x+w/2,y+h/2
				string=string+str(categories.index(j['category_id']))+' '+str(x_c/W)+' '+str(y_c/H)+' '+str(w/W)+' '+str(h/H)+'\n'
		txt=open(os.path.join(save_path,file_name.split('.')[0]+'.txt'),'w')
		txt.write(string)
		txt.close()

if __name__=='__main__':
	json_path='./coco_orgin/annotations_trainval2017/annotations/instances_val2017.json'
	json_dict=load_json(json_path)
	coco2yolo(json_dict=json_dict,save_path='./labels_new_val/')