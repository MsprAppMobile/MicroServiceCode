from flask import Blueprint,request,jsonify
import Database.connection as connection
from Router.VerifToken import verifyToken

code_api = Blueprint('code_api',__name__)

@code_api.route('/codes', methods=['GET','POST'])
def codes() :
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor = conn.cursor()
        if request.method=='GET':
            cursor.execute("SELECT * FROM code")
            codes = [
                dict(id=row[0],name = row[1], expiration_date=row[2], image=row[3],description=row[4], value=row[5],identifiant_QRCode=row[6],is_unique = row[7],category=row[8])
                for row in cursor.fetchall()
            ]
            if codes is not None :
                cursor.close()
                conn.close()
                return jsonify(codes),200
                
        if request.method=='POST':
            data = request.get_json()
            new_name = data['name']
            new_expiration_date = data['expiration_date']
            new_image = data['image']
            new_description = data['description']
            new_value = data['value']
            new_identifiantQRCode = data['identifiant_QRCode']
            new_is_unique = data['is_unique']
            new_category = data['category']
            sql = """INSERT INTO code (name,expiration_date,image,description,value,identifiant_QRCode,is_unique,category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
            cursor.execute(sql,(new_name,new_expiration_date,new_image,new_description,new_value,new_identifiantQRCode,new_is_unique,new_category))
            created_code = {
                'name' : new_name,
                'expiration_date' : new_expiration_date,
                'image' : new_image,
                'description':new_description,
                'value':new_value,
                'identifiant_QRCode':new_identifiantQRCode,
                'is_unique' :new_is_unique,
                'catgeory' : new_category
            }
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(created_code),201
    else :
        return "Your token is expired"

@code_api.route('/code/<int:id>',methods=['GET','PUT','DELETE'])
def single_code(id):
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor = conn.cursor()
        code = None
        if request.method == 'GET':
            cursor.execute("SELECT * FROM code WHERE id =%s",(int(id),))
            rows = cursor.fetchall()
            for r in rows :
                code = r
            if code is not None :
                cursor.close()
                conn.close()
                return jsonify(code),200
            else :
                cursor.close()
                conn.close()
                return "Bad user id",400

        if request.method == 'PUT' :
            sql = """UPDATE code
                    SET name = %s,
                        expiration_date=%s,
                        image=%s,
                        description=%s,
                        value=%s,
                        identifiant_QRCode=%s,
                        is_unique =%s,
                        category = %s
                    WHERE id=%s """
            data = request.get_json()
            name= data["name"]
            expiration_date = data["expiration_date"]
            image = data["image"]
            description = data["description"]
            value = data["value"]
            identifiant_QRCode = data["identifiant_QRCode"]
            is_unique = data["is_unique"]
            category = data['category']
            updated_code = {
                'id':id,
                'name' : name,
                'expiration_date' : expiration_date,
                'image' : image,
                'description':description,
                'value':value,
                'identifiant_QRCode':identifiant_QRCode,
                'is_unique' :is_unique,
                'category' :category
            }
            cursor.execute(sql,(name,expiration_date,image,description,value,identifiant_QRCode,is_unique,category,int(id)))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(updated_code)

        if request.method == 'DELETE':
            sql = """ DELETE FROM code WHERE id=%s """
            cursor.execute(sql,(int(id),))
            conn.commit()
            cursor.close()
            conn.close()
            return id,200
    else :
        return "Your token is expired"

@code_api.route('/code/<string:identifiant_QRCode>',methods=['GET'])
def code_by_qrCode(identifiant_QRCode) :
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor = conn.cursor()
        code = None
        if request.method == 'GET':
            cursor.execute("SELECT * FROM code WHERE identifiant_QRCode =?",(identifiant_QRCode,))
            rows = cursor.fetchall()
            for r in rows :
                code = r
            if code is not None :
                cursor.close()
                conn.close()
                return jsonify(code),200
            else :
                cursor.close()
                conn.close()
                return "Something wrong",404
    else :
        return "Your token is expired"