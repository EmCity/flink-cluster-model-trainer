package org.lmu;

import com.mongodb.*;
import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.JSONParser;

import java.io.FileReader;
import java.util.List;

/**
 * Created by lemkec on 6/30/17.
 *
 * Call:
 * flink-1.3.0/bin/flink run -c org.lmu.JobNameBatchDB BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar TestJob42
 *
 */
public class JobNameBatchDB {

    public static void main(String[] args) throws Exception {

        String jobName = "";
        if (args.length > 0 && args[0] != null) {
            jobName = args[0];
            System.out.println("Got JobName: " + jobName);
        } else {
            throw new Exception("check args parameters: " + args);
        }

        /*
        String testjsonFile = "./BigDataScience/sose17-small-data/flink/flink-python-job/src/main/java/org/lmu/JobDef.json";
        JSONObject jobsjson;
        jobsjson = (JSONObject) new JSONParser().parse(new FileReader(testjsonFile));
        */

        //JSONObject jobsjson = (JSONObject) new JSONParser().parse(obj.toString());

        JSONObject jobsjson;

        //flink
        FlinkJobDistribution flinkdistribute = new FlinkJobDistribution();
        jobsjson = flinkdistribute.getJobJSONObject(jobName);
        System.out.println("MONGO: " + jobsjson.toString());


        JSONArray resCollect = flinkdistribute.distribute(jobsjson);

        // create result

        // result json
        for (Object t: resCollect.toArray()) {
            JSONObject jo = (JSONObject)t;
            System.out.println(jo.toString());

        }

        JSONObject bestResultJosnObject = flinkdistribute.getBestMapeJsonObject(resCollect);
        System.out.println("BEST: " + bestResultJosnObject.toString());



        // set status
        System.out.println("Save best result with status Finished" );
        bestResultJosnObject.put("status", "Finished");
        flinkdistribute.saveResultJSONObjectToMongoDB(bestResultJosnObject);

    }


}
