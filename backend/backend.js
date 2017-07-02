var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.json()); // add a middleware (so that express can parse request.body's json)
const hostname = 'sambahost.dyndns.lrz.de';
const port = 8500;
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/samba";
var path = require('path');

app.get('/', function(req, res) {
  //res.sendFile(path.join(__dirname + '../gui/src/index.html'));
  res.sendFile('/root/code/sose17-small-data/gui/src/index.html') 
});

// save AlgoParaImputs
app.post('/api/', (req, res) => {
  console.log(typeof(req))
  console.log(req.body)
  data = req.body;

  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    db.collection("jobs").insertOne(data);
    db.collection("jobs").find().sort({timestart:-1},function(err,cursor){});
    db.close();
  });
    res.send(req.body);
});

// not in use
app.post('/save_result/', (req, res) => {
  console.log(typeof(req))
  console.log(req.body)
  data = req.body;

  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    // TODO db.collection("results").insertOne(data);
    db.close();
  });
    //res.send(req.body);
    res.send('ok-....'+ req.body);
});
// get results
app.get('/get_results/', (req, res) => {
  var x = "";  
  MongoClient.connect(url, function(err, db) {
      var col = db.collection('results');
      x += "error: " + err + "<br>";
      
      var cursor =  col.find({});
      cursor.toArray(function(err, result){
          x = result;
          res.send(x);   
          console.log(result);

          db.close();
      });

    });
});


app.post('/test/', function (req, res) {
    console.log('works');
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

