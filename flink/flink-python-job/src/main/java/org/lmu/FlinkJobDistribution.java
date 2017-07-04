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

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

public class FlinkJobDistribution {

    public JSONObject getJobJSONObject(String jobName) throws UnknownHostException, ParseException {
        MongoClient mongoClient = new MongoClient("sambahost.dyndns.lrz.de", 27017);
        DBCollection coll = mongoClient.getDB("samba").getCollection("jobs");

        BasicDBObject query = new BasicDBObject("job_name", jobName);

        DBCursor cursor = coll.find(query);
        if(cursor== null){
            //System.out.println("Problem with Database");
            return null;
        }

        BasicDBObject job = null;
        try{
            while(cursor.hasNext()){
                job = (BasicDBObject) cursor.next();
                //System.out.println(job);

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
        MongoClient mongoClient = new MongoClient("sambahost.dyndns.lrz.de", 27017);
        DBCollection coll = mongoClient.getDB("samba").getCollection("results");

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
        // set up the batch execution environment
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().disableSysoutLogging();
        org.apache.log4j.BasicConfigurator.configure(new NullAppender());

        JSONObject algorithms = (JSONObject) json.get("algorithms");
        JSONObject data = (JSONObject) json.get("data");
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
        //for (String task: tasks) {
            //System.out.println("FlinkJobDistribution: Do Task" +  task);
        //}

        DataSet<String> elementsDataSet = env.fromCollection(tasks);

        //distribute on workers
        DataSet<String> dataset = elementsDataSet.flatMap(new OnWorkers());

        System.out.println("collect");
        List<String> res = dataset.collect();

        JSONArray resJsonArray = new JSONArray();
        JSONParser parser = new JSONParser();
        for (String s : res) {
            System.out.print(s);
            resJsonArray.add(parser.parse(s));
        }



        //saves the result as text
        //dataset.writeAsText("result.txt", FileSystem.WriteMode.OVERWRITE);
        //dataset.print();

        return resJsonArray;
    }

    private static void fillList(JSONObject json, JSONArray array, ArrayList<String> tasks) {
        for (Object obj : array) {
            obj = new JSONObject((JSONObject) obj);
            ((JSONObject) obj).put("job_name", json.get("job_name"));
            //((JSONObject) obj).put("data", data);
            tasks.add(((JSONObject) obj).toJSONString());
        }
    }

    private static JSONArray createSVMJobs(JSONObject svm) {
        JSONArray c_array = (JSONArray) svm.get("C");
        JSONArray e_array = (JSONArray) svm.get("epsilon");
        JSONArray kernel_array = (JSONArray) svm.get("kernel");
        JSONArray degree_array = (JSONArray) svm.get("degree");
        JSONArray gamma_array = (JSONArray) svm.get("gamma");
        JSONArray coef_array = (JSONArray) svm.get("coef0");
        Boolean shrinking = (Boolean)svm.get("shrinking");
        Double tol = (Double) svm.get("tol");
        Long cache_size = (Long) svm.get("cache_size");
        Integer max_iter = Math.toIntExact((long)svm.get("max_iter"));



        JSONArray result = new JSONArray();
        if(c_array != null & e_array != null & kernel_array != null & degree_array != null & gamma_array != null & coef_array != null) {
            for (Object c : c_array) {
                for (Object e : e_array) {
                    for (Object kernel : kernel_array) {
                        for (Object degree : degree_array) {
                            for (Object gamma : gamma_array) {
                                for (Object coef0 : coef_array) {
                                    JSONObject obj = new JSONObject();
                                    obj.put("algorithm", "SVM");
                                    obj.put("C", c);
                                    obj.put("epsilon", e);
                                    obj.put("kernel", kernel);
                                    obj.put("degree", degree);
                                    obj.put("gamma", gamma);
                                    obj.put("coef0", coef0);
                                    obj.put("shrinking", shrinking);
                                    obj.put("tol", tol);
                                    obj.put("cache_size", cache_size);
                                    obj.put("max_iter", max_iter);
                                    result.add(obj);
                                }
                            }
                        }
                    }
                }
            }
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

    private static JSONArray createNNJobs(JSONObject nn) {
        return new JSONArray();
    }

    public static final class OnWorkers implements FlatMapFunction<String, String> {
        /**
         * serial uid.
         */
        public static final long serialVersionUID = 1L;

        @Override
        public void flatMap(String value, final Collector<String> out) {

            String res = "";
            try {
                Runtime rt = Runtime.getRuntime();


                String cmd;
                String pythonPath;

                String os = System.getProperty("os.name").toLowerCase();
                if(os.equals("windows 10")){
                    //rt.exec("activate dataScience");
                    cmd = "python3";
                    pythonPath = "../../../sose17-small-data/python/traffic-prediction/src/flink/trainModel.py";
                }
                else{
                    rt.exec("source activate dataScience");
                    cmd = "python3";
                    pythonPath = "~/code/sose17-small-data/python/traffic-prediction/src/flink/trainModel.py";
                }


                //TODO cl
                //cmd = "/home/l/lemkec/anaconda3/bin/python";
                // TODO cl
                //pythonPath = "/home/l/lemkec/BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/trainModel.py";


                //Process proc = rt.exec(new String[]{cmd, pythonPath, value});
                //TODO ... cmd
                Process proc = rt.exec(cmd + " "  + pythonPath + " " + value);

                BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
                BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

                String s = null;
                while ((s = stdInput.readLine()) != null) {

                    res += "\n" + s;
                }

                // read any errors from the attempted command
                //System.out.println("----Here is the standard error of the command (if any):\n");
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
