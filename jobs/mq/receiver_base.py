# coding:utf-8
'''
Created on 2012-12-12

@author: JD
'''

import pika
import sys

class MQReceiverBase(object):
    def __init__(self, binding_keys_list):
        self.host = '42.121.31.175'
        self.exchange = 'woyaoooMQExc'
        self.type = 'topic'
        self.binding_keys = binding_keys_list
        
    def startListen(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
            channel = connection.channel()
            channel.exchange_declare(exchange = self.exchange, type = self.type)
            
            result = channel.queue_declare(exclusive = True)
            queue_name = result.method.queue
            
            for eachBindingKey in self.binding_keys:
                channel.queue_bind(exchange = self.exchange, queue = queue_name, routing_key = eachBindingKey)
            
            print >> sys.stdout, "MQReceiver starting...Connect to MQ server successfull!!"  
            channel.basic_consume(self.callBack, queue = queue_name, no_ack = True)
            channel.start_consuming()
        except Exception, e:
            print >> sys.stdout, 'Error @MQReceiver.StartListen: %r' % e    
      
    def callBack(self, ch, method, properties, body):
        try:
           print('this is base. need a sub implementation for callback')
        except Exception, e:
            print >> sys.stdout, 'Error @MQReceiver_Conversateion.Create: %r' % e      
            