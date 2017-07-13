package org.lmu;

import com.mongodb.*;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.util.Collector;
import org.apache.log4j.varia.NullAppender;

import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.JSONParser;
import org.lmu.JSON.parser.ParseException;
import java.util.Arrays;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

public final class FlinkJobDistribution {
    private final static String DBNAME = "samba";
    private final static String COLLECTION = "jobs";
    private final static MongoCredential CREDENTIALS = MongoCredential.createMongoCRCredential("sambauser",DBNAME, "teamsamba".toCharArray());
    private final static String URL = "sambahost.dyndns.lrz.de";
    private final static int PORT = 27017;

    public JSONObject getJobJSONObject(String jobName) throws UnknownHostException, ParseException {
	    MongoClient mongoClient = new MongoClient(new ServerAddress(URL, PORT), Arrays.asList(CREDENTIALS));
        DBCollection coll = mongoClient.getDB(DBNAME).getCollection(COLLECTION);
        BasicDBObject query = new BasicDBObject("job_name", jobName);

        DBCursor cursor = coll.find(query);
        if(cursor== null){
            return null;
        }

        BasicDBObject job = null;
        try{
            while(cursor.hasNext()){
                job = (BasicDBObject) cursor.next();
            }
        } finally{
            cursor.close();
        }
        if(job == null){
            System.out.println("Query: " + query + " found nothing");
        }
        mongoClient.close();
        return (JSONObject) new JSONParser().parse(job.toString());
    }

    public void saveResultJSONObjectToMongoDB(JSONObject jsonObject) throws UnknownHostException {
	    MongoClient mongoClient = new MongoClient(new ServerAddress(URL, PORT), Arrays.asList(CREDENTIALS));
	    DBCollection coll = mongoClient.getDB(DBNAME).getCollection(COLLECTION);
	    DBObject b = (DBObject)com.mongodb.util.JSON.parse(jsonObject.toString()) ;
        System.out.println("Object: " + b);
        coll.insert(b);
        mongoClient.close();
    }

    public JSONObject getBestMapeJsonObject(JSONArray resultsJSONArray){
        double bestmape = 420;
        JSONObject bestJsonObject = new JSONObject();
        for (Object o: resultsJSONArray) {
            JSONObject jsonObject = (JSONObject) o;
            double mape = (double)jsonObject.get("mape");
            if(bestmape > mape){
                bestmape = mape;
                bestJsonObject = jsonObject;
            }
        }
        return bestJsonObject;
    }

    public static JSONArray distribute(JSONObject json) throws Exception {
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        JSONObject algorithms = (JSONObject) json.get("algorithms");
        JSONObject svm = (JSONObject) algorithms.get("SVM");
        JSONObject lr = (JSONObject) algorithms.get("LR");
        JSONObject nn = (JSONObject) algorithms.get("NN");

        String jobName = json.get("job_name").toString();
        System.out.println("FlinkJobDistribution: Job: " + jobName);
        //TODO env.createProgramPlan(jobName);

        JSONArray svmArray = svm != null ? createSVMJobs(svm) : new JSONArray();
        JSONArray lrArray = lr != null ? createLRJobs(lr) : new JSONArray();
        JSONArray nnArray = nn != null ? createNNJobs(nn) : new JSONArray();

        // get input data
        ArrayList<String> tasks = new ArrayList<>();
        fillList(json, svmArray, tasks);
        fillList(json, lrArray, tasks);
        fillList(json, nnArray, tasks);

        System.out.println("FlinkJobDistripbution: Distribute: " + tasks.size() + " jobs on the workers:");
        DataSet<String> dataset = env.fromCollection(tasks).flatMap(new OnWorkers());

        JSONArray resJsonArray = new JSONArray();
        JSONParser parser = new JSONParser();
        for (String s : dataset.collect()) {
            System.out.print(s);
            resJsonArray.add(parser.parse(s));
        }
        return resJsonArray;
    }

    private static void fillList(JSONObject json, JSONArray array, ArrayList<String> tasks) {
        for (Object obj : array) {
            obj = new JSONObject((JSONObject) obj);
            ((JSONObject) obj).put("job_name", json.get("job_name"));
            tasks.add(((JSONObject) obj).toJSONString());
        }
    }

    private static JSONArray createSVMJobs(JSONObject svm) throws Exception{
        JSONArray c_array = (JSONArray) svm.get("C");
        JSONArray e_array = (JSONArray) svm.get("epsilon");
        JSONArray kernel_array = (JSONArray) svm.get("kernel");
        JSONArray gamma_array = (JSONArray) svm.get("gamma");

        JSONArray result = new JSONArray();
        if(c_array != null & e_array != null & kernel_array != null & gamma_array != null) {
            for (Object c : c_array) {
                for (Object e : e_array) {
                    for (Object kernel : kernel_array) {
                        for (Object gamma : gamma_array) {
                            JSONObject obj = new JSONObject();
                            obj.put("algorithm", "SVM");
                            obj.put("C", Double.parseDouble(c.toString()));
                            obj.put("epsilon", Double.parseDouble(e.toString()));
                            obj.put("kernel", kernel);
                            obj.put("gamma", Double.parseDouble(gamma.toString()));
                            obj.put("shrinking", svm.get("shrinking"));
                            obj.put("tolerance", Double.parseDouble(svm.get("tolerance").toString()));
                            obj.put("cache_size", Double.parseDouble(svm.get("cache_size").toString()));
                            obj.put("max_iter", Integer.parseInt(svm.get("max_iter").toString()));
                            result.add(obj);
                        }
                    }
                }
            }
        }
        else{
            throw new Exception("SVM-ARRAYS NULL");
        }
        return result;
    }

    private static JSONArray createLRJobs(JSONObject lr) {
        Boolean normalize = (Boolean)lr.get("normalize");
        Boolean fit_intercept = (Boolean)lr.get("fit_intercept");
        JSONArray result = new JSONArray();
        JSONObject obj = new JSONObject();
        obj.put("algorithm", "LR");
        obj.put("normalize", normalize);
        obj.put("fit_intercept", fit_intercept);
        result.add(obj);
        return result;
    }

    private static JSONArray createNNJobs(JSONObject nn) throws Exception {
        JSONArray learningRates = (JSONArray) nn.get("learning_rate");
        JSONArray epochs = (JSONArray) nn.get("epochs");
        JSONArray costFunctions = (JSONArray) nn.get("cost_function");
        JSONArray result = new JSONArray();
        if(learningRates != null & epochs != null & costFunctions != null) {
            for (Object learningRate : learningRates) {
                for (Object epoch : epochs) {
                    for (Object costFunction : costFunctions) {
                        JSONObject obj = new JSONObject();
                        obj.put("algorithm", "NN");
                        obj.put("normalization", nn.get("normalization"));
                        obj.put("learning_rate", Double.parseDouble(learningRate.toString()));
                        obj.put("epochs", Integer.parseInt(epoch.toString()));
                        obj.put("cost_function", costFunction);
                        result.add(obj);
                    }
                }
            }
        }
        else{
            throw new Exception("NN-ARRAYS NULL");
        }
        return result;
    }

    public static final class OnWorkers implements FlatMapFunction<String, String> {
        public static final long serialVersionUID = 1L;

        @Override
        public void flatMap(String value, final Collector<String> out) {
            String res = "";
            try {
                String pythonPath = "/root/anaconda/envs/dataScience/bin/python3";
                String trainModelPath = "/root/code/sose17-small-data/python/traffic-prediction/src/flink/trainModel.py";
                Process proc = Runtime.getRuntime().exec(pythonPath + " "  + trainModelPath + " " + value);
                BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
                BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));
                String s;

                while ((s = stdInput.readLine()) != null) {
                    res += "\n" + s;
                }

                // read any errors from the attempted command
                while ((s = stdError.readLine()) != null) {
                    res += "\n" + s;
                }
            } catch (Exception e) {
                res += e.toString();
            }
            out.collect(res);
        }
    }
}
