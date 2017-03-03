'''
Created on Dec 3, 2014
Script to keepalive of PSS API
create Class CaseReport to reduce the repetition
@author: liwan3
'''
import sys,os,time,datetime
#from suds.client import Client
import urllib2
import json
import httplib
import csv
import re
import time
import csv,xlrd,xlwt
from dateutil.tz import *

reload(sys)
sys.setdefaultencoding('utf-8')

class CaseReport(object):
    """
    Attributes: Client Id, Client Secret, Token
                Get methods of each Service
    """
    def __init__(self,id,secret):
        """returning a new Monitor Object"""
        self.id=id
        self.secret=secret
        self.token=''

    def getToken(self):
        """to generate the new token"""
        import subprocess,shlex
        """the shelex's split method will split the raw command line into a sequence, the default delimiter is whitespace"""
        command="""curl -k -H "Content-Type: application/x-www-form-urlencoded" -X POST -d "client_id=%s" \
        -d "client_secret=%s" -d "grant_type=client_credentials" https://cloudsso.cisco.com/as/token.oauth2"""%(self.id,self.secret)
        args = shlex.split(command)
        results=[]
        matched=None
        try:
            process = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout,stderr=process.communicate()
        except:
            results=[False,'failed to get token from https://cloudsso.cisco.com/as/token.oauth2']

        else:
            token_type=''
            access_token=''
            matched=re.search("\"access_token\":\"(\S+)\",\"token_type\":\"(\S+)\",\"expires_in\":\d+",stdout)
            if matched:
                token_type=matched.group(2)
                access_token=matched.group(1)
            else:
                results=[False,stdout]
                return results
            if 'bearer' in token_type:
                token_type='Bearer'
            self.token="%s %s"%(token_type,access_token)
            results=[True,self.token]
        return results

    def fillHeaders(self,action):
        headers={}
        headers["Authorization"]=self.token
        #////////
        #print self.token
        #////////

        headers["Host"]="api.cisco.com"
        #headers["SOAPAction"]=action
        headers["Accept"]="text/html, application/xhtml+xml, */*"
        headers["Accept-Encoding"]="gzip,deflate"
        headers["User-Agent"]="Jakarta Commons-HttpClient/3.1"
        headers["Content-Type"]="text/xml;charset=UTF-8"

        return headers

    def getCaseSummary(self,case_ids):
        HttpHeaders={}
        HttpHeaders=self.fillHeaders(0)#0----no action
        try:
            conn = httplib.HTTPSConnection("api.cisco.com")
            conn.request("GET",case_ids,"",HttpHeaders)
            res = conn.getresponse()
            response=[res.status,res.read()]
            #/////////////
            #print "Return code:", res.status, " reason:", res.reason, " details:", res.read()
            #/////////////

        except urllib2.URLError, e:
            response=[e.reason.errno,None]
            print "exit case code1"
        except httplib.HTTPException, e:
            print "exit case code3"
            conn.connect()
        except:
            response=[sys.exc_info()[1],sys.exc_info()[2]]
            print "exit case code2"
        return response

    def de_json(self,o_json):
        try:
            data = json.loads(o_json)
            return data
        except:
            print "decode json error"

    def call_caseAPI(self,case_id):
        case_combine = ""
        case_string="/case/v1.0/cases/case_ids/"

        case_combine = str(case_string)+str(case_id).strip('\n')
        '''Based on Case API limited, one call need limit to 10 per seconds,try 5 per seconds'''
        time.sleep(1)

        status,case_raw_data = self.getCaseSummary(case_combine)
        case_status=self.format_case_output(case_raw_data)

        return case_status

    def format_case_output(self,case_o):
        try:
            data = self.de_json(case_o)
            case_status = str(data["RESPONSE"]["CASES"]["CASE"]["STATUS"])

            return case_status
        except:
            return "CANNOT QUERY"

    def combine_report(self):
        new_array = []
        with open('CdetCase.csv') as csv_obj:
            reader_cur = csv.reader(csv_obj)
            for row in reader_cur:
                case_id = 0
                case_id = row[19]
                if case_id:
                    row.insert(20,str(self.generate_case_status(case_id)))
                    new_array.append(row)
        return new_array

    def generate_case_status(self,each_caseid):
        item_case_status = []
        if (len(str(each_caseid)) == 9):
            case_status1 = self.call_caseAPI(str(each_caseid))
            item_case_status.append(case_status1)
        elif (len(str(each_caseid)) == 15):
            item_case_status.append("Case Status")
        elif (len(str(each_caseid)) >= 19):
            case_string = ""
            case_status_string = ""
            part_caseId = []
            part_caseId = str(each_caseid).split(';')
            for each_part_caseId in part_caseId:
                case_status = self.call_caseAPI(str(each_part_caseId))
                case_status_string = case_status_string + case_status + ";"
            item_case_status.append(str(case_status_string).strip(';'))
        print str(item_case_status)
        #return str(item_case_status)
        return str(item_case_status[0])

    def xls_set_style(name,height,bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        
        return style
            
    def file_name(self):
        try:
            pathname = os.path.dirname(sys.argv[0])
            date=datetime.date.today()
            filename=os.path.join(pathname,"%s-bugReport")%date
            fmt = '%Y-%m-%d %H:%M:%S %p %Z'
            now = datetime.datetime.now(tzlocal())
            dt=now.strftime(fmt)

            return filename
        except Exception,e:
            return str(e)

    def write_xls(self,outdata):
#        Workbook = self.open_excel()
        n = 1
        wb = xlwt.Workbook()
        sheet_sntc = wb.add_sheet(u'PSS-SNTC',cell_overwrite_ok= True)

        for i in range(0,len(outdata)-1):
            n = n+1
            print "Count:", n
            for j in range(0,len(outdata[i])):
                sheet_sntc.write(i,j,outdata[i][j])

        filename = self.file_name() + '.xls'
        wb.save(filename)
    '''
    def write_csv(self,outdata):
        n=1
        pathname = os.path.dirname(sys.argv[0])
        date=datetime.date.today()
        filename=os.path.join(pathname,"%s-bugReport.csv")%date
        fmt = '%Y-%m-%d %H:%M:%S %p %Z'
        now = datetime.datetime.now(tzlocal())
        dt=now.strftime(fmt)
        csvfile = file(filename,'w')
        writer = csv.writer(csvfile)
        for data in outdata:
            n = n+1
            print "Count:", n
            writer.writerow(data)
        csvfile.close()            
    '''
if __name__ == '__main__':
    Monitor=CaseReport("h6jtt29msjs6htewyrd8jmnj","mczhMdVQjkqyrTSBRcy2RRXJ")
    token_status,token_string=Monitor.getToken()
    if not token_status:
        status_str='Could not get Token, Reason:%s'%token_string
        print status_str
    else:
        output_data = []
        output_data = Monitor.combine_report()
        Monitor.write_xls(output_data)
        #Monitor.write_csv(output_data)
