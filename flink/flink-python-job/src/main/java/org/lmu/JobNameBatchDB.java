package org.lmu;

import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;

/**
 * Created by lemkec on 6/30/17.
 * <p>
 * Call:
 * flink-1.3.0/bin/flink run -c org.lmu.JobNameBatchDB BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar TestJob42
 */
public final class JobNameBatchDB {
    /**
     * Flink entry point.
     * @param args job arguments
     * @throws Exception if json can't be parsed
     */
    public static void main(final String[] args) throws Exception {
        String jobName;
        if (args.length > 0 && args[0] != null) {
            jobName = args[0];
            System.out.println("Got JobName: " + jobName);
        } else {
            throw new Exception("check args parameters:");
        }
        FlinkJobDistribution flinkdistribute = new FlinkJobDistribution();
        JSONObject jobsjson = flinkdistribute.getJobJSONObject(jobName);
        System.out.println("JobNameBatchDB: Got json with jobname " + jobName + " from mongo.");

        JSONArray resCollect = flinkdistribute.distribute(jobsjson);
        for (Object t : resCollect.toArray()) {
            JSONObject jsonObject = (JSONObject) t;
            double mape = (double) jsonObject.get("mape");
         //   double mape_valid = (double) jsonObject.get("mape_valid")
            System.out.println("JobNameBatchDB: Results: " + jobName + " got a result with mape: " + mape);
         //   System.out.println("JobNameBatchDB: Results: " + jobName + " got a result with mape_valid: " + mape_valid);
        }
        JSONObject bestResultJosnObject = flinkdistribute.getBestMapeJsonObject(resCollect);
        System.out.println("Save best result with status Finished");
        bestResultJosnObject.put("status", "Finished");
        bestResultJosnObject.put("timestart", jobsjson.get("timestart"));
        bestResultJosnObject.put("timeend", System.currentTimeMillis());
        flinkdistribute.saveResultJSONObjectToMongoDB(bestResultJosnObject);
    }
}
