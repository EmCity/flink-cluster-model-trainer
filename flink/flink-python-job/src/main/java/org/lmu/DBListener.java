package org.lmu;

import com.mongodb.*;
import com.mongodb.util.JSON;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.JSONParser;
import java.util.concurrent.LinkedBlockingQueue;

public class DBListener {

    public static void main(String[] args) throws Exception{
        //connect to DB
        MongoClient mongoClient = new MongoClient("sambahost.dyndns.lrz.de", 27017);
        DBCollection coll = mongoClient.getDB("samba").getCollection("jobs");

        //list for the jobs
        LinkedBlockingQueue<JSONObject> queue = new LinkedBlockingQueue<>();

        //db listener
        DBCursor cur = coll.find().sort(BasicDBObjectBuilder.start("$natural", 1).get())
                .addOption(Bytes.QUERYOPTION_TAILABLE | Bytes.QUERYOPTION_AWAITDATA | Bytes.QUERYOPTION_NOTIMEOUT);

        JSONParser parser = new JSONParser();

        //db listener thread
        //TODO: fix that only new elements are added to queue
        Runnable task = () -> {
            System.out.println("\tWaiting for events");
                while (cur.hasNext()) {
                    DBObject obj = cur.next();
                    String json = JSON.serialize(obj);
                    JSONObject jsonObj = null;
                    try{
                        jsonObj = (JSONObject) parser.parse(json);
                        System.out.println("New Entry" + jsonObj.toJSONString());
                        if(jsonObj != null){
                            queue.add(jsonObj);
                        }
                    }
                    catch(Exception e){
                        System.out.println(e);
                    }

                }
            };
        new Thread(task).start();

        //flink thread
        FlinkJobDistribution flink = new FlinkJobDistribution();
        Runnable task1 = () -> {
            try {
                while (true) {
                    if (!queue.isEmpty()) {
                        JSONObject obj = queue.poll();
                        System.out.println("New Job" + obj.toJSONString());
                        flink.distribute(obj);
                    } else {
                        Thread.currentThread().sleep(1000);
                    }
                }
            }
            catch(Exception e){
                //System.out.println(e);
            }
        };
        new Thread(task1).start();
    }
}
