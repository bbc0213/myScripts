#coding:utf-8

import xmltodict
import json
import os
import time
import glob
import sys
from os import listdir
from os.path import isdir , join , isfile
from collections import OrderedDict

start = time.time()


mypath = str(sys.argv[1])




index = 1

files = listdir(mypath)





for f in files:
    fullpath = join(mypath,f)

    if isdir(fullpath):
        
        

        targetPattern = fullpath + "/*.dml"



        globtemp = glob.glob(targetPattern)

        
        

        array = []

        temparray=[]

        delarray=[]

        

        timeloop = 0

        Acct = ''

        covercount = 0

        for i in range(len(globtemp)):
            with open(globtemp[i], 'r' , encoding='UTF-8') as fd:
                doc = xmltodict.parse(fd.read())
                if(doc.__contains__('Doc')==True):
                    if((doc['Doc']['@type'])[0] == 'B'):
                        covercount = covercount + 1



        for i in range(covercount):
            Loop = True
            while(Loop == True):
                with open(globtemp[timeloop], 'r' , encoding='UTF-8') as fd:
                    doc = xmltodict.parse(fd.read())

                    if(doc.__contains__('Doc')==True):
                        if((doc['Doc']['@type'])[0] == 'B'):

                            with open('./xml/trace.xml','r',encoding='UTF-8') as fd1:
                                doc1 = xmltodict.parse(fd1.read())
                            
                            if(len(globtemp) == 1 and doc['Doc']['Acct']['@interpretation'] == doc1['Apply_Case']['Aux_Info']['Remit_Acct']['@Acct']):
                                doc['Doc'].update({'@CHK_Remit':'true'})
                            else:
                                doc['Doc'].update({'@CHK_Remit':'false'})

                            loc = doc['Doc']['@LOC']
                            Conf = []

                            for key , value in doc['Doc'].items():
                                if(key[0] != '@'):
                                    if(doc['Doc'][key]['@Conf'] != ''):
                                        Conf.append(float(doc['Doc'][key]['@Conf']))
                                    doc['Doc'][key].update({'@LOC':loc})

                            if(Conf != []):
                                doc['Doc'].update({'@Conf':min(Conf)})
                            else:
                                doc['Doc'].update({'@Conf':''})


                            xmlstr = xmltodict.unparse(doc , pretty=True)
                            myfile = open(globtemp[timeloop],"w",encoding="utf-8")
                            myfile.write(xmlstr)
                            fd.close()
                            fd1.close()
                            myfile.close()

                            array.append(globtemp[timeloop])

                            for key , value in doc['Doc'].items():
                                if(key == 'Acct'):
                                    Acct = doc['Doc']['Acct']['@interpretation']

                            del globtemp[timeloop]
                            Loop = False
                            timeloop = 0
                            
                        else:
                            timeloop = timeloop +1
                    if(timeloop == len(globtemp)):
                        Loop = False

        #print(targetPattern)
        #print(array)             

        compare = len(globtemp)



        for i in range(len(globtemp)):
            with open(globtemp[i], 'r' , encoding='UTF-8') as fd:
                #print(globtemp[i])

                count = 0
                lencount = 0
                realcount = 0
                doc = xmltodict.parse(fd.read())
                totalConf = []
                Conf = []
                Loop = True
                if(doc.__contains__('Doc')==True):
                    if((doc['Doc']['@type'])[0] == 'b'):
                        loc = doc['Doc']['@LOC']
                        doc['Doc'].update({'@CHK_Acct':Acct})
                        for k , v in doc['Doc'].items():

                            if (k[0] != '@' and k != 'Transaction_Row'):
                                doc['Doc'][k].update({'@LOC':loc})
                            
                            elif( k == 'Transaction_Row'):

                                if(type(doc['Doc']['Transaction_Row']) != list):
                                    for key , value in doc['Doc']['Transaction_Row'].items():
                                        if(key == 'Date'):
                                            if(doc['Doc']['Transaction_Row']['Date']['@interpretation'] != ''):
                                                try:
                                                    s1_time = time.mktime(time.strptime((doc['Doc']['Transaction_Row']['Date']['@interpretation']),'%Y-%m-%d'))
                                                    temparray.append(s1_time)
                                                    delarray.append(s1_time)
                                                    count = count + 1
                                                except:
                                                    print('wrong date')
                                                
                                    if(count == 0):
                                        s1_time = time.mktime(time.strptime('2000-01-01','%Y-%m-%d'))
                                        temparray.append(s1_time)
                                        delarray.append(s1_time)
                                    for key , value in doc['Doc']['Transaction_Row'].items():
                                        if(key[0] != '@'):                                 
                                            if(doc['Doc']['Transaction_Row'][key]['@Conf'] != ''):
                                                Conf.append(float(doc['Doc']['Transaction_Row'][key]['@Conf']))
                                            doc['Doc']['Transaction_Row'][key].update({'@LOC':loc})


                                    if(Conf != []):
                                        doc['Doc']['Transaction_Row'].update({'@Conf':min(Conf)})
                                    else:
                                        doc['Doc']['Transaction_Row'].update({'@Conf':''})
                                    
                                    doc['Doc']['Transaction_Row'].update({'@LOC':loc})
                                    for key , value in doc['Doc'].items():
                                        if (key[0] != '@'):
                                            if(doc['Doc'][key]['@Conf'] != ''):
                                                totalConf.append(float(doc['Doc'][key]['@Conf']))
                                else:
                                    
                                    while(Loop == True):
                                        if(lencount == len(doc['Doc']['Transaction_Row'])):
                                            s1_time = time.mktime(time.strptime('2000-01-01','%Y-%m-%d'))
                                            temparray.append(s1_time)
                                            delarray.append(s1_time)
                                            Loop = False
                                        else:
                                            for key , value in doc['Doc']['Transaction_Row'][lencount].items():
                                                if(key == 'Date'):
                                                    
                                                    if(doc['Doc']['Transaction_Row'][realcount]['Date']['@interpretation'] != ''):
                                                        try:
                                                            s1_time = time.mktime(time.strptime((doc['Doc']['Transaction_Row'][realcount]['Date']['@interpretation']),'%Y-%m-%d'))
                                                            temparray.append(s1_time)
                                                            delarray.append(s1_time)
                                                            Loop = False
                                                        except:
                                                            print('wrong date')

                                    
                                        lencount = lencount + 1
                                        realcount = realcount +1

                                        
                                        
                                            
                                    for j in range(len(doc['Doc']['Transaction_Row'])):
                                        doc['Doc']['Transaction_Row'][j].update({'@type':''})
                                        for key , value in doc['Doc']['Transaction_Row'][j].items():
                                            if(key[0] != '@' and key != 'Aux_Info'):
                                                if(doc['Doc']['Transaction_Row'][j][key]['@Conf'] != ''):
                                                    Conf.append(float(doc['Doc']['Transaction_Row'][j][key]['@Conf']))
                                                doc['Doc']['Transaction_Row'][j][key].update({'@LOC':loc})


                                            if j > 0:
                                                
                                                for key1 , value1 in doc['Doc']['Transaction_Row'][j-1].items():
                                                    if(key == 'Balance' and key1 == 'Balance'):
                                                        if(doc['Doc']['Transaction_Row'][j]['Balance']['@interpretation'] != '' and doc['Doc']['Transaction_Row'][j-1]['Balance']['@interpretation'] != ''):
                                                            if(int(float(doc['Doc']['Transaction_Row'][j]['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row'][j-1]['Balance']['@interpretation']))) > 0:
                                                                doc['Doc']['Transaction_Row'][j].update({'@type':'Inc.'})
                                                                
                                                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd1:
                                                                    doc1 = xmltodict.parse(fd1.read())
                                                                    doc['Doc']['Transaction_Row'][j].update({'Aux_Info':doc1['Apply_Case']['Aux_Info']})
                                                            elif(int(float(doc['Doc']['Transaction_Row'][j]['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row'][j-1]['Balance']['@interpretation']))) == 0:
                                                                if(doc['Doc']['Transaction_Row'][j]['Deposit']['@interpretation'] == 0):
                                                                    doc['Doc']['Transaction_Row'][j].update({'@type':'Inc.'})
                                                                    with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd1:
                                                                        doc1 = xmltodict.parse(fd1.read())
                                                                        doc['Doc']['Transaction_Row'][j].update({'Aux_Info':doc1['Apply_Case']['Aux_Info']})
                                                                else:
                                                                    doc['Doc']['Transaction_Row'][j].update({'@type':'Dec.'})
                                                            
                                                            else:
                                                                doc['Doc']['Transaction_Row'][j].update({'@type':'Dec.'})
                                                        else:
                                                            doc['Doc']['Transaction_Row'][j].update({'@type':''})

                                                        
                                        if(Conf != []):
                                            doc['Doc']['Transaction_Row'][j].update({'@Conf':min(Conf)})
                                        else:
                                            doc['Doc']['Transaction_Row'][j].update({'@Conf':''})

                                        doc['Doc']['Transaction_Row'][j].update({'@LOC':loc})

                                        
                                    
                                    for k in range(len(doc['Doc']['Transaction_Row'])):
                                        if(doc['Doc']['Transaction_Row'][k]['@Conf'] != ''):
                                            totalConf.append(float(doc['Doc']['Transaction_Row'][k]['@Conf']))
                            
                            for key , value in doc['Doc'].items():
                                if (key[0] != '@' and key != 'Transaction_Row' and doc['Doc'][key]['@Conf'] != ''):
                                    totalConf.append(float(doc['Doc'][key]['@Conf']))
                        
                        if(totalConf != []):
                            doc['Doc'].update({'@Conf':min(totalConf)})
                        else:
                            doc['Doc'].update({'@Conf':''})
                        with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd1:
                            doc1 = xmltodict.parse(fd1.read())
                            doc['Doc'].update({'Aux_Info':doc1['Apply_Case']['Aux_Info']})
                        xmlstr = xmltodict.unparse(doc , pretty=True)
                        myfile = open(globtemp[i],"w",encoding="utf-8")
                        myfile.write(xmlstr)
                        fd.close()
                        fd1.close()
                        myfile.close()




        for i in range(compare):
            Loop = True
            if(len(delarray) !=0 and len(temparray) != 0):
                #print(temparray)
                #print(delarray)
                
                for j in range(len(temparray)):
                    while(Loop == True):
                        #print(j)
                        if(len(delarray) !=0 and temparray[j] == min(delarray)):
                            #print(temparray[j])
                            #print(min(delarray))
                            #print('here')
                            array.append(globtemp[j])
                            del globtemp[j]
                            del temparray[j]
                            Loop = False
                        if(len(delarray) ==0):
                            Loop = False
                        else:
                            j=j+1
                
                delarray.remove(min(delarray))
            
            
        




        #print(array[0].split('/')[-1])



        i=0
        j=0
        k=-1
        with open(array[0] , 'r' , encoding='UTF-8') as fd:
            doc1 = xmltodict.parse(fd.read())
            if(doc1.__contains__('Doc')==True):
                FC_type = doc1["Doc"]["@type"]
                fd.close
            if((doc1['Doc']['@type'])[0] == 'b'):
                j=1


        for xml_f in array:
            with open(xml_f, 'r' , encoding='UTF-8') as fd:
                doc1 = xmltodict.parse(fd.read())
                if((doc1['Doc']['@type'])[0] == 'B'):
                    doc1["Doc"].update({"@index":i})
                    xmlstr = xmltodict.unparse(doc1 , pretty=True)
                    myfile = open(xml_f,"w",encoding="utf-8")
                    myfile.write(xmlstr)
                    fd.close()
                    myfile.close()
                    k=0
                if((doc1['Doc']['@type'])[0] == 'b'): 
                    doc1["Doc"].update({"@index":j})
                    xmlstr = xmltodict.unparse(doc1 , pretty=True)
                    myfile = open(xml_f,"w",encoding="utf-8")
                    myfile.write(xmlstr)
                    fd.close()
                    myfile.close()


                CHK_Date = '2000-01-01'
                CHK_Balance_0 = '0'

                

                if(k==0 and len(array) > 1 and covercount != len(array)):
                    with open(array[i+1] , 'r' , encoding='UTF-8') as fd1:
                        doc = xmltodict.parse(fd1.read())
                        if((doc['Doc']['@type'])[0] == 'b'):
                            doc['Doc'].update({'@CHK_Date':'2000-01-01' , '@CHK_Balance_0': '0'})
                        xmlstr = xmltodict.unparse(doc , pretty=True)
                        myfile = open(array[i+1],"w",encoding="utf-8")
                        myfile.write(xmlstr)
                        fd1.close()
                        myfile.close()
                        k=k+1

                if(j==1):
                    with open(array[0] , 'r' , encoding='UTF-8') as fd1:
                        doc = xmltodict.parse(fd1.read())
                        if((doc['Doc']['@type'])[0] == 'b'):
                            doc['Doc'].update({'@CHK_Date':'2000-01-01' , '@CHK_Balance_0': '0'})
                        xmlstr = xmltodict.unparse(doc , pretty=True)
                        myfile = open(array[0],"w",encoding="utf-8")
                        myfile.write(xmlstr)
                        fd1.close()
                        myfile.close()

                if(len(array)-1 > i):
                    
                    if((doc1['Doc']['@type'])[0] == 'b'):
                        if(type(doc1['Doc']['Transaction_Row']) != list):
                            for key , value in doc1['Doc']['Transaction_Row'].items():
                                if(key == 'Date'):
                                    CHK_Date = doc1['Doc']['Transaction_Row']['Date']['@interpretation']
                                elif(key == 'Balance'):
                                    CHK_Balance_0 = doc1['Doc']['Transaction_Row']['Balance']['@interpretation']
                        else:
                            for key , value in doc1['Doc']['Transaction_Row'][len(doc1['Doc']['Transaction_Row'])-1].items():
                                if(key == 'Date'):
                                    CHK_Date = doc1['Doc']['Transaction_Row'][len(doc1['Doc']['Transaction_Row'])-1]['Date']['@interpretation']
                                elif(key == 'Balance'):
                                    CHK_Balance_0 = doc1['Doc']['Transaction_Row'][len(doc1['Doc']['Transaction_Row'])-1]['Balance']['@interpretation']
                        with open(array[i+1] , 'r' , encoding='UTF-8') as fd1:
                            doc = xmltodict.parse(fd1.read())
                            doc['Doc'].update({'@CHK_Date':CHK_Date , '@CHK_Balance_0':CHK_Balance_0})
                            xmlstr = xmltodict.unparse(doc , pretty=True)
                            myfile = open(array[i+1],"w",encoding="utf-8")
                            myfile.write(xmlstr)
                            fd1.close()
                            myfile.close()

            i = i+1
            j = j+1

        

        for i in range(len(array)):
            if(i==covercount):
                with open(array[i] , 'r' , encoding='UTF-8') as fd:
                    doc = xmltodict.parse(fd.read())
                if(type(doc['Doc']['Transaction_Row']) != list):
                    doc['Doc']['Transaction_Row'].update({'@type':''})
                    for key , value in doc['Doc']['Transaction_Row'].items():
                        if(key == 'Deposit'):
                            if(doc['Doc']['Transaction_Row']['Deposit']['@interpretation'].isdecimal() == True):
                                doc['Doc']['Transaction_Row'].update({'@type':'Inc.'})
                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                    doc2 = xmltodict.parse(fd2.read())
                                    doc['Doc']['Transaction_Row'].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                fd2.close()
                            else:
                                doc['Doc']['Transaction_Row'].update({'@type':'Dec.'})
                else:
                    doc['Doc']['Transaction_Row'][0].update({'@type':''})
                    for key , value in doc['Doc']['Transaction_Row'][0].items():
                        if(key == 'Deposit'):
                            if(doc['Doc']['Transaction_Row'][0]['Deposit']['@interpretation'].isdecimal() == True):
                                doc['Doc']['Transaction_Row'][0].update({'@type':'Inc.'})
                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                    doc2 = xmltodict.parse(fd2.read())
                                    doc['Doc']['Transaction_Row'][0].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                fd2.close()
                            else:
                                doc['Doc']['Transaction_Row'][0].update({'@type':'Dec.'})
                
                xmlstr = xmltodict.unparse(doc , pretty=True)
                myfile = open(array[i],"w",encoding="utf-8")
                myfile.write(xmlstr)
                myfile.close()
                fd.close()
            elif(i>covercount):
                with open(array[i-1] , 'r' , encoding='UTF-8') as fd:
                    doc = xmltodict.parse(fd.read())
                with open(array[i] , 'r' , encoding='UTF-8') as fd1:
                    doc1 = xmltodict.parse(fd1.read())
                
                if(type(doc1['Doc']['Transaction_Row']) != list):
                    if(type(doc['Doc']['Transaction_Row']) == list):
                        doc1['Doc']['Transaction_Row'].update({'@type':''})
                        for key , value in doc1['Doc']['Transaction_Row'].items():
                            for key1 , value1 in doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1].items():
                                if( key == 'Balance' and key1 == 'Balance'):
                                    if(doc1['Doc']['Transaction_Row']['Balance']['@interpretation'] != '' and doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1]['Balance']['@interpretation'] != '' ):
                                        if(int(float(doc1['Doc']['Transaction_Row']['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1]['Balance']['@interpretation']))) > 0:
                                            doc1['Doc']['Transaction_Row'].update({'@type':'Inc.'})
                                            with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                doc2 = xmltodict.parse(fd2.read())
                                                doc1['Doc']['Transaction_Row'].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                            fd2.close()
                                        elif(int(float(doc1['Doc']['Transaction_Row']['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1]['Balance']['@interpretation']))) == 0:
                                            if(int(float(doc1['Doc']['Transaction_Row']['Deposit']['@interpretation'])) == 0):
                                                doc1['Doc']['Transaction_Row'].update({'@type':'Inc.'})
                                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                    doc2 = xmltodict.parse(fd2.read())
                                                    doc1['Doc']['Transaction_Row'].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                                fd2.close()
                                            else:
                                                doc1['Doc']['Transaction_Row'].update({'@type':'Dec.'})
                                        else:
                                            doc1['Doc']['Transaction_Row'].update({'@type':'Dec.'})
                                    else:
                                        doc1['Doc']['Transaction_Row'].update({'@type':''})
                    else:
                        doc1['Doc']['Transaction_Row'].update({'@type':''})
                        for key , value in doc1['Doc']['Transaction_Row'].items():
                            for key1 , value1 in doc['Doc']['Transaction_Row'].items():
                                if( key == 'Balance' and key1 == 'Balance'):
                                    if(doc1['Doc']['Transaction_Row']['Balance']['@interpretation'] != '' and doc['Doc']['Transaction_Row']['Balance']['@interpretation'] != '' ):
                                        if(int(float(doc1['Doc']['Transaction_Row']['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row']['Balance']['@interpretation']))) > 0:
                                            doc1['Doc']['Transaction_Row'].update({'@type':'Inc.'})
                                            with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                doc2 = xmltodict.parse(fd2.read())
                                                doc1['Doc']['Transaction_Row'].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                            fd2.close()
                                        elif(int(float(doc1['Doc']['Transaction_Row']['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row']['Balance']['@interpretation']))) == 0:
                                            if(int(float(doc1['Doc']['Transaction_Row']['Deposit']['@interpretation'])) == 0):
                                                doc1['Doc']['Transaction_Row'].update({'@type':'Inc.'})
                                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                    doc2 = xmltodict.parse(fd2.read())
                                                    doc1['Doc']['Transaction_Row'].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                                fd2.close()
                                            else:
                                                doc1['Doc']['Transaction_Row'].update({'@type':'Dec.'})
                                        else:
                                            doc1['Doc']['Transaction_Row'].update({'@type':'Dec.'})
                                    else:
                                        doc1['Doc']['Transaction_Row'].update({'@type':''})

                else:
                    if(type(doc['Doc']['Transaction_Row']) == list):
                        doc1['Doc']['Transaction_Row'][0].update({'@type':''})
                        for key , value in doc1['Doc']['Transaction_Row'][0].items():
                            for key1 , value1 in doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1].items():
                                if( key == 'Balance' and key1 == 'Balance'):
                                    if(doc1['Doc']['Transaction_Row'][0]['Balance']['@interpretation'] != '' and doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1]['Balance']['@interpretation'] != ''):
                                        if(int(float(doc1['Doc']['Transaction_Row'][0]['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1]['Balance']['@interpretation']))) > 0:
                                            doc1['Doc']['Transaction_Row'][0].update({'@type':'Inc.'})
                                            with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                doc2 = xmltodict.parse(fd2.read())
                                                doc1['Doc']['Transaction_Row'][0].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                            fd2.close()
                                        elif(int(float(doc1['Doc']['Transaction_Row'][0]['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row'][len(doc['Doc']['Transaction_Row'])-1]['Balance']['@interpretation']))) == 0:
                                            if(int(float(doc1['Doc']['Transaction_Row'][0]['Deposit']['@interpretation'])) == 0):
                                                doc1['Doc']['Transaction_Row'][0].update({'@type':'Inc.'})
                                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                    doc2 = xmltodict.parse(fd2.read())
                                                    doc1['Doc']['Transaction_Row'][0].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                                fd2.close()
                                            else:
                                                doc1['Doc']['Transaction_Row'][0].update({'@type':'Dec.'})
                                        else:
                                            doc1['Doc']['Transaction_Row'][0].update({'@type':'Dec.'})
                                    else:
                                        doc1['Doc']['Transaction_Row'][0].update({'@type':''})
                    else:
                        doc1['Doc']['Transaction_Row'][0].update({'@type':''})
                        for key , value in doc1['Doc']['Transaction_Row'][0].items():
                            for key1 , value1 in doc['Doc']['Transaction_Row'].items():
                                if( key == 'Balance' and key1 == 'Balance'):
                                    if(doc1['Doc']['Transaction_Row'][0]['Balance']['@interpretation'] != '' and doc['Doc']['Transaction_Row']['Balance']['@interpretation'] != ''):
                                        if(int(float(doc1['Doc']['Transaction_Row'][0]['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row']['Balance']['@interpretation']))) > 0:
                                            doc1['Doc']['Transaction_Row'][0].update({'@type':'Inc.'})
                                            with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                doc2 = xmltodict.parse(fd2.read())
                                                doc1['Doc']['Transaction_Row'][0].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                            fd2.close()
                                        elif(int(float(doc1['Doc']['Transaction_Row'][0]['Balance']['@interpretation'])) - int(float(doc['Doc']['Transaction_Row']['Balance']['@interpretation']))) == 0:
                                            if(int(float(doc1['Doc']['Transaction_Row'][0]['Deposit']['@interpretation'])) == 0):
                                                doc1['Doc']['Transaction_Row'][0].update({'@type':'Inc.'})
                                                with open('./xml/doc.cml' , 'r' , encoding='UTF-8') as fd2:
                                                    doc2 = xmltodict.parse(fd2.read())
                                                    doc1['Doc']['Transaction_Row'][0].update({'Aux_Info':doc2['Apply_Case']['Aux_Info']})
                                                fd2.close()
                                            else:
                                                doc1['Doc']['Transaction_Row'][0].update({'@type':'Dec.'})
                                        else:
                                            doc1['Doc']['Transaction_Row'][0].update({'@type':'Dec.'})
                                    else:
                                        doc1['Doc']['Transaction_Row'][0].update({'@type':''})


                xmlstr = xmltodict.unparse(doc1 , pretty=True)
                myfile = open(array[i],"w",encoding="utf-8")
                myfile.write(xmlstr)
                myfile.close()
                fd.close()
                fd1.close()
            
            





        total = 0


        for i in range(len(array)):
            Rec_Amt=0
            if(i>(covercount-1)):
                with open(array[i], 'r' , encoding='UTF-8') as fd:
                    doc = xmltodict.parse(fd.read())
                    with open('./xml/Salary_Memo_KW.xml' , 'r' , encoding='UTF-8') as fd1:
                        doc1 = xmltodict.parse(fd1.read())

                        if(type(doc['Doc']['Transaction_Row']) != list):
                            doc['Doc']['Transaction_Row'].update({'@Rec_able':'false'})
                            doc['Doc']['Transaction_Row'].update({'@Rec_Amt':0})
                            doc['Doc']['Transaction_Row'].update({'@Rec_Type':''})
                            for k in range(len(doc1['Aux_Info']['Salary_Memo_KW']['KW'])):
                                for key , value in doc['Doc']['Transaction_Row'].items():
                                    for key1 , value1 in doc['Doc']['Transaction_Row'].items():
                                        if( key == 'Memo' and key1 == '@type'):
                                            if(type(doc1['Aux_Info']['Salary_Memo_KW']['KW']) == list):
                                                if(doc['Doc']['Transaction_Row']['Memo']['@interpretation'] == doc1['Aux_Info']['Salary_Memo_KW']['KW'][k]['#text'] and doc['Doc']['Transaction_Row']['@type'] == 'Inc.'):
                                                    doc['Doc']['Transaction_Row'].update({'@Rec_able':'true'})
                                                    doc['Doc']['Transaction_Row'].update({'@Rec_Amt':doc['Doc']['Transaction_Row']['Deposit']['@interpretation']})
                                                    doc['Doc']['Transaction_Row'].update({'@Rec_Type':doc1['Aux_Info']['Salary_Memo_KW']['KW'][k]['@Rec_Type']})
                                                    Rec_Amt = Rec_Amt + int(float(doc['Doc']['Transaction_Row']['Deposit']['@interpretation']))
                                            else:
                                                if(doc['Doc']['Transaction_Row']['Memo']['@interpretation'] == doc1['Aux_Info']['Salary_Memo_KW']['KW']['#text'] and doc['Doc']['Transaction_Row']['@type'] == 'Inc.'):
                                                    doc['Doc']['Transaction_Row'].update({'@Rec_able':'true'})
                                                    doc['Doc']['Transaction_Row'].update({'@Rec_Amt':doc['Doc']['Transaction_Row']['Deposit']['@interpretation']})
                                                    doc['Doc']['Transaction_Row'].update({'@Rec_Type':doc1['Aux_Info']['Salary_Memo_KW']['KW']['@Rec_Type']})
                                                    Rec_Amt = Rec_Amt + int(float(doc['Doc']['Transaction_Row']['Deposit']['@interpretation']))
                        else:
                            for j in range(len(doc['Doc']['Transaction_Row'])):
                                doc['Doc']['Transaction_Row'][j].update({'@Rec_able':'false'})
                                doc['Doc']['Transaction_Row'][j].update({'@Rec_Amt':0})
                                doc['Doc']['Transaction_Row'][j].update({'@Rec_Type':''})
                                for k in range(len(doc1['Aux_Info']['Salary_Memo_KW']['KW'])):
                                    for key , value in doc['Doc']['Transaction_Row'][j].items():
                                        for key1 , value1 in doc['Doc']['Transaction_Row'][j].items():
                                            if( key == 'Memo' and key1 == '@type'):
                                                if(type(doc1['Aux_Info']['Salary_Memo_KW']['KW']) == list):
                                                    if(doc['Doc']['Transaction_Row'][j]['Memo']['@interpretation'] == doc1['Aux_Info']['Salary_Memo_KW']['KW'][k]['#text'] and doc['Doc']['Transaction_Row'][j]['@type'] == 'Inc.'):
                                                        doc['Doc']['Transaction_Row'][j].update({'@Rec_able':'true'})
                                                        doc['Doc']['Transaction_Row'][j].update({'@Rec_Amt':doc['Doc']['Transaction_Row'][j]['Deposit']['@interpretation']})
                                                        doc['Doc']['Transaction_Row'][j].update({'@Rec_Type':doc1['Aux_Info']['Salary_Memo_KW']['KW'][k]['@Rec_Type']})
                                                        Rec_Amt = Rec_Amt + int(float(doc['Doc']['Transaction_Row'][j]['Deposit']['@interpretation']))
                                                else:
                                                    if(doc['Doc']['Transaction_Row'][j]['Memo']['@interpretation'] == doc1['Aux_Info']['Salary_Memo_KW']['KW']['#text'] and doc['Doc']['Transaction_Row'][j]['@type'] == 'Inc.'):
                                                        doc['Doc']['Transaction_Row'][j].update({'@Rec_able':'true'})
                                                        doc['Doc']['Transaction_Row'][j].update({'@Rec_Amt':doc['Doc']['Transaction_Row'][j]['Deposit']['@interpretation']})
                                                        doc['Doc']['Transaction_Row'][j].update({'@Rec_Type':doc1['Aux_Info']['Salary_Memo_KW']['KW']['@Rec_Type']})
                                                        Rec_Amt = Rec_Amt + int(float(doc['Doc']['Transaction_Row'][j]['Deposit']['@interpretation']))

                                    
 


                        fd1.close()
                    
                    doc['Doc'].update({"@Rec_Amt":Rec_Amt})
                    xmlstr = xmltodict.unparse(doc , pretty=True)
                    myfile = open(array[i],"w",encoding="utf-8")
                    myfile.write(xmlstr)
                    myfile.close()           
                    fd.close()

                total = total + Rec_Amt




        tempConf = []

        


        for xml_f in array:
            with open(xml_f, 'r' , encoding='UTF-8') as fd:
                doc = xmltodict.parse(fd.read())
                if(doc['Doc']['@Conf'] != ''):
                    tempConf.append(float(doc['Doc']['@Conf']))
    






        k=0


        combinearray=[]

        for xml_f in array:
            with open(xml_f, 'r' , encoding='UTF-8') as fd:
                doc1 = xmltodict.parse(fd.read())
                if(doc1.__contains__('Doc')==True):
                    if((doc1['Doc']['@type'])[0] == 'B'):
                        doc1.update( Cover = doc1.pop('Doc'))

                    elif((doc1['Doc']['@type'])[0] == 'b'):
                        doc1.update( Page = doc1.pop('Doc'))
                    temp = 'temp' + str(k) + '.dml'
                    combinearray.append(temp)
                    xmlstr = xmltodict.unparse(doc1 , pretty=True)
                    myfile = open(temp,"w",encoding="utf-8")
                    myfile.write(xmlstr)
                    fd.close()
                    myfile.close()
                    k=k+1


        with open('./xml/trace.xml' , 'r' , encoding='UTF-8') as fd:
            doc = xmltodict.parse(fd.read())
            for i in range(covercount):
                with open(combinearray[i] , 'r' , encoding='UTF-8') as fd1:
                    doc1 = xmltodict.parse(fd1.read())

                    if(doc1.__contains__('Cover')== True):

                        doc1['Cover'].update({"@CHK_Name":doc['Apply_Case']['Aux_Info']['Customer']['@Name']})
                        doc1['Cover'].update({"@CHK_Bank_Code":doc['Apply_Case']['Aux_Info']['Remit_Acct']['@Bank_Code']})
                        doc1['Cover'].update({"@CHK_Acct_Holder":doc['Apply_Case']['Aux_Info']['Remit_Acct']['@Acct_Holder']})
                        doc1['Cover'].update({"@CHK_Acct":doc['Apply_Case']['Aux_Info']['Remit_Acct']['@Acct']})

                        xmlstr = xmltodict.unparse(doc1 , pretty=True)
                        myfile = open(combinearray[i],"w",encoding="utf-8")
                        myfile.write(xmlstr)
                        fd.close()
                        fd1.close()
                        myfile.close()


        






       
        
        if(tempConf != []):
            Root = OrderedDict([("Finance_Cert",OrderedDict([("@index",index),("@type",FC_type),("@Rec_Amt",total),("@Conf",min(tempConf)),("Cover",[]),("Page",[])]))])
        else:
            Root = OrderedDict([("Finance_Cert",OrderedDict([("@index",index),("@type",FC_type),("@Rec_Amt",total),("@Conf",''),("Cover",[]),("Page",[])]))])

        Root1 = OrderedDict({"Remit_Acct":OrderedDict({"Cover":[]})})

        


        fd.close()

        j=0



        for xml_f in combinearray:
            with open(xml_f, 'r' , encoding='UTF-8') as fd:
                doc1 = xmltodict.parse(fd.read())                                
            if(j<covercount):
                if(doc1.__contains__('Cover')== True):
                    if(doc1['Cover']['@CHK_Remit'] == 'true'):
                        Root1['Remit_Acct']['Cover'].append(doc1['Cover'])
                        xmlstr = xmltodict.unparse(Root1 , pretty=True)
                        save_path = fullpath
                        completeName = os.path.join(save_path,"doc1.cml")
                        myfile = open(completeName,"w",encoding="utf-8")
                        myfile.write(xmlstr)
                        fd.close()
                        myfile.close()
                    else:
                        Root["Finance_Cert"]["Cover"].append(doc1["Cover"])
                        j=j+1
                else:
                    Root["Finance_Cert"]["Page"].append(doc1["Page"])
                    j=j+1
            else:
                Root["Finance_Cert"]["Page"].append(doc1["Page"])
                j=j+1

        



        if(j>=covercount):
            xmlstr = xmltodict.unparse(Root , pretty=True)

            save_path = fullpath
            completeName = os.path.join(save_path,"doc1.cml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(xmlstr)

            fd.close()
            myfile.close()

            index = index + 1


end = time.time()

elapsed = end - start
print("Time taken: ", elapsed, "seconds.")