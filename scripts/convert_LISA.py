# -*- coding: utf-8 -*-
"""
Created on 02/26/2016

This script is to convert the LISA_dataset to appropriate format needed by YOLO 

@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
import csv
from os import walk, getcwd
from PIL import Image
from shutil import copyfile

#classes = ["stop", "pedestrianCrossing", "turnleft", "slow","signalAhead", "yieldAhead"]
classes = ["stop","pedestrianCrossing", "signalAhead"]

def convert(size, box):
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

def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def processROI(xmin, ymin, xmax, ymax, img_path, txt_path, cls_id):
    im=Image.open(img_path)
    w= int(im.size[0])
    h= int(im.size[1])

    #print(w, h)
    b = (float(xmin), float(xmax), float(ymin), float(ymax))
    bb = convert((w,h), b)
    print(bb)
    with open(txt_path, "w") as txt_file:
        txt_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

"""-------------------------------------------------------------------""" 
COPY_IMGS = 'true'

""" Configure Paths """
Lisa4Yolo_dataset = "../LISA/LISA4YOLO_DATASET"
images_fold = os.path.join(Lisa4Yolo_dataset , "images")
labels_fold = os.path.join(Lisa4Yolo_dataset , "labels")
createFolder(Lisa4Yolo_dataset)
createFolder(images_fold)
createFolder(labels_fold)

#cls_id = classes.index(cls)

""" Training image list (write)"""
train_file = open('%s/training.txt'%(Lisa4Yolo_dataset), 'w')

""" LISA dataset annotations (Read) """
lisa_file = open('../LISA/allAnnotations.csv', 'r')
reader = csv.reader(lisa_file,delimiter=';')

""" Process """
for row in reader:
    #print(row[0]
    img_name = os.path.basename(row[0])
    base_name, img_ext = os.path.splitext(img_name)
    annotate_tag = row[1]

    if(img_ext == '.png' and annotate_tag in classes):
        createFolder(os.path.join(images_fold, annotate_tag))
        createFolder(os.path.join(labels_fold, annotate_tag))

        """ Copy images to folders """
        img_path = os.path.join(images_fold, annotate_tag, img_name)
        if COPY_IMGS=='true' and not os.path.exists(img_path):
            copyfile(row[0], img_path)

        """ Prepare for output text files """
        txt_name = base_name + '.txt'
        txt_path = os.path.join(labels_fold, annotate_tag, txt_name)
        print("Output text file:" + txt_path)

        """ Convert the data to YOLO format """
        cls_id = classes.index(annotate_tag)
        processROI(row[2],row[3],row[4],row[5],img_path,txt_path,cls_id)

        """ Save those images with bb into list"""
        train_file.write(img_path + '\n')
train_file.close()
