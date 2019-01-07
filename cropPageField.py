#!/usr/bin/python
#
# execute this python file in the directory you locate target ZIPs (in labeling tool v3 format)
# it report the number of 1) a specified tag (in XMLs without extracting ZIPs)
#                         2) a specified tag with a given attribute (...)
#                         3) a specified tag with a given attribute without a given child tag (...)
#
# below is an example getting the number of each "name" of all "Page" without child "ITSFINE": 
#     $ python3 findElements.py Page name ITSFINE
#     $ python  findElements.py Page name ITSFINE
#
# below is an example getting the number of each "value" of all "MEMO"
#     $ python3 findElements.py MEMO value
#     $ python  findElements.py MEMO value
#

import os
import sys
import errno
import zipfile
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd
from PIL import Image

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

myColumns = ['Case', 'Tif', 'Frame', 'Page', 'Field', 'FieldX', 'FieldY', 'FieldW', 'FieldH']
df = pd.DataFrame(columns=myColumns)

myLabels = [ 
        'ACCOUNT_ID',
        'DATE',
        'MEMO',
        'DEPOSIT',
        'WITHDRAWAL',
        'BALANCE',
        'BANK _NAME',
        'BALANCE_0',
        'ATM_ID',
        'REMARKS',
        'PAGE',
        'ACCOUNT_HOLDER',
        'CURRENCY',
        'END',
        'EMPLOYEE',
        'ACCOUNT_1',
        'ACCOUNT_TYPE',
        'OTHERS',
        'ITSFINE',
        'CHAR'
        ]

mkdir_p("./pageImage/")
mkdir_p("./fieldImage/")

pageImageIndex=0
fieldImageIndex=0

for filename in os.listdir(sys.argv[1]):
    if filename.endswith(".zip"):
        filename = sys.argv[1] + filename
        #print("processing ZIP \"" + filename + "\"")
        with zipfile.ZipFile(filename, "r") as zip_file:
            for zipped_filename in zip_file.namelist():
                if zipped_filename.endswith("xml"):
                    #print(zipped_filename)
                    if re.match(r'.*XMLs\/\w+\/\w+\.xml', zipped_filename): #only match the Large labeling XMLs
                        print(zipped_filename, "in", filename)
                        tree = ET.fromstring(zip_file.read(zipped_filename))
                        for casetree in tree.iter("Case"):
                            case = casetree.get("name")
                            for tifftree in casetree.iter("Tif"):
                                tiff = tifftree.get("name")
                                for frametree in tifftree.iter("Frame"):
                                    frame = frametree.get("name")
                                    for pagetree in frametree.iter("Page"):
                                        page = pagetree.get("name")
                                        if page != "Default":
                                            pagebbox = list(map(int, pagetree.get("bbox").split()))
                                            pagebbox[2] = pagebbox[0] + pagebbox[2]
                                            pagebbox[3] = pagebbox[1] + pagebbox[3]
                                            #print(pagebbox)
                                            myRegex = re.escape(case) + r"/" + re.escape(tiff) + r"/" + re.escape(frame)
                                            for zipped_filename in zip_file.namelist():
                                                if re.match(myRegex, zipped_filename):
                                                    print(zipped_filename)
                                                    frameImage =  Image.open(zip_file.open(zipped_filename))
                                                    pageImage = frameImage.crop(pagebbox)
                                                    #pageImage.show()
                                                    pageImageName = "./pageImage/pageImage_" + str(pageImageIndex) + ".jpg"
                                                    pageImage.save(pageImageName)
                                                    pageImageIndex += 1
                                                    break
                                            for field in pagetree:
                                                fieldbbox = [field.get("lefttop_x"), field.get("lefttop_y"), field.get("width"), field.get("height")]
                                                fieldbbox = list(map(int, fieldbbox))
                                                fieldbbox[2] = fieldbbox[0] + fieldbbox[2]
                                                fieldbbox[3] = fieldbbox[1] + fieldbbox[3]
                                                #print(fieldbbox)
                                                fieldImage = frameImage.crop(fieldbbox)
                                                #fieldImage.show()
                                                fieldImageName = "./fieldImage/fieldImage_" + str(fieldImageIndex) + ".jpg"
                                                fieldImage.save(fieldImageName)
                                                fieldImageIndex += 1
                                                fieldbbox = [case, tiff, frame, page, field.tag, field.get("lefttop_x"), field.get("lefttop_y"), field.get("width"), field.get("height")]
                                                df = df.append(pd.Series(fieldbbox, index=myColumns), ignore_index=True) 
                                            frameImage.close()



#print(df)
excel = "Field.xlsx"
df.to_excel(excel)
print('Write to file', excel)
