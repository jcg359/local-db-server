const sql = require('mssql');

async function runQuery(connectionConfig, query) {
  const { type, server, port, database, user, password, options } = connectionConfig;

  const config = {
    server,
    port,
    database,
    user,
    password,
    options: options || {},
  };

  const pool = await sql.connect(config);
  try {
    const result = await pool.request().query(query);
    return result.recordset;
  } finally {
    await pool.close();
  }
}

module.exports = { runQuery };
