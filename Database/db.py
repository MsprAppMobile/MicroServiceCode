import connection

conn = connection.db_connection()

cursor = conn.cursor()

sql_delete_codeList = """DROP TABLE IF EXISTS codelist;"""  

sql_delete_code = """DROP TABLE IF EXISTS code; """

sql_delete_user = """DROP TABLE IF EXISTS user """

sql_code= """CREATE table code (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    expiration_date DATETIME NOT NULL,
    image VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    value INT NOT NULL,
    identifiant_QRCode VARCHAR(200) NOT NULL,
    is_unique BOOLEAN NOT NULL,
    category VARCHAR(300) NOT NULL);"""

sql_user = """ CREATE table `user` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pseudo VARCHAR(100) NOT NULL,
    mail VARCHAR(300) NOT NULL,
    password VARCHAR(100) NOT NULL);"""

sql_codelist = """CREATE table `codelist` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    code_id INT NOT NULL,
    status BOOLEAN NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (code_id) REFERENCES code(id));"""

cursor.execute(sql_delete_codeList)
cursor.execute(sql_delete_code)
cursor.execute(sql_delete_user)
cursor.execute(sql_code)
cursor.execute(sql_user)
cursor.execute(sql_codelist)