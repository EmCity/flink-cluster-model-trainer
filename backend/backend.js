var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.json()); // add a middleware (so that express can parse request.body's json)
const hostname = 'sambahost.dyndns.lrz.de';
const port = 8500;
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/samba";



app.post('/api/', (req, res) => {
  console.log(typeof(req))
  console.log(req.body)
  data = req.body;

  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    db.collection("jobs").insertOne(data);
    db.close();
  });
    res.send(req.body);
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
