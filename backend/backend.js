var express = require('express');
var child = require('child_process');
var app = express();
var path = require('path');
var bodyParser = require('body-parser');

app.set('views', path.join(__dirname, '/../gui/src'));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use('/',express.static(path.join(__dirname, '/../gui/src/public/')));
app.use('/',express.static(path.join(__dirname, '/../gui/src/')));
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));


const hostname = 'sambahost.dyndns.lrz.de';
const port = 8500;
/*
const hostname = 'localhost';
const port = 8500;
*/

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://sambauser:teamsamba@sambahost.dyndns.lrz.de:27017/samba";

// CORS
app.all('/', function(req, res, next) {
    console.log('CORS');
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    next();
 });

app.get('/', function(req, res) {
  console.log('a');
  res.render("index");
});

app.get('/results', function(req, res) {
  res.render("results");
});

app.get('/results', function(req, res) { 
  res.render("results"); 
}); 

// save AlgoParaImputs
app.post('/api/',(req, res) => {
  data = req.body;

  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    db.collection("jobs").insertOne(data);
    db.collection("jobs").find().sort({timestart:-1},function(err,cursor){});
    db.close();
    callFlink(data.job_name, function(msg) {
    	console.log(msg);
    });

    res.send(req.body);
  });
});

// save AlgoParaImputs
app.get('/start_job/:job_name', (req, res) => {
    console.log(req.params.job_name);
    callFlink(req.params.job_name, function(javaOut){
        res.send(javaOut);
    });
    console.log("Started flink job.")
});

function callFlink (jobname, func) {
    child.exec('/root/flink-1.3.0/bin/flink run -c org.lmu.JobNameBatchDB ' +
        '/root/code/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar' + ' ' + jobname, (error, stdout, stderr) =>{
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
      console.log(`stderr: ${stderr}`);
      if (stderr) func(stderr);

      func(stdout);
    });
}

// get results
app.get('/get_results/', (req, res) => {
  try{
    MongoClient.connect(url, function(err, db) {
        if (err) {
            console.error(`exec error: ${err}`);
            res.send(JSON.stringify("{error:\"Database query error\"}") );
            return;
        }

        var coll = db.collection('results');
        cursor = coll.find({});
        cursor.toArray(function(err, result){
               res.render("results",{ data: JSON.stringify(result) });
    });
    db.close();
  });
  }catch(err){
    console.log('Error has occured!', error);
  }
});

// get results rest api
app.get('/get_results_api/', (req, res) => {
  try{
  MongoClient.connect(url, function(err, db) {
      if (err) {
        console.error(`exec error: ${err}`);
        res.send(JSON.stringify("{error:\"Database query error\"}") );
        return;
      }
      var coll = db.collection('results');
      cursor = coll.find({});
      cursor.toArray(function(err, result){
        res.send(JSON.stringify(result) );
      });
      db.close();
  });
  }catch(err){
    console.error('Error has occured!', err);
    res.send(JSON.stringify("{error:\"Database connect error\"}") );
  }
});

// get results rest api
app.get('/get_jobs_api/', (req, res) => {
  try{
  MongoClient.connect(url, function(err, db) {
      if (err) {
        console.error(`exec error: ${err}`);
        res.send(JSON.stringify("{error:\"Database query error\"}") );
        return;
      }
      var coll = db.collection('jobs');
      cursor = coll.find({});
      cursor.toArray(function(err, result){
        res.send(JSON.stringify(result) );
      });
      db.close();
  });
  }catch(err){
    console.error('Error has occured!', err);
    res.send(JSON.stringify("{error:\"Database connect error\"}") );
  }
});

app.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});