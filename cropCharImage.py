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
from PIL import Image
#import xml.etree.ElementTree as ET
#from xml.dom import minidom
from lxml import etree as ET

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

mkdir_p("./pageImage/")
mkdir_p("./fieldImage/")
mkdir_p("./charImage/")

pageImageIndex=0
fieldImageIndex=0
charImageIndex=0

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
                        xmltree1 = ET.ElementTree(tree)
                        xmltree1.write('xmltree1.xml')
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
                                            for char in pagetree:
                                                if char.tag == "CHAR":
                                                    charbbox = [char.get("lefttop_x"), char.get("lefttop_y"), char.get("width"), char.get("height")]
                                                    charbbox = list(map(int, charbbox))
                                                    for field in pagetree:
                                                        fieldbbox = [field.get("lefttop_x"), field.get("lefttop_y"), field.get("width"), field.get("height")]
                                                        fieldbbox = list(map(int, fieldbbox))
                                                        fieldbbox[2] = fieldbbox[0] + fieldbbox[2]
                                                        fieldbbox[3] = fieldbbox[1] + fieldbbox[3]
                                                        #print(charbbox, fieldbbox)
                                                        if charbbox[0] >= fieldbbox[0] and charbbox[0] <= fieldbbox[2] and charbbox[1] >= fieldbbox[1] and charbbox[1] <= fieldbbox[3]:
                                                            #print(charbbox, fieldbbox)
                                                            field.append(char)
                                                            #pagetree.remove(char)
                                                            break
                                            for field in pagetree:
                                                if len(field.get('value')) == len(field.findall('CHAR')) and len(field.get('value')) != 0:
                                                    #print(field.tag, field.get('value').replace('\n',' ').replace('\r',''))
                                                    charList=[]
                                                    for char in field.findall('CHAR'):
                                                        charList.append([char.get('lefttop_x'),char.get('labelName')])
                                                    charList.sort()
                                                    for i in range(len(charList)):
                                                        for char in field.findall('CHAR'):
                                                            if char.get('labelName') == charList[i][1]:
                                                                char.attrib['value'] = field.get('value')[i]
                                                                charbbox = [char.get("lefttop_x"), char.get("lefttop_y"), char.get("width"), char.get("height")]
                                                                charbbox = list(map(int, charbbox))
                                                                charbbox[2] = charbbox[0] + charbbox[2]
                                                                charbbox[3] = charbbox[1] + charbbox[3]
                                                                #print(charbbox)
                                                                charImage = frameImage.crop(charbbox)
                                                                #charImage.show()
                                                                charImageName = "./charImage/charImage_" + str(charImageIndex) + "_" + char.get('value') + ".jpg"
                                                                charImage.save(charImageName)
                                                                charImageIndex += 1
                                            
                        xmltree2 = ET.ElementTree(tree)
                        xmltree2.write('xmltree2.xml',  pretty_print=True)

