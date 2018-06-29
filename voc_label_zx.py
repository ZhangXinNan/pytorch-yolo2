#encoding=utf8
import xml.etree.ElementTree as ET
# import pickle
import os
# from os import listdir, getcwd
# from os.path import join

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert(size, box):
    '''x,y是中心坐标，x,y,w,h分别除以图像宽高'''
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id, in_file, out_file):
    # in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    # out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text # 0 表示容易识别，1 表示难以识别。
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = os.getcwd()
# 读取每年（2012、2007）、每类（train、val）数据集
for year, image_set in sets:
    print year, image_set
    # 存结果文件夹, image_id.txt(cls_id,x,y,w,h)
    labels_dir = 'VOCdevkit/VOC%s/labels/'%(year)
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    # 读取train/val的文件id
    image_ids_file = 'VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)
    image_ids = open(image_ids_file).read().strip().split()
    # 输出文件列表
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    print '\t', 'input id:', image_ids_file
    print '\t', 'output list:', '%s_%s.txt'%(year, image_set)

    for image_id in image_ids:
        # 输出文件列表
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
        in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
        out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
        convert_annotation(year, image_id, in_file, out_file)
        out_file.close()
        in_file.close()
    list_file.close()

