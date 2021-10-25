from flask import Flask,request


app = Flask(__name__)


def log(user,password):
    if user == 'admin' and password == 'password':
        return True
    else:
        return False



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
            if log(request.form['username'],request.form['password']):
                return 'Logged In'
            else:
                return "Invalid username or password"
app.run(host='127.0.0.1',port=80,debug=True)