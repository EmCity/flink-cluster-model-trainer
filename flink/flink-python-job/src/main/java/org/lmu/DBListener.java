package org.lmu;

import com.mongodb.*;
import com.mongodb.util.JSON;
import org.bson.types.BSONTimestamp;
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
                .addOption(Bytes.QUERYOPTION_TAILABLE | Bytes.QUERYOPTION_AWAITDATA);

        JSONParser parser = new JSONParser();

        //db listener thread
        Runnable task = () -> {
            System.out.println("\tWaiting for events");
                while (cur.hasNext()) {
                    DBObject obj = cur.next();
                    String json = JSON.serialize(obj);
                    JSONObject jsonObj = null;
                    try{
                        jsonObj = (JSONObject) parser.parse(json);
                    }
                    catch(Exception e){
                    }
                    if(jsonObj != null){
                        queue.add(jsonObj);
                    }
                }
            };
        new Thread(task).start();

        //flink thread
        RunCMD2 flink = new RunCMD2();
        Runnable task1 = () -> {
           while(true){
               try{
                    flink.distribute(queue.poll());
               }
               catch(Exception e){

               }
           }
        };

        new Thread(task1).start();
    }
}
