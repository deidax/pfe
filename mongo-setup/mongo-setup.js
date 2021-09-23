rsconf = {
    _id : "rsmongo",
    members: [
        {
            "_id": 0,
            "host": "mongodb:27017",
            "priority": 4
        },
        {
            "_id": 1,
            "host": "mongodb1:27017",
            "priority": 2
        },
        {
            "_id": 2,
            "host": "mongodb2:27017",
            "priority": 1
        }
    ]
 }

rs.initiate(rsconf);