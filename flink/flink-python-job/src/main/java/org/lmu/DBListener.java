package org.lmu;

import com.mongodb.BasicDBObjectBuilder;
import com.mongodb.Bytes;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.util.JSON;
import org.json.simple.parser.JSONParser;
import org.json.simple.JSONObject;

import java.util.concurrent.LinkedBlockingQueue;

/**
 * DBListener for listening to the mongo DB.
 */
public final class DBListener {
    /**
     * port of the DB.
     */
    public static final int PORT = 27017;
    /**
     * private constructor.
     */
    private DBListener() { }

    /**
     * entry point for the DB listener.
     * @param args arguments for the DB listener.
     * @throws Exception if db is unknown.
     */
    public static void main(final String[] args) throws Exception {
        //connect to DB
        MongoClient mongoClient = new MongoClient("sambauser:teamsamba@sambahost.dyndns.lrz.de/"
                        + "?authSource=db1&authMechanism=MONGODB-CR", PORT);
        DBCollection coll = mongoClient.getDB("samba").getCollection("jobs");
        //list for the jobs
        LinkedBlockingQueue<JSONObject> queue = new LinkedBlockingQueue<>();
        //db listener
        DBCursor cur = coll.find().sort(BasicDBObjectBuilder.
                start("$natural", 1).get()).addOption(Bytes.QUERYOPTION_TAILABLE
                | Bytes.QUERYOPTION_AWAITDATA | Bytes.QUERYOPTION_NOTIMEOUT);
        JSONParser parser = new JSONParser();
        Runnable task = () -> {
            System.out.println("\tWaiting for events");
            while (cur.hasNext()) {
                DBObject obj = cur.next();
                String json = JSON.serialize(obj);
                JSONObject jsonObj;
                try {
                    jsonObj = (JSONObject) parser.parse(json);
                    System.out.println("New Entry" + jsonObj.toJSONString());
                    queue.add(jsonObj);
                } catch (Exception e) {
                    System.out.println(e.toString());
                }
            }
        };
        new Thread(task).start();

        Runnable task1 = () -> {
                while (true) {
                    if (!queue.isEmpty()) {
                        JSONObject obj = queue.poll();
                        System.out.println("New Job" + obj.toJSONString());
                        try {
                            FlinkJobDistribution flink = new FlinkJobDistribution();
                            flink.distribute(obj);
                        } catch (Exception e) {
                            System.out.println(e.toString());
                        }
                    }
                }
        };
        new Thread(task1).start();
    }
}
