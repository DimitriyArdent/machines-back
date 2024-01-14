from quart import Quart, request, Blueprint,   current_app, json,jsonify
import aiopg
import json
from quart_jwt_extended import JWTManager
from quart_jwt_extended import create_access_token
from datetime import timedelta
import psycopg2
from utils.constants import CONNECTION_STRING

 
machines = Blueprint('machines', __name__)



 

@machines.route('', methods=["POST"])
async def test():
 
    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM  get_machines()")
            result = await cursor.fetchall()
            try:
                if result  :
                    column_names = [desc[0] for desc in cursor.description]
                    rows_as_dicts = [dict(zip(column_names, row)) for row in result]
                    return  jsonify(rows_as_dicts)
                else:
                    return  {"error":"error"}
            except Exception as e:
              return jsonify({"error": "Internal server error"}), 500


@machines.route('/images', methods=["POST"])
async def get_images():
    
     async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM  get_images()")
            result = await cursor.fetchall()
            try:
                if result  :
                    column_names = [desc[0] for desc in cursor.description]
                    rows_as_dicts = [dict(zip(column_names, row)) for row in result]
                    return  jsonify(rows_as_dicts)
                else:
                    return  {"error":"error"}
            except Exception as e:
              return jsonify({"error": "Internal server error"}), 500






@machines.route('/get_specific_machine', methods=["POST"])
async def get_specific_machine():
 
    res =  await request.get_data()
    specific_machine_data = json.loads(res.decode('utf-8'))
    machine_id = specific_machine_data.get("machine_id")

    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM get_specific_machine('{machine_id}');")
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in await cursor.fetchall()]
            if result and  result[0]:
                res = {"result": result }
                return res, 200
            else:
                return 'machine was not found',404
            



 

@machines.route('/manufacturerIds', methods=["POST"])
async def get_manufacturerIds():
    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute( "SELECT * FROM select_manufacturers_id();")
            result = await cursor.fetchall()
            if result:
                flattened_list = [item for sublist in result for item in sublist]

                res = {"result": flattened_list }
                return res, 200
            else:
                return 'manufacturers if=d were not found',404
            





@machines.route('/delete_machine', methods=["POST"])
async def delete_machine():
  
    res =  await request.get_data()
    delete_machine_data = json.loads(res.decode('utf-8'))
    machine_id = delete_machine_data.get('machine_id')
 
      
    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT delete_machine('{machine_id}');")
            result = await cursor.fetchall()
            if result and  result[0][0] == True:    
                res = {"result": result }
                return {"res":res, "status": 200, "id":machine_id}
            else:
                return 'machine was not found',500
            


            
@machines.route('/filterNames', methods=["POST"])
async def filter_machine_name():
    res =  await request.get_data()
    filter_names_machine_data = json.loads(res.decode('utf-8'))
    searchParams = filter_names_machine_data.get('searchParams')
    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * from filter_machine_name('{searchParams}');")
            result = await cursor.fetchall()
            try:
                if result    :   
                    column_names = [desc[0] for desc in cursor.description]
                    rows_as_dicts = [dict(zip(column_names, row)) for row in result]
                    return  jsonify(rows_as_dicts)         
                else:
                    return 'machine was not found',500
            except Exception as e:
                print(e)


            
@machines.route('/filterManufacturerId', methods=["POST"])
async def filter_filterManufacturerId():
    res =  await request.get_data()
    filter_filterManufacturerId = json.loads(res.decode('utf-8'))
    searchParams = filter_filterManufacturerId.get('searchParams')
    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * from   filter_manufacturerid('{searchParams}');")
            result = await cursor.fetchall()
            try:
                if result    :   
                    column_names = [desc[0] for desc in cursor.description]
                    rows_as_dicts = [dict(zip(column_names, row)) for row in result]
                    return  jsonify(rows_as_dicts)         
                else:
                    return 'machine was not found',500
            except Exception as e:
                print(e)
            
 

@machines.route('/filterStatus', methods=["POST"])
async def filter_status():
    res =  await request.get_data()
    filter_filterManufacturerId = json.loads(res.decode('utf-8'))
    searchParams = filter_filterManufacturerId.get('searchParams')
    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * from   filter_status('{searchParams}');")
            result = await cursor.fetchall()
            try:
                if result    :   
                    column_names = [desc[0] for desc in cursor.description]
                    rows_as_dicts = [dict(zip(column_names, row)) for row in result]
                    return  jsonify(rows_as_dicts)         
                else:
                    return 'machine was not found',500
            except Exception as e:
                print(e)
            




@machines.route('/order', methods=["POST"])
async def order():
    res =  await request.get_data()
    order = json.loads(res.decode('utf-8'))
 
    searchParams = order.get('searchParams')
    dir = searchParams[0].get('dir')
    column = searchParams[0].get('field')

    if(dir == None):
        dir = 'asc'

    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * from   order_by('{dir}','{column}');")
            result = await cursor.fetchall()
            try:
                if result    :   
                    column_names = [desc[0] for desc in cursor.description]
                    rows_as_dicts = [dict(zip(column_names, row)) for row in result]
                    return  jsonify(rows_as_dicts)         
                else:
                    return 'machine was not found',500
            except Exception as e:
                print(e)
            


































@machines.route('/update_machine', methods=["POST"])
async def update_machine():
 
    res =  await request.get_data()
    update_machine_data = json.loads(res.decode('utf-8'))
    update_machine_data = update_machine_data['editedValues']

    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    machineid = update_machine_data[0]
    machinename = update_machine_data[1]
    manufacturerid = update_machine_data[2]
    purchasedatetime = update_machine_data[3]
    yearofmanufacture = update_machine_data[4]
    machinestatus = update_machine_data[5]
    capacity = update_machine_data[6]
     

        # Execute the SQL function with parameters
    cur.execute("""
            SELECT * FROM update_machine(%s, %s, %s, %s, %s, %s, %s);
        """, (
            machineid,
            machinename,
            manufacturerid,
            purchasedatetime,
            yearofmanufacture,
            machinestatus,
            capacity
        ))

    column_names = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result_with_columns = [dict(zip(column_names, row)) for row in result]
    conn.commit()
    cur.close()
    conn.close()
    if result  :   
        res = {"result": result_with_columns }
        return {"res":res, "status": 200 }
    else:
        return 'machine was not updated',500
   

@machines.route('/update_image', methods=["POST"])
async def update_image():
    res =  await request.get_data()
    update_image = json.loads(res.decode('utf-8'))
    image_table_values = update_image.get('imageTableValues')
    imageurl= image_table_values[0]
    machineId = image_table_values[1]
    

    async with current_app.config["pool"].acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute( f"SELECT * FROM add_image('{imageurl}','{machineId}');")
            result = await cursor.fetchall()
            if result:
                
                flattened_list = [item for sublist in result for item in sublist]

                res = {"result": flattened_list }
                return {"result":res, "status": 200}
            else:
                return 'update_image operation failed',404
            


 

@machines.route('/add_machine', methods=["POST"])
async def add_machine():
 
 
    res =  await request.get_data()
    add_machine_data = json.loads(res.decode('utf-8'))
    update_machine_data = add_machine_data['machine']
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    machinename = update_machine_data[1]
    manufacturerid = update_machine_data[2]
    purchasedatetime = update_machine_data[3]
    yearofmanufacture = update_machine_data[4]
    machinestatus = update_machine_data[5]
    capacity = update_machine_data[6]
    cur.execute("""
            SELECT * FROM add_machine(  %s, %s, %s, %s, %s, %s);
        """, (
             
            machinename,
            manufacturerid,
            purchasedatetime,
            yearofmanufacture,
            machinestatus,
            capacity 
        ))

    column_names = [desc[0] for desc in cur.description]

    result = cur.fetchall()
    result_with_columns = [dict(zip(column_names, row)) for row in result]
    conn.commit()
    cur.close()
    conn.close()
    if result  :   
        res = {"result": result_with_columns }
        return {"res":res, "status": 200 }
    else:
        return 'machine was not updated',500
