from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app=Flask(__name__)
api=Api(app)

class User(Resource):
    def get(self):
        data=pd.read_csv('users.csv')
        data=data.to_dict()
        return {'data':data},200
    
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userId',required=True)
        parser.add_argument('name',required=True)
        parser.add_argument('city',required=True) #optional arguments with required=False
        args=parser.parse_args() #parse arguments and values in python dictionary

        new_data=pd.DataFrame({
            'userId':args['userId'],
            'name':args['name'],
            'city':args['city'],
            'locations':[[]]
        })

        data=pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return{
                'message':f"'{args['userId']}' already exists."
            }, 401
        else:
            new_data=pd.DataFrame({
                'userId':args['userId'],
                'name':args['name'],
                'city':args['city'],
                'locations':[[]]
            })
        data=data.append(new_data,ignore_index=True)
        data.to_csv('users.csv',index=False)
        return {'data':data.to_dict()},200
    # pass
    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userId',required=True)
        parser.add_argument('location',required=True)
        args=parser.parse_args() #argumets to dictionary

        data=pd.read_csv('users.csv')
        if args['userId'] in list(data['userId']):
            data['locations']=data['locations'].apply(lambda x: ast.literal_eval(x)) # evaluate strings to list of strings
            user_data=data[data['userId']==args['userId']]  #select user
            user_data['locations']=user_data['locations'].values[0].append(args['location'])
            data.to_csv('users.csv',index=False) # save to csv
            return {'data':data.to_dict()},200
        else:
            return{'message':f"'{args['userId']}' user not found."},404
         
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userId',required=True)
        args=parser.parse_args()
        data=pd.read_csv('users.csv')
        if args['userId'] in list(data['userId']):
            data=data[data['userId']!=args['userId']]
            data.to_csv('users.csv',index=False)
        else:
            return{'message':f"'{args['userId']}' user not found."},404

api.add_resource(User, '/user')


if __name__=='__main__':
    app.run(debug=True)
    