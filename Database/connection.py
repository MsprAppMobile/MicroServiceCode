import mariadb

def db_connection():
    conn = None
    try : conn = mariadb.connect(user='baptistebrs', password='test', host='127.0.0.1',database='GoStyle')
    except mariadb.Error as e:
        print('erreur')
    return conn