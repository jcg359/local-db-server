import os

connections = {
    'holiday_gifts_mysql': {
        'type': 'mysql',
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', '3306')),
        'database': os.getenv('MYSQL_DATABASE'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
    },
    'holiday_gifts_mssql': {
        'type': 'mssql',
        'server': os.getenv('MSSQL_HOST'),
        'port': 1433,
        'database': os.getenv('MSSQL_DATABASE'),
        'user': os.getenv('MSSQL_USER'),
        'password': os.getenv('MSSQL_PASSWORD'),
    },
}
