from flask import Blueprint,request,jsonify
import Database.connection as connection

code_api = Blueprint('code_api',__name__)

@code_api.route('/codes', methods=['GET','POST'])
def codes() :
    conn = connection.db_connection()
    cursor = conn.cursor()
    if request.method=='GET':
        cursor.execute("SELECT * FROM code")
        codes = [
            dict(id=row[0],name = row[1], expiration_date=row[2], image=row[3],description=row[4],identifiant_QRCode=row[5],is_unique = row[6])
            for row in cursor.fetchall()
        ]
        if codes is not None :
            cursor.close()
            conn.close()
            return jsonify(codes)
    if request.method=='POST':
        data = request.get_json()
        new_name = data['name']
        new_expiration_date = data['expiration_date']
        new_image = data['image']
        new_description = data['description']
        new_identifiantQRCode = data['identifiant_QRCode']
        new_is_unique = data['is_unique']
        sql = """INSERT INTO code (name,expiration_date,image,description,identifiant_QRCode,is_unique) VALUES (?,?,?,?,?,?) """
        cursor.execute(sql,(new_name,new_expiration_date,new_image,new_description,new_identifiantQRCode,new_is_unique))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Code with the id {cursor.lastrowid} created successful"

@code_api.route('/code/<int:id>',methods=['GET','PUT','DELETE'])
def single_code(id):
    conn = connection.db_connection()
    cursor = conn.cursor()
    code = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM code WHERE id =?",(int(id),))
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

    if request.method == 'PUT' :
        sql = """UPDATE code
                SET name = ?,
                    expiration_date=?,
                    image=?,
                    description=?,
                    identifiant_QRCode=?,
                    is_unique =?
                WHERE id=? """
        data = request.get_json()
        name= data["name"]
        expiration_date = data["expiration_date"]
        image = data["image"]
        description = data["description"]
        identifiant_QRCode = data["identifiant_QRCode"]
        is_unique = data["is_unique"]
        updated_code = {
            'id':id,
            'name' : name,
            'expiration_date' : expiration_date,
            'image' : image,
            'description':description,
            'identifiant_QRCode':identifiant_QRCode,
            'is_unique' :is_unique
        }
        cursor.execute(sql,(name,expiration_date,image,description,identifiant_QRCode,is_unique,int(id)))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(updated_code)

    if request.method == 'DELETE':
        sql = """ DELETE FROM code WHERE id=? """
        cursor.execute(sql,(int(id),))
        conn.commit()
        cursor.close()
        conn.close()
        return "Code with the id {} has been deleted".format(id),200

@code_api.route('/code/<int:identifiant_QRCode',methods=['GET'])
def code_by_qrCode(identifiant_QRCode) :
    conn = connection.db_connection()
    cursor = conn.cursor()
    code = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM code WHERE identifiant_QRCode =?",(int(identifiant_QRCode),))
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