from flask import Blueprint,request,jsonify
import Database.connection as connection
from Router.VerifToken import verifyToken

codelist_api = Blueprint('codelist_api',__name__)

@codelist_api.route('/list/<int:user_id>',methods=['GET'])
def code_by_user(user_id) :
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor= conn.cursor()
        if request.method=='GET' :
            cursor.execute("SELECT code.id, code.name, code.expiration_date, code.image, code.description, code.value, code.identifiant_QRCode, code.is_unique, code.category, codelist.status from code INNER JOIN codelist ON code.id = codelist.code_id where codelist.user_id =%s",(int(user_id),))
            list_codes = [
                dict(id=row[0],name = row[1], expiration_date=row[2], image=row[3],description=row[4], value=row[5],identifiant_QRCode=row[6],is_unique = row[7],category=row[8],status=row[9])
                for row in cursor.fetchall()
            ]
            cursor.close()
            conn.close()
            return jsonify(list_codes),200
    else :
        return "Your token is expired"
    else :
        return "Your token is expired"

@codelist_api.route('/list',methods=['POST'])
def codelist():
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor= conn.cursor()
        if request.method=='POST' :
            data = request.get_json()
            code_id=data['code_id']
            user_id = data['user_id']
            status = data['status']
            sqllist = """INSERT INTO codelist (code_id,user_id,status) VALUES (%s,%s,%s) """
            cursor.execute(sqllist,(code_id,user_id,status))
            cerated_item = {
                'code_id' : code_id,
                'user_id' : user_id,
                'status' : status
            }
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(cerated_item),200
    else :
        return "Your token is expired"

@codelist_api.route('/list/<int:code_id>/<int:user_id>',methods=['DELETE','PUT'])
def list_update(code_id,user_id) :
    token = request.headers.get('token')
    if(verifyToken(token)) :
        conn = connection.db_connection()
        cursor= conn.cursor()
        if request.method=='DELETE' :
            sqllist = """DELETE FROM codelist where code_id = %s and user_id=%s """
            cursor.execute(sqllist,(int(code_id),int(user_id)))
            conn.commit()
            cursor.close()
            conn.close()
            return code_id
        if request.method == 'PUT' :
            sql = """UPDATE codelist
                    SET status = ?
                    WHERE user_id=%s and code_id=%s """
            data = request.get_json()
            status = data['status']
            updated_code = {
                'user_id' : user_id,
                'code_id' : code_id,
                'status' :  bool(status),
            }
            cursor.execute(sql,(status,int(code_id),int(user_id)))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify(updated_code),200
    else :
        return "Your token is expired"
