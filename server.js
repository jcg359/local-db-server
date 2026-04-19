require('dotenv').config();
const express = require('express');
const connections = require('./config/connections');
const queries = require('./config/queries');
const mysqlRunner = require('./db/mysql');
const mssqlRunner = require('./db/mssql');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/datasets/:name', async (req, res) => {
  const { name } = req.params;

  const queryDef = queries[name];
  if (!queryDef) {
    return res.status(404).json({ error: `Dataset '${name}' not found` });
  }

  const connectionConfig = connections[queryDef.connection];
  if (!connectionConfig) {
    return res.status(500).json({ error: `Connection '${queryDef.connection}' not configured` });
  }

  try {
    let results;
    if (connectionConfig.type === 'mysql') {
      results = await mysqlRunner.runQuery(connectionConfig, queryDef.sql);
    } else if (connectionConfig.type === 'mssql') {
      results = await mssqlRunner.runQuery(connectionConfig, queryDef.sql);
    } else {
      return res.status(500).json({ error: `Unsupported connection type '${connectionConfig.type}'` });
    }

    res.json({ results });
  } catch (err) {
    console.error(`Error executing dataset '${name}':`, err.message);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
