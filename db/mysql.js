const mysql = require('mysql2/promise');

async function runQuery(connectionConfig, sql) {
  const { type, ...config } = connectionConfig;
  const connection = await mysql.createConnection(config);
  try {
    const [rows] = await connection.execute(sql);
    return rows;
  } finally {
    await connection.end();
  }
}

module.exports = { runQuery };
