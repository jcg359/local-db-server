import pymssql

def run_query(conn_config, sql):
    connection = pymssql.connect(
        server=conn_config['server'],
        port=conn_config['port'],
        database=conn_config['database'],
        user=conn_config['user'],
        password=conn_config['password'],
    )
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        connection.close()
