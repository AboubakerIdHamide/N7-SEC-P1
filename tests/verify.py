#!/usr/bin/env python3
"""Repeatable HTTP integration checks. Uses only Python standard library; demo data is retained."""
import json,urllib.request,urllib.error,time,base64,hmac,hashlib,os
from pathlib import Path
BASE=os.environ.get('API_URL','http://127.0.0.1:8080')
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
results=[]
def req(name,method,path,expected,body=None,token=None):
 headers={'Content-Type':'application/json'}
 if token:headers['Authorization']='Bearer '+token
 r=urllib.request.Request(BASE+path,json.dumps(body).encode() if body is not None else None,headers,method=method)
 try:
  with opener.open(r,timeout=15) as response:code=response.status;raw=response.read().decode()
 except urllib.error.HTTPError as e:code=e.code;raw=e.read().decode()
 try:data=json.loads(raw)
 except ValueError:data=raw
 results.append({'name':name,'method':method,'path':path,'expected':expected,'actual':code,'pass':code==expected,'response':data if '/auth/' not in path or code!=200 and code!=201 else {'message':'Token received (redacted)'}})
 print(('PASS' if code==expected else 'FAIL'),code,name,flush=True)
 if code!=expected: print(data);raise AssertionError(name)
 return data
password='Demo1234!'
def login(email):return req('Login '+email,'POST','/auth/login',200,{'email':email,'password':password})
a=login('admin@demo.test');e1=login('employee1@demo.test');e2=login('employee2@demo.test');t=login('tech@demo.test')
A,E,F,T=[u['token'] for u in [a,e1,e2,t]]
req('01 No JWT','GET','/api/profile',401)
req('02 Invalid JWT','GET','/api/profile',401,token='invalid.token.value')
def b64(v):return base64.urlsafe_b64encode(v).rstrip(b'=')
header=b64(json.dumps({'alg':'HS256','typ':'JWT'}).encode());payload=b64(json.dumps({'sub':'employee1@demo.test','role':'EMPLOYEE','iat':int(time.time())-600,'exp':int(time.time())-300}).encode());unsigned=header+b'.'+payload
secret=base64.b64decode(os.environ.get('JWT_SECRET','VGhpcy1pcy1hLXNlY3JldC1rZXktZm9yLWRlbW8tand0LXNpZ25pbmctMzI='))
expired=(unsigned+b'.'+b64(hmac.new(secret,unsigned,hashlib.sha256).digest())).decode()
req('03 Expired correctly signed JWT','GET','/api/profile',401,token=expired)
req('04 Employee admin route','GET','/api/admin/users',403,token=E)
def incident(title,category,priority,token):return req('Create '+title,'POST','/api/incidents',201,{'title':title,'description':'Classroom demonstration: investigate, document the action, and verify resolution.','category':category,'priority':priority},token)
i1=incident('Suspicious phishing email','PHISHING','CRITICAL',E);i2=incident('Office Wi-Fi connection failure','NETWORK','MEDIUM',E);i3=incident('Account access blocked','ACCESS','HIGH',F)
req('05 Other employee incident','GET',f"/api/incidents/{i3['id']}",403,token=E)
req('06 Unassigned technician update','PUT',f"/api/incidents/{i3['id']}/status",403,{'status':'IN_PROGRESS'},T)
req('Disable employee 2','PUT',f"/api/admin/users/{e2['user']['id']}/disable",200,token=A)
req('07 Disabled login','POST','/auth/login',401,{'email':'employee2@demo.test','password':password})
req('Disabled existing JWT','GET','/api/profile',401,token=F)
req('Reenable employee 2','PUT',f"/api/admin/users/{e2['user']['id']}/enable",200,token=A)
req('08 Duplicate email','POST','/auth/register',409,{'fullName':'Duplicate','email':'employee1@demo.test','password':password})
req('09 Invalid incident data','POST','/api/incidents',400,{'title':'','description':'','category':'PHISHING'},E)
req('Admin list','GET','/api/incidents',200,token=A)
req('Employee cannot assign','PUT',f"/api/incidents/{i1['id']}/assign/{t['user']['id']}",403,token=E)
req('Admin assignment','PUT',f"/api/incidents/{i1['id']}/assign/{t['user']['id']}",200,token=A)
assigned=req('Technician assigned list','GET','/api/incidents/assigned',200,token=T);assert any(i['id']==i1['id'] for i in assigned)
req('Start treatment','PUT',f"/api/incidents/{i1['id']}/status",200,{'status':'IN_PROGRESS'},T)
req('Add treatment note','POST',f"/api/incidents/{i1['id']}/comments",201,{'content':'Le poste a ete isole du reseau. Analyse antivirus effectuee. Le message de phishing a ete supprime.'},T)
req('Resolve incident','PUT',f"/api/incidents/{i1['id']}/status",200,{'status':'RESOLVED'},T)
detail=req('Owner sees state and history','GET',f"/api/incidents/{i1['id']}",200,token=E);assert detail['incident']['status']=='RESOLVED' and len(detail['history'])>=5 and len(detail['comments'])>=1
mine=req('Employee list isolation','GET','/api/incidents/my',200,token=E);assert all(i['createdBy']['id']==e1['user']['id'] for i in mine)
req('Close incident','PUT',f"/api/incidents/{i2['id']}/status",200,{'status':'CLOSED'},A)
req('Closed incident locked','PUT',f"/api/incidents/{i2['id']}/status",409,{'status':'OPEN'},A)
req('Unknown incident','GET','/api/incidents/99999999',404,token=A)
req('Admin statistics','GET','/api/admin/statistics',200,token=A)
email='registration-'+str(int(time.time()))+'@demo.test'
reg=req('Registration ignores requested ADMIN role','POST','/auth/register',201,{'fullName':'Security Test Employee','email':email,'password':password,'role':'ADMIN'});assert reg['role']=='EMPLOYEE'
R=reg['token']
req('Wrong current password','PUT','/api/profile/password',400,{'oldPassword':'incorrect','newPassword':'Updated123!','confirmation':'Updated123!'},R)
req('Password confirmation mismatch','PUT','/api/profile/password',400,{'oldPassword':password,'newPassword':'Updated123!','confirmation':'Mismatch123!'},R)
req('Change password','PUT','/api/profile/password',200,{'oldPassword':password,'newPassword':'Updated123!','confirmation':'Updated123!'},R)
req('Old password rejected','POST','/auth/login',401,{'email':email,'password':password})
req('New password accepted','POST','/auth/login',200,{'email':email,'password':'Updated123!'})
updated=req('Update name and email','PUT','/api/profile',200,{'fullName':'Updated Test Employee','email':'updated-'+email},R)
req('Profile refreshed token','GET','/api/profile',200,token=updated['token'])
output=Path(__file__).resolve().parents[1]/'docs';output.mkdir(exist_ok=True)
(output/'test-results.json').write_text(json.dumps(results,indent=2))
(output/'demo-fixtures.json').write_text(json.dumps({'incidentId':i1['id'],'otherIncidentId':i3['id'],'technicianId':t['user']['id'],'employee2Id':e2['user']['id'],'expiredToken':expired},indent=2))
print(f'\n{len(results)}/{len(results)} HTTP checks passed. Scenario complete.')
