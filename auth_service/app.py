from flask import Flask,request ,render_template, jsonify,make_response
import os,jwt,datetime
import psycopg2
from dotenv import load_dotenv
app=Flask(__name__)

load_dotenv()

conn=psycopg2.connect(
    database=os.getenv("database"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port"))

def encode(username):
    try:
        payload={
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=0, minutes=10),
            "user": username
        }
        res= jwt.encode(
            payload,
            os.getenv("jwt_secret"),
            algorithm='HS256'
        )
        return res , None
    except Exception as e:
        print(e)
        return None , e

def decode(auth_token):
    try:
        payload = jwt.decode(
            auth_token,
            os.getenv("jwt_secret"),
            algorithms="HS256"
        )
        print(payload)
        return payload['user'], None
    except jwt.ExpiredSignatureError:
        return  None , 'Expired token, please log in again'
    except jwt.InvalidTokenError:
        return  None , 'Invalid token. Please log in again.'

@app.route('/')
def home():
    return render_template('index.html')
# for user
@app.route('/register', methods=['POST'])
def register():
    request_data=request.get_json()
    print(request_data)
    first_name=request_data['first_name']
    last_name=request_data['last_name']
    email=request_data['email']
    contact_no=int(request_data['contact_no'])
    password=request_data['password']

    try:
        cur=conn.cursor()
        res=cur.execute("INSERT INTO userlogin(first_name,last_name,email,contact_no,password) VALUES(%s, %s, %s, %s, %s)",(first_name,last_name,email,contact_no,password))
        print(res)
        conn.commit()
        cur.close()
    except Exception as err:
        print(err)
        message= str(err)
        return make_response(jsonify({
            'status': 'error',
            'message': message
        }))
    else:
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully registered'
        }),200)

# for user
@app.route('/login', methods=['POST'])
def login():
    request_data=request.get_json()
    username=request_data['email']
    password=request_data['password']

    if username=='' or password=='':
        return make_response(jsonify({
            'status': 'error',
            'message': 'unauthorized login'
        }),401)

    try:
        cur=conn.cursor()
        cur.execute("SELECT password,email FROM userlogin WHERE email='{}'".format(username))
        res=cur.fetchall()
        cur.close()
        if password in res[0]:
            res,e=encode(res[0][1])
            if e:
                raise Exception("Internal server error")
            else:
                return make_response(jsonify({
                    'status': 'success',
                    'token': res
            }),200)
        else:
            if password not in res[0]:
                return make_response(jsonify({
                'status': 'error',
                'message': 'forbidden, invalid username or password'
            }),403)
            else:
                return 'none', "invalid username or password"
    except Exception as err:
        message= str(err)
        return make_response(jsonify({
            'status': 'error',
            'message': message
        }))

@app.route('/validation')
def validate():
    try:
        bearer = request.headers.get('Authorization')
        if bearer is None:
            raise Exception("No token in header")
        else:
            token = bearer.split()[1] 
            res,e= decode(token)
            if e is None:
                return make_response(jsonify({
                    'status': 'success',
                    'message': res
                }))
            else:
                raise Exception(e)
    except Exception as err:
        print(err)
        message=str(err)
        return make_response({
            'status': 'error',
            'message': message
        })

# for retailer
@app.route('/jregister', methods=['POST'])
def jregister():
    request_data=request.get_json()
    first_name=request_data['first_name']
    last_name=request_data['last_name']
    email=request_data['email']
    contact_no=int(request_data['contact_no'])
    password=request_data['password']

    try:
        cur=conn.cursor()
        res=cur.execute("INSERT INTO ornamlogin(first_name,last_name,email,contact_no,password) VALUES(%s, %s, %s, %s, %s)",(first_name,last_name,email,contact_no,password))
        print(res)
        conn.commit()
        cur.close()
    except Exception as err:
        print(err)
        message=str(err)
        return make_response(jsonify({
            'status': 'error',
            'message': message
        }))
    else:
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully registered'
        }),200)

# for retailer
@app.route('/jlogin', methods=['POST'])
def jlogin():
    auth=request.get_json()
    username=auth['email']
    password=auth['password']

    if username=='' or password=='':
        return make_response(jsonify({
            'status': 'error',
            'message': 'unauthorized login'
        }),401)
    
    try:
        cur=conn.cursor()
        cur.execute("SELECT password,email FROM ornamlogin WHERE email='{}'".format(username))
        res= cur.fetchall()
        cur.close()
        if password in res[0]:
            print(res[0][1])
            res,e=encode(res[0][1])
            if e:
                raise Exception("Internal server error")
            else:
                return make_response(jsonify({
                    'status': 'success',
                'token': res
            }),200)
        else:
            if password not in res[0]:
                return make_response(jsonify({
                'status': 'error',
                'message': 'forbidden, invalid username or password'
            }),403)
            else:
                return 'none', "invalid username or password"
    except Exception as err:
        message=str(err)
        return make_response(jsonify({
            'status': 'error',
            'message': message
        }))

# for retailer
@app.route('/jvalidation')
def jvalidate():
    try:
        bearer = request.headers.get('Authorization')
        print(bearer)
        if bearer is None:
            raise Exception("No token in header")
        else:
            token = bearer.split()[1] 
            res, e= decode(token)
            if e is None:
                return make_response({
                    'status': 'success',
                    'user': res
                })
            else:
                return make_response({
                    'status': 'error',
                    'message': e
                })
    except Exception as err:
        print(err)
        message=str(err)
        return make_response({
            'status': 'error',
            'message': message
        })

if __name__ == "__main__":
    app.run(debug=True)