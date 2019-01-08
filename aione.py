#coding:utf-8

from flask import Flask,request , render_template , jsonify , Response 
from xml.dom.minidom import parse
import xml.dom.minidom
import xmltodict
import json
import os
import gzip
import shutil
import requests
import base64
import subprocess
import errno
import glob
import zipfile
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymssql
from collections import OrderedDict
from os.path import isdir , join , isfile
from os import listdir
from os.path import basename
import sys


password = '1qaz@WSX'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  #顯示中文
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://aione_sa:'+ password +'@172.24.17.23:1803/aione_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

save_path = './xml'
root_path = './'
inter_path = os.path.abspath(os.path.dirname(__file__))

def process_management():
    with open('temp.json') as json_data:
        d = json.load(json_data)
        if(d.__contains__('traceId')==True):
            TraceId = d["traceId"]
        if(d.__contains__('receiveNo')==True):
            receiveNO = d["receiveNo"]
        if(d.__contains__('masterId')==True):
            masterId = d["masterId"]
        if(d.__contains__('docIds')==True):
            p8guid = d["docIds"]

    if os.path.exists('./JSONWRONG'):
        if os.path.exists('./exec/'+ TraceId):

            with zipfile.ZipFile('./exec/' + TraceId + '/' +  TraceId + '.zip', 'w',zipfile.ZIP_DEFLATED) as f:    
                f.write(os.path.join('./wrongjson.vml'))

            with open('./exec/' + TraceId + '/' + TraceId + '.zip','rb') as f1:
                file_base64 = f1.read()
                    
                base64_data = base64.b64encode(file_base64)

        else:
            with zipfile.ZipFile('./wrongjson.zip', 'w',zipfile.ZIP_DEFLATED) as f:    
                f.write(os.path.join('./wrongjson.vml'))

            with open('./wrongjson.zip','rb') as f1:
                file_base64 = f1.read()
                    
                base64_data = base64.b64encode(file_base64)
        
        os.rmdir('./JSONWRONG')


    elif os.path.exists('./filenetfaild'):
        
        

        with zipfile.ZipFile('./exec/' + TraceId + '/' +  TraceId + '.zip', 'w',zipfile.ZIP_DEFLATED) as f:
            f.write(os.path.join('./filenetwrong.vml'))

        with open('./exec/' + TraceId + '/' + TraceId + '.zip','rb') as f1:
            file_base64 = f1.read()
                
            base64_data = base64.b64encode(file_base64)
        os.rmdir('./filenetfaild')

    else:
        if(receiveNO == '00000000'):
            with zipfile.ZipFile('./exec/' + TraceId + '/' +  TraceId + '.zip', 'w',zipfile.ZIP_DEFLATED) as f:
                f.write(os.path.join('./01234567-89AB-CDEF-FEDC-BA9876543210.vml'))


            with open('./exec/' + TraceId + '/' +  TraceId + '.zip','rb') as f1:
                file_base64 = f1.read()
                
                base64_data = base64.b64encode(file_base64)


        elif(masterId == 'A188496736' or masterId == 'A105569461' or masterId == 'A152998894' or masterId == 'A195420653' or masterId == 'A161318840' or
            masterId == 'A123190295' or masterId == 'A170518643' or masterId == 'A102676736' or masterId == 'A195476459' or masterId == 'A136618097' or
            masterId == 'A117989759' or masterId == 'A170626604' or masterId == 'A177044299' or masterId == 'A107694056' or masterId == 'A178194412'):

            if(masterId == 'A188496736'):
                vmlTraceId = '201801027000101_01'
            if(masterId == 'A105569461'):
                vmlTraceId = '201801027000101_02'
            if(masterId == 'A195420653'):
                vmlTraceId = '201801027000101_03'
            if(masterId == 'A161318840'):
                vmlTraceId = '201801027000101_04'
            if(masterId == 'A123190295'):
                vmlTraceId = '201801027000101_05'
            if(masterId == 'A170518643'):
                vmlTraceId = '201801027000101_06'
            if(masterId == 'A102676736'):
                vmlTraceId = '201801027000101_07'
            if(masterId == 'A195476459'):
                vmlTraceId = '201801027000101_08'
            if(masterId == 'A136618097'):
                vmlTraceId = '201801027000101_09'
            if(masterId == 'A117989759'):
                vmlTraceId = '201801027000101_10'
            if(masterId == 'A170626604'):
                vmlTraceId = '201801027000101_11'
            if(masterId == 'A177044299'):
                vmlTraceId = '201801027000101_12'
            if(masterId == 'A107694056'):
                vmlTraceId = '201801027000101_13'
            if(masterId == 'A152998894'):
                vmlTraceId = '201801027000101_14'
            if(masterId == 'A178194412'):
                vmlTraceId = '20180101A000000_01'

            #print("./replace.pl ./exec/" + vmlTraceId + "/01234567-89AB-CDEF-FEDC-BA9876543210.vml " + receiveNO + " " + TraceId + " ./exec/" + vmlTraceId + "/01234567-89AB-CDEF-FEDC-BA9876543210.vml")
            subprocess.call("./replace.pl ./exec/" + vmlTraceId + "/01234567-89AB-CDEF-FEDC-BA9876543210.vml " + receiveNO + " " + TraceId + " ./exec/" + vmlTraceId + "/01234567-89AB-CDEF-FEDC-BA9876543210.vml" , shell= True)
            

            with zipfile.ZipFile('./exec/' + vmlTraceId + '/' +  vmlTraceId + '.zip', 'w',zipfile.ZIP_DEFLATED) as f:
                f.write(os.path.join('./exec/' + vmlTraceId + '/01234567-89AB-CDEF-FEDC-BA9876543210.vml'),basename(os.path.join('./exec/' + vmlTraceId + '/01234567-89AB-CDEF-FEDC-BA9876543210.vml')))


            with open('./exec/' + vmlTraceId + '/' +  vmlTraceId + '.zip','rb') as f1:
                file_base64 = f1.read()           
                base64_data = base64.b64encode(file_base64)


        else:

            with zipfile.ZipFile('./exec/' + TraceId + '/' +  TraceId + '.zip', 'w',zipfile.ZIP_DEFLATED) as f: 
                startdir = "./exec/" + TraceId 
                for dirpath, dirnames, filenames in os.walk(startdir): 
                    for filename in filenames:
                        if(filename.find(".vml") != -1): 
                            f.write(os.path.join(dirpath,filename), basename(os.path.join(dirpath,filename)))

            with open('./exec/' + TraceId + '/' +  TraceId + '.zip','rb') as f1:
                file_base64 = f1.read()
                
                base64_data = base64.b64encode(file_base64)


    str_base64_data = json.dumps(base64_data.decode())

    d.update({"xml":json.loads(str_base64_data)})

    
    r = requests.post('http://172.24.40.129:31887/MWS/services/RS/aione', json = d , headers = {'Content-tpye': 'application/json; charset=utf8'})




@app.route("/services/take_image", methods=["OPTIONS","POST"])
def take_image():

    if(request.method == 'OPTIONS'):
        headers = {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'POST , GET , OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers':'origin , x-csrftoken , content-type , accept',
        }

        return '' , 200 , headers

    else:
        data = request.get_data()
        jsondata = data.decode('utf-8').replace("'",'"')
        realjson = json.loads(jsondata)
        
        if(realjson.__contains__('receiveNo')==True and 
            realjson.__contains__('masterId')==True and 
            realjson.__contains__('masterName')==True and 
            realjson.__contains__('masterAddress')==True and 
            realjson.__contains__('companyName')==True and 
            realjson.__contains__('companyId')==True and 
            realjson.__contains__('companyAddress')==True and 
            realjson.__contains__('companyOwner')==True and
            realjson.__contains__('appropriationBankCode')==True and 
            realjson.__contains__('appropriationOwner')==True and 
            realjson.__contains__('appropriationAccount')==True and 
            realjson.__contains__('docIds')==True and
            realjson.__contains__('systemCode')==True and 
            realjson.__contains__('callbackService')==True and 
            realjson.__contains__('traceId')==True):

            

            receiveNo = realjson['receiveNo']
            masterId = realjson['masterId']
            masterName = realjson['masterName']
            masterAddress = realjson['masterAddress']
            companyName = realjson['companyName']
            companyId = realjson['companyId']
            companyAddress = realjson['companyAddress']
            companyOwner = realjson['companyOwner']
            appropriationBankCode = realjson['appropriationBankCode']
            appropriationOwner = realjson['appropriationOwner']
            appropriationAccount = realjson['appropriationAccount']
            docIds = realjson['docIds']
            systemCode = realjson['systemCode']
            callbackService = realjson['callbackService']
            traceId = realjson['traceId']
            
            

            xmljson = OrderedDict([('Apply_Case', OrderedDict([('@traceId', traceId), ('@Apply_Nbr', receiveNo), ('@version', 'v1.0'), ('Aux_Info', OrderedDict([('Customer', OrderedDict([('@Name', masterName), ('@ID', masterId), ('@Address', masterAddress)])), ('Company', OrderedDict([('@Name', companyName), ('@ID',companyId), ('@Address',companyAddress), ('@Owner',companyOwner)])), ('Remit_Acct', OrderedDict([('@Bank_Code',appropriationBankCode), ('@Acct_Holder', appropriationOwner), ('@Acct', appropriationAccount)]))]))]))])                                                                  


            tempjson = {"traceId":traceId,"receiveNo":receiveNo,"masterId":masterId,"mqSource":systemCode,"docIds":docIds,"token":'','mserviceFrom':'itri','mserviceTo':'pms','priority':''}

            

            xmlstr = xmltodict.unparse(xmljson , pretty=True)
            
            

            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise

            if not os.path.exists('./exec'):
                try:
                    os.makedirs('./exec')
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            
            

            completeName = os.path.join(save_path,"trace.xml")
            jsonfile = os.path.join(root_path,"temp.json")


            f = os.fork()



            if os.path.exists('./GPUBUSY'):
                resp = jsonify({"resCode":304 , "rspMsg":"GPU正在忙碌中"})
                resp.status_code = 304
                return resp
                  
            else:
                if(f == 0):
                    os.makedirs('./GPUBUSY')

                    myfile = open(completeName,"w",encoding="utf-8")
                    myfile.write(xmlstr)
                    myfile.close()

                    with open(jsonfile,'w',encoding='utf-8') as filejson:
                        json.dump(tempjson,filejson,ensure_ascii=False)
                        filejson.write
                    
                    if(receiveNo == '00000000'):
                        
                        print('end-to-end')


                    elif(masterId == 'A188496736' or masterId == 'A105569461' or masterId == 'A152998894' or masterId == 'A195420653' or masterId == 'A161318840' or
                    masterId == 'A123190295' or masterId == 'A170518643' or masterId == 'A102676736' or masterId == 'A195476459' or masterId == 'A136618097' or
                    masterId == 'A117989759' or masterId == 'A170626604' or masterId == 'A177044299' or masterId == 'A107694056' or masterId == 'A178194412'):
                        print('masterId end to end')


                    elif(traceId == '201801010060301_01'):
                        subprocess.call("./runDML2CML.sh " + traceId + " " + docIds,shell=True)

                        subprocess.call("python3 combinedoc.py ./exec/" + traceId + " " + docIds , shell = True)

                        subprocess.call("./runCML2VML.sh " + traceId + " " + docIds, shell = True)



                    else:
                        
                        if(docIds == ''):
                            p8guid = 'once'
                            subprocess.call("python3 ImageWebService_AIONE_keepTiff.py " + receiveNo + " " + p8guid + " " + traceId , shell = True)
                        else:
                            if(docIds.__contains__(',')):
                                arrayp8guid = docIds.split(',')
                                for i in range(len(arrayp8guid)):
                                    subprocess.call("python3 ImageWebService_AIONE_keepTiff.py " + receiveNo + " " + arrayp8guid[i] + " " + traceId , shell = True)
                            else:
                                p8guid = docIds
                                subprocess.call("python3 ImageWebService_AIONE_keepTiff.py " + receiveNo + " " + p8guid + " " + traceId , shell = True)

                        
                        
                        exitdir = './exec/'+ traceId

                        if(os.path.exists(exitdir)):

                            start_combine = open('./exec/'+ traceId +'/start_combine', 'w')
                            subprocess.call("python3 combine.py" , shell = True)

                            if(os.path.isdir(exitdir)):
                                files = listdir('./exec/' + traceId)           
                                for f in files:
                                    fullpath = join('./exec/'+traceId,f)
                                    
                                    if isdir(fullpath):
                                        
                                        p8guid = f
                                        

                                        start_inference = open('./exec/'+ traceId +'/start_inference', 'w')
                                        
                                        subprocess.call("CUDA_VISIBLE_DEVICES='' python3 ./integration/slim/inference_three.py -abs_path " + inter_path + "/integration/slim/ -s1_in " + "./exec/" + traceId + "/" + p8guid +"/" , shell = True)
                                        
                                        start_ctbc_ocr = open('./exec/'+ traceId +'/start_ctbc_ocr', 'w')

                                        #print("./integration/ctbc_ocr " + "exec/" + traceId + "/" + p8guid + " " + inter_path + "/integration")
                                        subprocess.call("./integration/ctbc_ocr " + "exec/" + traceId + "/" + p8guid + " " + inter_path + "/integration" , shell=True)

                                        targetPattern = './exec/' + traceId + '/' + p8guid + "/*OCR.loc"
                                        globtemp = glob.glob(targetPattern)

                                        if(globtemp != []):

                                            start_dml = open('./exec/'+ traceId +'/start_dml', 'w')

                                            for i in range(len(globtemp)):
                                                subprocess.call("python3 dml.py " + globtemp[i] , shell = True)

                                            dmltargetPattern = './exec/' + traceId + '/' + p8guid + "/*.dml"

                                            dmlglobtemp = glob.glob(dmltargetPattern)


                                            if(dmlglobtemp != []):
                                                start_runDML2CML = open('./exec/'+ traceId +'/start_runDML2CML', 'w')
                                                subprocess.call("./runDML2CML.sh " + traceId + " " + p8guid,shell=True)

                                        start_combinedoc = open('./exec/'+ traceId +'/start_combinedoc', 'w')
                                        subprocess.call("python3 combinedoc.py ./exec/" + traceId + " " + p8guid , shell = True)

                                        start_runCML2VML = open('./exec/'+ traceId +'/start_runCML2VML', 'w')
                                        subprocess.call("./runCML2VML.sh " + traceId + " " + p8guid, shell = True)


                        else:
                            if not os.path.exists('./exec/'+ traceId):
                                try:
                                    os.makedirs('./exec/' + traceId)
                                except OSError as exc:
                                    if exc.errno != errno.EEXIST:
                                        raise
                            filenetwrong = {"tiffInfo": {"@caseNo":receiveNo,"@p8guid":docIds,"@traceId":traceId,"@version": "v1.0","transError": { "@transFailReason": "filenet取件失敗" }}}
                            xmlstr = xmltodict.unparse(filenetwrong , pretty=True)
                            completeName = os.path.join("./filenetwrong.vml")
                            myfile = open(completeName,"w",encoding="utf-8")
                            myfile.write(xmlstr)
                            myfile.close()
                            os.makedirs('./filenetfaild')

                    
                    os.rmdir('./GPUBUSY')

                    process_management()
                    resp = jsonify({"resCode":200 , "rspMsg":"系統已結案"})
                    resp.status_code = 200
                    return resp
                else:
                    resp = jsonify({"resCode":200 , "rspMsg":"送出成功,系統已收案"})
                    resp.status_code = 200
                    return resp

        else:
            os.makedirs('./JSONWRONG')
            if(realjson.__contains__('traceId')==True):
                traceId = realjson['traceId']

                tempjson = {"traceId":traceId}

                jsonfile = os.path.join(root_path,"temp.json")

                with open(jsonfile,'w',encoding='utf-8') as filejson:
                    json.dump(tempjson,filejson,ensure_ascii=False)
                    filejson.write

                os.makedirs('./exec/' + traceId)

            process_management() 

            resp = jsonify({"resCode":200 , "rspMsg":"json格式錯誤"})
            resp.status_code = 200
            return resp

    
@app.route("/services/sqldata", methods=["OPTIONS","POST"])
def sqldata():

    if(request.method == 'OPTIONS'):
        headers = {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods':'POST , GET , OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers':'origin , x-csrftoken , content-type , accept',
        }

        return '' , 200 , headers

    else:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            
    
        f = os.fork()

        if(f == 0):
            Bankcoderesult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'Bank_Code_Chart'})


            Bankcodejson = {"Aux_Info":
                                {"Bank_Code_Chart":
                                    {"Chart":[]
                                    }

                                }
                            }



            for row  in Bankcoderesult:
                dict1 = {'@'+row[4]:row[1],'@'+row[2]:row[3]}
                Bankcodejson["Aux_Info"]["Bank_Code_Chart"]["Chart"].append(dict1)



            Bankxmlstr = xmltodict.unparse(Bankcodejson , pretty=True)


            completeName = os.path.join(save_path,"Bank_Code_Chart.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(Bankxmlstr)





            #print(Bankxmlstr)

            ######################################################################################################################################


            ExpIntresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'Exp_Int_Day'})


            ExpIntjson = {"Aux_Info":
                                {"Exp_Int_Day":{"Date":[]}
                                }
                            }

            for row  in ExpIntresult:
                dict1 = row[3]
                ExpIntjson["Aux_Info"]["Exp_Int_Day"]["Date"].append(dict1)


            ExpIntxmlstr = xmltodict.unparse(ExpIntjson , pretty=True)


            completeName = os.path.join(save_path,"Exp_Int_Day.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(ExpIntxmlstr)

            #print(ExpIntxmlstr)

            ######################################################################################################################################




            IBTFeeresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'IBT_Fee_Memo_KW'})


            IBTFeejson = {"Aux_Info":
                                {"IBT_Fee_Memo_KW":{"KW":[]}
                                }
                            }

            for row  in IBTFeeresult:
                dict1 = row[3]
                IBTFeejson["Aux_Info"]["IBT_Fee_Memo_KW"]["KW"].append(dict1)


            IBTFeexmlstr = xmltodict.unparse(IBTFeejson , pretty=True)


            completeName = os.path.join(save_path,"IBT_Fee_Memo_KW.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(IBTFeexmlstr)


            #print(IBTFeexmlstr)




            #####################################################################################################################################




            IBTMemoresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'IBT_Memo_KW'})




            IBTMemojson = {"Aux_Info":
                                {"IBT_Memo_KW":{"KW":[]}
                                }
                            }

            for row  in IBTMemoresult:
                dict1 = row[3]
                IBTMemojson["Aux_Info"]["IBT_Memo_KW"]["KW"].append(dict1)


            IBTMemoxmlstr = xmltodict.unparse(IBTMemojson , pretty=True)

            completeName = os.path.join(save_path,"IBT_Memo_KW.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(IBTMemoxmlstr)



            #print(IBTMemoxmlstr)


            ######################################################################################################################################




            IntMemoresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'Int_Memo_KW'})




            IntMemojson = {"Aux_Info":
                                {"Int_Memo_KW":{"KW":[]}
                                }
                            }

            for row  in IntMemoresult:
                dict1 = row[3]
                IntMemojson["Aux_Info"]["Int_Memo_KW"]["KW"].append(dict1)


            IntMemoxmlstr = xmltodict.unparse(IntMemojson , pretty=True)


            completeName = os.path.join(save_path,"Int_Memo_KW.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(IntMemoxmlstr)


            #print(IntMemoxmlstr)


            ######################################################################################################################################




            SalaryMemoresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'Salary_Memo_KW'})




            SalaryMemojson = {"Aux_Info":
                                {"Salary_Memo_KW":{"KW":[]}
                                }
                            }
            i = 0
            for row  in SalaryMemoresult:
                dict1 = {"@Rec_Type":row[1] , "#text":row[3]}
                
                SalaryMemojson["Aux_Info"]["Salary_Memo_KW"]["KW"].append(dict1)

                i=i+1
                


            SalaryMemoxmlstr = xmltodict.unparse(SalaryMemojson , pretty=True)

            completeName = os.path.join(save_path,"Salary_Memo_KW.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(SalaryMemoxmlstr)



            #print(SalaryMemoxmlstr)

            ######################################################################################################################################




            NonBankingresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'Non_Banking_Day'})




            NonBankingjson = {"Aux_Info":
                                {"Non_Banking_Day":{"KW":[]}
                                }
                            }

            for row  in NonBankingresult:
                dict1 = row[3]
                NonBankingjson["Aux_Info"]["Non_Banking_Day"]["KW"].append(dict1)



            NonBankingxmlstr = xmltodict.unparse(NonBankingjson , pretty=True)


            completeName = os.path.join(save_path,"Non_Banking_Day.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(NonBankingxmlstr)


            #print(NonBankingxmlstr)


            ######################################################################################################################################




            iPostcoderesult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'iPost_Code_Chart'})


            iPostcodejson = {"Aux_Info":
                                {"iPost_Code_Chart":
                                    {"Chart":[]
                                    }

                                }
                            }



            for row  in iPostcoderesult:
                dict1 = {'@'+row[4]:row[1],'@'+row[2]:row[3]}
                iPostcodejson["Aux_Info"]["iPost_Code_Chart"]["Chart"].append(dict1)



            iPostcodexmlstr = xmltodict.unparse(iPostcodejson , pretty=True)


            completeName = os.path.join(save_path,"iPost_Code_Chart.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(iPostcodexmlstr)


            #print(iPostcodexmlstr)

            ######################################################################################################################################

            Incomeresult = db.engine.execute('select * from  dbo.aux_view where code = %(code)s', {'code': 'Income_list_Withholding_voucher'})


            Incomejson = {"Aux_Info":{"IW_incomeCate_Chart":{"Chart":[]}}}



            for row  in Incomeresult:
                dict1 = {'@Code':row[1],'@Remark':row[3],'@Rec_Type':row[5]}
                Incomejson["Aux_Info"]["IW_incomeCate_Chart"]["Chart"].append(dict1)



            Incomexmlstr = xmltodict.unparse(Incomejson , pretty=True)


            completeName = os.path.join(save_path,"IW_incomeCate_Chart.xml")
            myfile = open(completeName,"w",encoding="utf-8")
            myfile.write(Incomexmlstr)

            #print(Incomexmlstr)

            resp = jsonify({"resCode":200 , "rspMsg":"sql成功"})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({"resCode":200 , "rspMsg":"送出成功,系統已收案"})
            resp.status_code = 200
            return resp


if __name__ == '__main__':
    

    if(os.path.exists('./GPUBUSY')):
        os.rmdir('./GPUBUSY')

    app.run(host="0.0.0.0",debug=True,port=6080)


