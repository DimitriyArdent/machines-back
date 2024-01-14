
from quart import Quart, request, Blueprint,   current_app, json
import aiopg
import json
from quart import jsonify

from quart_jwt_extended import decode_token
from quart_jwt_extended import create_access_token
from datetime import timedelta
from datetime import datetime

counter = 0

 
login = Blueprint('login', __name__)


 

@login.route('/login', methods=["POST"])
async def another_page():
    res =  await request.get_data()
    login_data = json.loads(res.decode('utf-8'))
    username = login_data.get("username")
    password = login_data.get("password")
    print(username)
    print(password)

    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM login('{username}', '{password}');")
            result = await cursor.fetchall()
            if result and result[0]:
                token =  create_access_token(username, expires_delta=timedelta(hours=12))
                res = {"token": token, "full_name":username }
                return res, 200
            else:
                return 'no access',401


@login.route('/tokenVerification', methods=["GET", "POST", "PUT", "DELETE"])
async def tokenVerification():
    print(request.path) 

    if(request.path == '/account/login'):    
        return None
    else:
        data = await request.json    
        if  isinstance(data, dict):       
            data = json.loads(json.dumps(data))
            data = data.get('username')


        authorization_header = request.headers.get('Authorization')  # Bearer eyJhbGciOiJIUzI1...
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            decoded_token = decode_token(token)
            identity = decoded_token.get('identity', None)   # 'John Smith'
            print(identity + '  ' + 'identity')
            print(data + '  ' + 'data')

            if(isinstance(data, str)):
                print(identity+ '  ' + data)
                if(identity == data):  
                    return None
                else:
                    return {'error':'The token is not valid', "error": 404}
            

     
    
   
 


@login.route('/test', methods=["POST"])
async def test():
    

    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM  machines")
            result = await cursor.fetchall()
            try:
                if result  :
                    
                    return  jsonify(result)
                else:
                    return  {"b":2}
            except Exception as e:
              current_app.logger.error(f"Error in test route: {str(e)}")
              return jsonify({"error": "Internal server error"}), 500
