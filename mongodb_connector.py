import pymongo

class dbHandler:

    # connect to database
    def __init__(self):
        print("Connecting to database...")
        client = pymongo.MongoClient("mongodb+srv://SSG:Pipeline123@cluster0-rjugd.mongodb.net/test?retryWrites=true")
        #client = pymongo.MongoClient("mongodb://SSG:Pipeline123@cluster0-rjugd.mongodb.net/test?retryWrites=true")
        db = client.get_database("user_stats")
        self.client = client
        self.db = db
        self.sentence_collection = self.db.get_collection("sentences")
        self.word_collection = self.db.get_collection("words")
        print("Database successfully connected!")

    # need to reconnect to db for some reason (example lost connection)
    def connectToDb(self):
        client = pymongo.MongoClient("mongodb+srv://SSG:Pipeline123@cluster0-rjugd.mongodb.net/test?retryWrites=true")
        #client = pymongo.MongoClient("mongodb://SSG:Pipeline123@cluster0-rjugd.mongodb.net/test?retryWrites=true")
        db = client.get_database("user_stats")
        self.client = client
        self.db = db
        self.sentence_collection = self.db.get_collection("sentences")
        self.word_collection = self.db.get_collection("words")

    # expects sentence in json format
    def insertSentenceToDb(self, sentence):
        try:
            print("Inserting sentence to db...")
            self.sentence_collection.insert_one(sentence)
            print("Sentence inserted!")
        except Exception as e:
            print("Error in inserting sentence - ", e)

    def closeConnection(self):
        self.client.close()

test_json = {
    "custom_id": 1,
    "sentence": "This is a test sentence"
}

# dbHandlerService = dbHandler()
# dbHandlerService.insertSentenceToDb(test_json)
# dbHandlerService.closeConnection()
