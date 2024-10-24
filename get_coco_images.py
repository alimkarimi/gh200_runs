"""
Script to get (using wget) Coco images for classification
"""
from pycocotools.coco import COCO
import PIL
from PIL import Image
import os
import pathlib
from argparse import ArgumentParser

parser = ArgumentParser(description="Select which dataset to pull")
parser.add_argument('-train', type=bool, help='Download training images from COCO', default=False)
parser.add_argument('-val', type = bool, help='Download validation images from COCO', default=False)

args = parser.parse_args()
print(args)

def display_categories():
    dataType='train2014'
    annFile='annotations/instances_{}.json'.format(dataType)
    # initialize COCO api for instance annotations
    coco=COCO(annFile)
    # display COCO categories and supercategories
    cats = coco.loadCats(coco.getCatIds())
    nms=[cat['name'] for cat in cats]
    print('COCO categories: \n{}\n'.format(' '.join(nms)))

    nms = set([cat['supercategory'] for cat in cats])
    print('COCO supercategories: \n{}'.format(' '.join(nms)))

    return coco

def get_training_images():
    catNms=['airplane','bus','cat', 'dog', 'pizza']#'bicycle', 'tv', 'book', 'toothbrush', 'bat', 'surfboard', 'hot dog']
    catIds = coco.getCatIds(catNms=catNms); #get a list category ids for each category name 
    ###Create training data set ###
    for n, cat_id in enumerate(catIds): ##for each category id
        print('in category id:,',cat_id)
        imgIds = coco.getImgIds(catIds = cat_id) #for each category id, get a list of img ids
        print(imgIds[:10]) #printing first 10 image ids
        pathlib.Path('train_orig/' + catNms[n]).mkdir(parents=True, exist_ok=True) #create a path to store 
    #     training data for the current category
        coco.download(tarDir = 'train_orig/' + catNms[n], imgIds = imgIds[0:1500]) #download first 1500 image ids 
    #     into the specified directory
        d = os.listdir('train_orig/' + catNms[n]) #create list of files in the created directory. This list has 1500 
    #     jpg file names
    #     print('list of files in d', d)
        for img in d: #iterate through list of downloaded images. Resize them to 64 x 64.
            
            try:
                temp_img = Image.open('train_orig/' + catNms[n] + '/' + img) #open image
                temp_img = temp_img.resize((64,64)) #resize
                save_path = 'train/' + catNms[n] + '/' # Create the folder if it doesn't exist
                os.makedirs(save_path, exist_ok=True)  # Create the folder if it doesn't exist
                temp_img.save(fp = save_path + 'resized_' + img) #overwrite image with the 64 x 64 version
            except OSError:
                print(f'failed on {save_path, img}')

                
            ## save function parameters:
    #         fp – A filename (string), pathlib.Path object or file object.
    #         format – Optional format override. If omitted, the format to use is determined from the 
    #         ##filename extension.
    #         If a file object was used instead of a filename, this parameter should always be used.

def get_validation_images():
    ###Create validation dataset ###
    catNms=['airplane','bus','cat', 'dog', 'pizza']# 'bicycle', 'tv', 'book', 'toothbrush', 'bat', 'surfboard', 'hot dog']
    catIds = coco.getCatIds(catNms=catNms); #get a list category ids for each category name 
    for n, cat_id in enumerate(catIds): ##for each category id
        print('in category id:,',cat_id)
        imgIds = coco.getImgIds(catIds = cat_id) #for each category id, get a list of img ids
        print(imgIds[:10]) #printing first 10 image ids
        pathlib.Path('val_orig/' + catNms[n]).mkdir(parents=True, exist_ok=True) #create a path to store training data for the current category
        coco.download(tarDir = 'val_orig/' + catNms[n], imgIds = imgIds[1500:2000]) #download first 500 image ids
    #     into the specified directory
        d = os.listdir('val_orig/' + catNms[n]) #create list of files in the created directory. This list has 500 
    #     jpg file names
    #     print('list of files in d', d)
        for img in d: #iterate through list of downloaded images. Resize them to 64 x 64. 
            try:
                    temp_img = Image.open('val_orig/' + catNms[n] + '/' + img) #open image
                    temp_img = temp_img.resize((64,64)) #resize
                    save_path = 'val/' + catNms[n] + '/' # Create the folder if it doesn't exist
                    os.makedirs(save_path, exist_ok=True)  # Create the folder if it doesn't exist
                    temp_img.save(fp = save_path + 'resized_' + img) #overwrite image with the 64 x 64 version
            except OSError:
                print(f'failed on {save_path, img}')
                ### save function parameters:
                #fp – A filename (string), pathlib.Path object or file object.
                #format – Optional format override. If omitted, the format to use is determined from the 
                ###filename extension.
                #If a file object was used instead of a filename, this parameter should always be used.

if __name__ == "__main__":
    coco = display_categories()
    if args.train:
        print('this is args.train', args.train)
        get_training_images()
    if args.val:
        print('this is args.val', args.val)
        get_validation_images()