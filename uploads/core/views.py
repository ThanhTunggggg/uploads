from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.forms import ContactForm

import os
import json
from collections import OrderedDict

import paho.mqtt.client as mqtt


def simple_upload(request):

    if request.method == 'GET':
        form = ContactForm()

    else:
        form = ContactForm(request.POST)
        
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            filename = uploaded_file_url.split("/")[-1]
            cmd = "cd media \nmrz --json " + filename + " > " + filename +".json"
            os.system(cmd)
            with open("media/" +filename+ ".json") as json_file:
               json_data = json.load(json_file, object_pairs_hook=OrderedDict)
               #print(json_data)
            if json_data["mrz_type"] != None:
                form = ContactForm(initial = json_data) #{"name":json_data["names"], "country":json_data["country"], "date_of_birth" :json_data["date_of_birth"]})
            #print(form)
            send_json_over_mqtt(json_data)
            return render(request, 'core/simple_upload.html', {'uploaded_file_url': uploaded_file_url, 'form': form})
    return render(request, 'core/simple_upload.html', {'form': form})

def correct_json(json_data):
    result = "{\"respcode\":0,\"errorDesc\":\"\",\"data\":[{\n"
    for key, val in json_data.items():
        if key == "valid_score":
            result = result + "  \"{0}\": {1}, \n".format(key, val)
        elif key.startswith("valid"):
            if val:
                result = result + "  \"{0}\": true, \n".format(key)
            else:
                result = result + "  \"{0}\": false, \n".format(key)
        elif key == "date_of_birth":
            tmp = "{0}-{1}-19{2}".format(val[2:4], val[4:6], val[0:2])
            result = result + "  \"{0}\": \"{1}\", \n".format(key, tmp)
        elif key == "walltime":
            result = result + "  \"{0}\": {1}, \n".format(key, val)
        elif key == "sex":
            if val == "F":
                result = result + "  \"{0}\": \"Female\", \n".format(key)
            else:
                result = result + "  \"{0}\": \"Male\", \n".format(key)
        elif key == "filename":
            result = result + "  \"{0}\": \"{1}\" \n".format(key, val) 
        else:
            result = result + "  \"{0}\": \"{1}\", \n".format(key, val) 
    result = result + "}]}"
    return result

def fill_json(json_data):
    if json_data["mrz_type"] != None:
        result = "{\"respcode\":0,\"errorDesc\":\"\",\"data\":[{\n" +\
                "  \"mrz_type\": \"TD3\", \n" +\
                "  \"valid_score\": 100, \n" +\
                "  \"type\": \"P<\", \n" +\
                "  \"country\": \"RUS\", \n"
        result += "  \"number\": \"{0}\", \n".format(json_data["number"])
        result += "  \"date_of_birth\": \"{1}-{2}-19{0}\", \n".format(*(json_data["date_of_birth"][2*i:2*i+2] for i in range(3)))
        result += "  \"expiration_date\": \"221114\", \n" +\
                "  \"nationality\": \"RUS\", \n"
        result += "  \"sex\": \"{0}\", \n".format("Female" if json_data["sex"] == "F" else "Male")
        result += "  \"names\": \"{0}\", \n".format(json_data["names"])
        result += "  \"surname\": \"{0}\", \n".format(json_data["surname"])
        result += "  \"personal_number\": \"211271<426U<<<\", \n" +\
                "  \"check_number\": \"4\", \n" +\
                "  \"check_date_of_birth\": \"4\", \n" +\
                "  \"check_ex piration_date\": \"3\", \n" +\
                "  \"check_composite\": \"4\", \n" +\
                "  \"check_personal_number\": \"0\", \n" +\
                "  \"valid_number\": true, \n" +\
                "  \"valid_date_of_birth\": true, \n" +\
                "  \"valid_expiration_date\": true, \n" +\
                "  \"valid_composite\": true, \n" +\
                "  \"valid_personal_number\": true, \n" +\
                "  \"method\": \"rescaled\", \n" +\
                "  \"walltime\": 0, \n" +\
                "  \"filename\": \"noname.jpg\"\n" +\
                "}]}"
        return result

def send_json_over_mqtt(json_data):
    topic = "/device/hungdaibang01"
    
    content = "{\"respcode\":0,\"errorDesc\":\"\",\"data\":[{\n" +\
            "  \"mrz_type\": \"TD3\", \n" +\
            "  \"valid_score\": 100, \n" +\
            "  \"type\": \"P<\", \n" +\
            "  \"country\": \"RUS\", \n" +\
            "  \"number\": \"XP8271602\", \n" +\
            "  \"date_of_birth\": \"12-21-1971\", \n" +\
            "  \"expiration_date\": \"221114\", \n" +\
            "  \"nationality\": \"RUS\", \n" +\
            "  \"sex\": \"Male\", \n" +\
            "  \"names\": \"HOANG\", \n" +\
            "  \"surname\": \"MARIA OLIVIA\", \n" +\
            "  \"personal_number\": \"211271<426U<<<\", \n" +\
            "  \"check_number\": \"4\", \n" +\
            "  \"check_date_of_birth\": \"4\", \n" +\
            "  \"check_ex piration_date\": \"3\", \n" +\
            "  \"check_composite\": \"4\", \n" +\
            "  \"check_personal_number\": \"0\", \n" +\
            "  \"valid_number\": true, \n" +\
            "  \"valid_date_of_birth\": true, \n" +\
            "  \"valid_expiration_date\": true, \n" +\
            "  \"valid_composite\": true, \n" +\
            "  \"valid_personal_number\": true, \n" +\
            "  \"method\": \"rescaled(3)\", \n" +\
            "  \"walltime\": 0.7344679832458496, \n" +\
            "  \"filename\": \"743bf29d-37a8-4e44-86d5-af649e97f4ca.JPG\"\n" +\
            "}]}"
    print(content)
    print(type(content))
    content = fill_json(json_data)
    print(content)
    qos = 0
    broker = "gpay.vn"
    port = 1883
    clientId = "mqttest1"

    #content = json.dumps(json) # encode oject to JSON
    #print("\nConverting to JSON\n")
    print ("data -type ",type(content))
    #print ("data out =",content)

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        #client.subscribe("$SYS/#")

    def on_message(client, userdata, msg):
        print("message: " + msg.topic + " " + str(msg.payload))
    
    def on_publish(client,userdata,result):
        print("data published \n")

    client = mqtt.Client(client_id=clientId, protocol=mqtt.MQTTv31, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish 
    print("Connecting to broker ",broker)
    client.connect(broker,port)
    #client.loop_start()
    #client.subscribe(topic)
    #time.sleep(3)
    #print("sending data")
    client.publish(topic, payload=content, qos=qos, retain=True)
    #time.sleep(10)
    #client.loop_stop()
    client.disconnect()







