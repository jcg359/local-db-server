/**
 * Named database connections.
 * Passwords are read from environment variables.
 * Supported types: 'mysql', 'mssql'
 */
module.exports = {
  holiday_gifts_mysql: {
    type: 'mysql',
    host: process.env.MYSQL_HOST,
    port: parseInt(process.env.MYSQL_PORT || '3306', 10),
    database: process.env.MYSQL_DATABASE,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
  },

  holiday_gifts_mssql: {
    type: 'mssql',
    server: process.env.MSSQL_HOST,
    port: 1433,
    database: process.env.MSSQL_DATABASE,
    user: process.env.MSSQL_USER,
    password: process.env.MSSQL_PASSWORD,
    options: {
      encrypt: true,
      trustServerCertificate: false,
    },
  },
};
