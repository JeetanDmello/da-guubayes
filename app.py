
from flask import Flask, render_template, redirect, url_for, request, session, get_flashed_messages
from flask_dropzone import Dropzone
import os
import json
# import process


app = Flask(__name__)
SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH= os.path.join(basedir,'static/posted'),
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*60*1000)
dropzone = Dropzone(app)

def loadpwd():
    pwdf = "pwd.txt"
    try:
        with open(pwdf, 'r') as file:
            #config = json.loads(file.read())
            config = json.loads(decrypt(file.read()))
    except IOError:
        config = {}
    return config

def decrypt(str1):
    strn = ""
    counter = 0
    for strg in str1.split("\n"):
        for chrt in strg.split(" "):
            if chrt != "":
                strn+=str(chr(int(chrt)-counter))
                counter += 1
                if(counter>1000):
                    counter = 0
        strn+="\n"
    return strn[:-1]

@app.route('/', methods=['GET', 'POST'])
def login():
    pwd=loadpwd()
    error = None
    print("The owner of this laptop is a true christian")
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        print(uname, password)
        if uname not in pwd.keys() or password != pwd[uname][0]:
            error = 'Invalid Credentials. Please try again.'
        else:
            response = redirect(url_for('home'))
            response.set_cookie('SessionCookie', uname, max_age = 600)
            session[uname]='USERNAME'
            return response
    return render_template('login.html', error=error)

# @app.route('/signup', methods = ['GET','POST']) 
# def signup():
#     print("In signin")
#     pwd=loadpwd()
#     if request.method == 'POST':
#         error = ''
#         uname = request.form['username']
#         password = request.form['password']
#         if uname  in pwd.keys():
#             error = 'Already exits'
#         else:
#             yep = {"Uname":uname,"Password":password}
#             json_obj = json.dumps(yep)
#             with open(pwdf,'r') as f:
#                 data = json.load(f)
#             data["credentials"].append(json_obj)
#             pwdf = "pwd.txt"
#             try:
#                 with open(pwdf, 'a') as file:
#                     #config = json.loads(file.read())
                    
#                     file.write(data)
#             except IOError:
#                 config = {}
#             response = redirect(url_for('login'))
#             return response

#     return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    dir='static/posted'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    user_id = request.cookies.get('SessionCookie')
    
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],"hello.png"))
        
    return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True)