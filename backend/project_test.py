def start_prediction():

    data = {"data":"dataset"}
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.samba
    db.jobs.insert(data)
    return data
