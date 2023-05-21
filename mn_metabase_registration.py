
import secrets
import requests
from scrtsxx import MetabaseCredentials

from flask import Flask,request

username = MetabaseCredentials.username
password = MetabaseCredentials.password
GroupID  = MetabaseCredentials.GroupID

mbUserURL       = "http://localhost:3000/api/user"
mbSessionURL    = "http://localhost:3000/api/session"
mbGroupURL      =  "http://localhost:3000/api/permissions/membership"

ErrorHTML = '''
        <html>
            <body>               
                <h2><span style="color: #00ccff;">FAILED!</span>&nbsp;</h2>
            </body>
        </html>
            
        '''

app = Flask(__name__)

@app.route('/registration', methods=['GET'])
def MN_Metabase_Registration():
    qp = request.args
    
    firstName = qp.get('fn')
    lastName  = qp.get('ln')
    email     = qp.get('email')
    password  = secrets.token_urlsafe(13)
    
    session = Generate_Metabase_Session_ID()
    
    if not session:
        return ErrorHTML
    
    mbdata = {'first_name' : firstName, 'last_name' : lastName, "email" : email, "password" : password}
    headers  = {"X-Metabase-Session": session}
    
    resp = requests.post(mbUserURL, json=mbdata, headers=headers)
    if resp.status_code == 200:
        JSON = resp.json()
        print(JSON)
        
        userid = JSON['id']
        
        ret = Add_New_User_To_Group(userid, session)
        
        if ret == 0:
            return '''
            <html>
                <body>               
                    <h2><span style="color: #00ccff;">An e-mail with login credentials has been sent to: %s</span>&nbsp;</h2>
                </body>
            </html>
                
            ''' % email
        else:
            return ErrorHTML
            
    else:
        return ErrorHTML
    
    
def Generate_Metabase_Session_ID():
    
    
    sessiondata = {"username" : username, "password" : password}
    
    resp = requests.post(mbSessionURL, json=sessiondata)
    if resp.status_code == 200:
        print(resp.json())
        return resp.json()['id']
    else:
        return None
    
    
def Add_New_User_To_Group(id, session):
    headers = {"X-Metabase-Session": session} 
    groupdata = {"group_id" : GroupID, "user_id" : id} 

    resp = requests.post(mbGroupURL, headers=headers, json=groupdata)
    
    if resp.status_code == 200:
        print(resp.json())
        print("User added to Group!")
        return 0
    else:
        return 404
    
        
    
    
    
    