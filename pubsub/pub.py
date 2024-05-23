import pika as pk
import func
import time
import sys
from powersystemsimulation import test
def main():
    connection= pk.BlockingConnection(pk.ConnectionParameters(host="localhost"))
    channel= connection.channel()

    channel.queue_declare(queue="network")
    channel.queue_declare(queue="iec61850")
    i=0
    while True:
        try:
            time.sleep(10)
            result= func.counter(i)
            i=i+1
            channel.basic_publish(exchange='',routing_key='network',body=str(result))
            channel.basic_publish(exchange='', routing_key='iec61850',body="working")

        except KeyboardInterrupt:
            connection.close()
            sys.exit()
            
    print("send the message")


class network():
    def __init__(self) -> None:
        self.connection=pk.BlockingConnection(pk.ConnectionParameters(host="localhost"))
        self.channel=self.connection.channel()
        self.channel.queue_declare(queue="network")
        self.channel.queue_declare(queue="iec61850")
    def start_publishing(self):
        result =test.run_pf("network")
        self.channel.basic_publish(exchange='',routing_key='network',body=str(result))
        result =test.run_pf("iec61850")
        self.channel.basic_publish(exchange='',routing_key='iec61850',body=str(result))


class evcharginstation():
    def __init__(self) -> None:
        self.connection=pk.BlockingConnection(pk.ConnectionParameters(host="localhost"))
        self.channel=self.connection.channel()
        self.channel.queue_declare(queue="rpc_queue")

    
    def send_reponse(self):
        return "ev started charging"
    
    def on_request(self,ch, method,props, body):
       
        value=str(body)
        value=value.replace("b",'')
        print("body printing .."+value)
        if value != None or value != '':
            response=self.send_reponse()
        else:
            response="no option selected"
        ch.basic_publish(exchange='',routing_key=props.reply_to,
                                   properties=pk.BasicProperties(
                                       correlation_id=props.correlation_id
                                   ),body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="rpc_queue",on_message_callback=self.on_request)
        self.channel.start_consuming()

    

    
    


if __name__=="__main__":
    while 1:
        time.sleep(10)
        ev=network()
        ev.start_publishing()