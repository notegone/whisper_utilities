import whisper
import json
import os
import pymongo

username = "mongo-admin"
password = "password"
DB_NAME = "shinzen"
DB_COLLECTION = "expandcontract"

#myclient = pymongo.MongoClient('mongodb://%s:%s@172.105.107.170:27017' % (username, password))
#dblist = myclient.list_database_names()

#print(myclient.list_database_names())
#mydb = myclient["shinzen"]
#mycol = mydb["expandcontract"]

#if "shinzen" in dblist:
#  print("The database exists.")
#else:
#  print("The database does not exists.")

def transcribe(audio_file,model):
    model = whisper.load_model(model)
    result = model.transcribe(audio_file)
    return result

def write_to_json(result, file):
    with open(file+".json", 'w') as f:
        json.dump(result, f)

def main():
    # loop through files in folder and run transcribe
    for file in os.listdir("audio"):
        if file.endswith(".mp3"):
            print(file)
            result = transcribe("audio/"+file,"large")
            print(result)
            write_to_json(result, "transcribe/"+file)
 #           mycol.replace_one(result, result, upsert=True)

if __name__ == "__main__":
    main()
