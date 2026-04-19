import pymysql
import pymysql.cursors

def run_query(conn_config, sql):
    connection = pymysql.connect(
        host=conn_config['host'],
        port=conn_config['port'],
        database=conn_config['database'],
        user=conn_config['user'],
        password=conn_config['password'],
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()
