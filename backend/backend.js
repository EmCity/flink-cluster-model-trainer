var express = require('express');
var child = require('child_process');
var app = express();
const hostname = 'sambahost.dyndns.lrz.de';
const port = 8500;
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://sambauser:teamsamba@sambahost.dyndns.lrz.de:27017/samba";
var path = require('path');
var bodyParser = require('body-parser');

app.set('views', path.join(__dirname, '/../gui/src/views'));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use('/',express.static(path.join(__dirname, '/../gui/src/public/')));


app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

app.get('/', function(req, res) {
  //console.log('Limit file size: '+limit);
  res.render("index")
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
      if (error) {
        console.error(`exec error: ${error}`);
        //res.send(JSON.stringify("{error:\"Database query error\"}") );
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
    console.log('Error has occured!', error);
    //res.send(JSON.stringify("{error:\"Database connect error\"}") );
  }
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

// var Grid = require('mongodb').Grid;
// var GridStore = require('mongodb').GridStore;
// function saveCsvToMongo(db, csv){
//     var grid = new Grid(db,'fs');
//     var buffer = new Buffer(csv);
//         grid.get(fileInfo._id, function(err, data){ontent_type: 'text'}, functio$
//   console.log(`stderr: ${stderr}`);
//             if (err) throw err;
//             console.log("Retrieved data: " + data.toString());
//         });
//     });
// }
