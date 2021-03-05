from flask import Blueprint,request,jsonify
import Database.connection as connection

codelist_api = Blueprint('codelist_api',__name__)

@codelist_api.route('/list/<int:user_id>',methods=['GET'])
def code_by_user(user_id) :
    conn = connection.db_connection()
    cursor= conn.cursor()
    if request.method=='GET' :
        cursor.execute("SELECT * FROM code WHERE id in (SELECT code_is from codelist where user_id =?)",(int(user_id),))
        codes = [
            dict(id=row[0],name = row[1], expiration_date=row[2], image=row[3],description=row[4],identifiant_QRCode=row[5],is_unique = row[6])
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        return jsonify(codes)

@codelist_api.route('/list',methods=['POST','DELETE'])
def codelist():
    conn = connection.db_connection()
    cursor= conn.cursor()
    if request.method=='POST' :
        data = request.get_json()
        code_id=data['code_id']
        user_id = data['user_id']
        status = data['status']
        sqllist = """INSERT INTO beerlist (code_is,user_id,status) VALUES (?,?,?) """
        cursor.execute(sqllist,(code_id,user_id,status))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Code {code_id} add to your favlist"

@codelist_api.route('/list/<int:code_id>/<int:user_id>',methods=['DELETE,PUT'])
def list_update(code_id,user_id) :
    if request.method=='DELETE' :
        sqllist = """DELETE FROM beerlist where code_id = ? and user_id=? """
        cursor.execute(sqllist,(int(code_id),int(user_id)))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Code {code_id} remove from your favlist"
    if request.method == 'PUT' :
        sql = """UPDATE codelist
                SET status = ?
                WHERE user_id=? and code_id=? """
        data = request.get_json()
        status = data['status']
        updated_code = {
            'user_id' : user_id,
            'code_id' : code_id,
            'status' : status,
        }
        cursor.execute(sql,(status,int(code_id),int(user_id)))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(updated_code)
