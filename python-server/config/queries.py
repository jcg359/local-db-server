queries = {
    'holiday_gifts_users': {
        'connection': 'holiday_gifts_mssql',
        'sql': 'SELECT * FROM dbo.UserPrincipal',
    },
    'giftsdb_users': {
        'connection': 'holiday_gifts_mysql',
        'sql': 'SELECT * FROM UserPrincipal',
    },
}
