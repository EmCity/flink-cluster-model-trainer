import get_traffic as traffic
import pandas as pd
from datetime import datetime
import TravelTimeSubmission as submission


def from_index_to_prediction_day(day, hour, minute, endhour, endminute):
    start = datetime(2016, 10, 18 + day, hour, minute, 0)
    end = datetime(2016, 10, 18 + day, endhour, endminute, 0)
    return "[" + str(start) + "," + str(end) + ")"

#we are interested in all weekdays
weekdays = [0,1,2,3,4,5,6]

#all 20 min windows
times = [[(8,00),(8,20)],[(8,20),(8,40)],[(8,40),(9,00)],[(9,00),(9,20)],[(9,20),(9,40)],[(9,40),(10,00)],
             [(15,00),(15,20)],[(15,20),(15,40)],[(15,40),(16,00)],[(16,00),(16,20)],[(16,20),(16,40)],[(16,40),(17,00)]]

dfResult = pd.DataFrame(columns=["intersection_id", "tollgate_id","avg_travel_time", "time_window"])
for day in weekdays:
    for h in times:
        df = traffic.get_traffic([day], (h[0], h[1]))
        df3 = df.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
        df5 = pd.DataFrame(df3, columns=["intersection_id", "tollgate_id","avg_travel_time", "time_window"])
        df5["time_window"] = from_index_to_prediction_day(day, h[0][0], h[0][1], h[1][0], h[1][1])
        dfResult = pd.concat([dfResult, df5])
dfResult = dfResult[["intersection_id", "tollgate_id", "time_window", "avg_travel_time"]]
print(dfResult)
submission.TravelTimeSubmission.save_df_travel_time_submission(submission.TravelTimeSubmission, df5)


