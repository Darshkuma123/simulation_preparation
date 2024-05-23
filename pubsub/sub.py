import pika as pk
import sys
import uuid
import pymongo 
from datetime import datetime
import uuid

client= pymongo.MongoClient("localhost", 27017)
network_database=client.get_database("network")
update_here=network_database['Network_values']
global i
def main():
    Connection= pk.BlockingConnection(pk.ConnectionParameters(host='localhost'))
    channel= Connection.channel()
    channel.queue_declare(queue='test')

    def callback(ch,method,properties, body):
        print(body)

    channel.basic_consume(queue='test',on_message_callback=callback)


    channel.queue_declare(queue='test2')

    channel.basic_consume(queue='test2',on_message_callback=callback)

    channel.start_consuming()

def retrive_network():
    Connection= pk.BlockingConnection(pk.ConnectionParameters(host='localhost'))
    channel= Connection.channel()
    channel.queue_declare(queue='network')
    channel.queue_declare(queue='iec61850')
    channel.basic_consume(queue='network',on_message_callback=callback)
    channel.basic_consume(queue='iec61850',on_message_callback=callback_iec61850)
    channel.start_consuming()
i=0
def callback(ch,method,properties, body):
        station_dict={}
        json_list=[]
        #print(body)
        body=str(body)
        body=body.replace('b','')
        body=body.replace('"','')
        body=body.replace('{','')
        body=body.replace('}','')
        process_input=body.split(',')
        epochtime=int(datetime.now().strftime("%s"))+1


        for p in process_input:
            json_string={
                "_id":uuid.uuid4().hex,
                "timestamp":epochtime,
                "attribute":p.split(":")[0].replace("'",'').strip(),
                "value":p.split(":")[1].strip()
            }
            json_list.append(json_string)

        update_here.insert_many(json_list)
        print(f"update value_ times")
        

        #station_dict["sample_station_"+sepochtime]=process_input
 #       print()
        # with open("output.txt",'w') as wi:
        #     wi.writelines(str(body))
        #     wi.close()
def retrive_network_iec61850():
    Connection= pk.BlockingConnection(pk.ConnectionParameters(host='localhost'))
    channel= Connection.channel()
    channel.queue_declare(queue='iec61850')
    channel.basic_consume(queue='iec61850',on_message_callback=callback_iec61850)
    channel.start_consuming()

def callback_iec61850(ch,method,properties, body):
        #print(body)
        # body=str(body)
        # body=body.replace('b','')
        # body=body.replace('"','')
        # process_input=body.split(',')
        update_here=network_database['iec61850']
        json_list=[]
        #print(body)
        body=str(body)
        body=body.replace('b','')
        body=body.replace('"','')
        body=body.replace('{','')
        body=body.replace('}','')
        process_input=body.split(',')
        epochtime=int(datetime.now().strftime("%s"))+1


        for p in process_input:
            json_string={
                "_id":uuid.uuid4().hex,
                "timestamp":epochtime,
                "attribute":p.split(":")[0].replace("'",'').strip(),
                "value":p.split(":")[1].strip()
            }
            json_list.append(json_string)

        update_here.insert_many(json_list)
        with open("output_iec61850.txt",'w') as wi:
            wi.writelines(str(body))
            wi.close()

def update():
    print("started listening")
    Connection= pk.BlockingConnection(pk.ConnectionParameters(host='localhost'))
    channel= Connection.channel()
    channel.queue_declare(queue='network')
    for method_frame, properties, body in channel.consume('network'):
        print(str(body))
    channel.close()
    Connection.close()

    num=0
class evclient():
    def __init__(self) -> None:
        self.connection= pk.BlockingConnection(pk.ConnectionParameters("localhost"))
        self.channel= self.connection.channel()
        result= self.channel.queue_declare(queue='',exclusive=True)

        self.calback_queue= result.method.queue
        self.channel.basic_consume(queue=self.calback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)
        self.reponse=None
        self.corr_id=None
    
    def on_response(self,ch, method,props,body):
        print("id1: " +str(self.corr_id))
        print("Id2: "+ str(props.correlation_id))
        if self.corr_id==props.correlation_id:
            self.reponse=body
    
    def call(self,command):
        self.reponse=None
        self.corr_id=str(uuid.uuid4())
        self.channel.basic_publish(exchange='',routing_key='rpc_queue',
                                   properties=pk.BasicProperties(
                                       reply_to=self.calback_queue,
                                       correlation_id=self.corr_id
                                   ),body=command)
        while self.reponse is None:
            self.connection.process_data_events(time_limit=None)
        return self.reponse
    

if __name__=="__main__":
   evstart= evclient()
   retrive_network()
   #retrive_network_iec61850()

#    print("ev connected")
#    response=evstart.call("start")
#    print("waitiing for response")
#    print(response)