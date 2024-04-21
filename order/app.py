from flask import Flask,request,make_response,jsonify
from flask_pymongo import PyMongo, ObjectId
import pika
import time
import os
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MONGO_URI']= os.getenv("MONGO_URI")
mongo=PyMongo(app)

def send_broker_message(msg):
    try:
        connectionParameters = pika.ConnectionParameters(host= os.getenv("RABBITMQ_HOST"))
        connection = pika.BlockingConnection(parameters= connectionParameters)
        channel = connection.channel()
        channel.basic_publish(exchange=os.getenv("EXCHANGE_NAME"), routing_key=os.getenv("ROUTING_KEY"), body=msg)
        channel.close()
        return jsonify({
            'success': True,
            'message': 'successfully published'
        })
    except Exception as err:
        print(err)
        return jsonify({
            'success': False,
            'messsage': err
        })

@app.route('/')
def home():
    result=[]
    res=mongo.db.user.find(
        {'email': 'udaiyar.satish03@gmail.com'}
    )
    for data in res:
        data['_nid']=str(data['_id'])
        data.pop('_id')
        data.pop('photo')
        result.append(data)
    return make_response(jsonify({
        'data': result
    }),200)

@app.route('/placerequest')
def add_order_request():
    try:
        data=request.get_json()
        store_id=data['_sid']
        print(store_id)
        user_id=data['_uid']
        print(user_id)
        res1=mongo.db.user.find({
            "_id": ObjectId(user_id)
        })
        for data1 in res1:
            data1.pop('_id')
            data1.pop('photo')
        print(data1)
        res2=mongo.db.store.find({
            "_id": ObjectId(store_id)
        })
        for data2 in res2:
            data2.pop('_id')
        print(data2)
        fres=mongo.db.order.insert_one({
            'email': data1['email'],
            'description': data1['description'],
            'loc': data2['loc'],
            'owned_by': data2['owned_by'],
            'making_charges': data2['making_charges'],
            'status': 'pending',
            'lat': data2['lat'],
            'long': data2['long']
        })
        msg={
            'message': 'successfully order placed'
        }
        broker_result = send_broker_message(msg=msg)
        print(broker_result)
        # need to connect to message broker for notification service here
        # after that send response for successful order placement
        return make_response(jsonify({
            'status': 'success',
            'message': 'order request successfully placed'
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': err
        }))
    
@app.route('/uorder_check')
def uorder_check():
    try:
        result=[]
        data= request.get_json()
        email= data['email']
        res=mongo.db.order.find({
            '$and': [{'status': 'pending'}, {'email': email}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/rorder_check')
def rorder_check():
    try:
        result=[]
        data= request.get_json()
        username= data['user']
        res=mongo.db.order.find({
            '$and': [{'status': 'pending'}, {'owned_by': username}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/uaccepted_order')
def uaccepted_order():
    try:
        result=[]
        data=request.get_json()
        email=data['email']
        res=mongo.db.order.find({
            '$and': [{'status': 'accepted'}, {'email': email}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/raccepted_order')
def raccepted_order():
    try:
        result=[]
        data=request.get_json()
        username= data['user']
        res=mongo.db.order.find({
            '$and': [{'status': 'accepted'}, {'owned_by': username}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/accept')
def accept():
    try:
        data=request.get_json()
        _id= data['_id']
        query_find={"_id": ObjectId(_id)}
        query_update={ "$set": {
            "status": "accepted"
        }}
        print('hi')
        res=mongo.db.order.update_one(query_find, query_update)
        print(res)
        # after the retalier is willing to work on the project, connect to broker for notification service
        # after response from broker send response successful acceptance
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully accepted'
        }))
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
@app.route('/reject')
def reject():
    try:
        data=request.get_json()
        _id= data['_id']
        query_find={"_id": ObjectId(_id)}
        res=mongo.db.order.delete_one(query_find)
        # after the retalier decides to reject the project, connect to broker for notification service
        # after response from broker send response successful rejection
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully rejected'
        }))
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))

@app.route('/done')
def done():
    try:
        data=request.get_json()
        _id= data['_id']
        query_find={"_id": ObjectId(_id)}
        query_update={ "$set": {
            "status": "done"
        }}
        res=mongo.db.order.update_one(query_find, query_update)
        # after the retalier done with the project, connect to broker for notification service
        # after response from broker send response successfully done
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully done'
        }))
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)