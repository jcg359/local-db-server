/**
 * Named query definitions.
 * Each entry maps a dataset name to a connection name and SQL query.
 *
 * connection: must match a key in config/connections.js
 * sql:        the query to execute (no parameters for now)
 */
module.exports = {

  holiday_gifts_users: {
    connection: 'holiday_gifts_mssql',
    sql: 'SELECT * FROM dbo.UserPrincipal',
  },

  giftsdb_users: {
    connection: 'holiday_gifts_mysql',
    sql: 'SELECT * FROM UserPrincipal',
  },
};
