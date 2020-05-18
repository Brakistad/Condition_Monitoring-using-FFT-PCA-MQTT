# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 11:08:26 2020

@author: oyvin
"""

import paho.mqtt.client as mqttClient;
import time as t;
from kb_utils import SaveLoad as SL;

localClient = mqttClient.Client();
serverClient = mqttClient.Client();
serverIp = "none";
userInfo = ("none", "none");
subTopic = "default";
recievedMsg = False;
recentMsg = "";
maxMsgLogs = 10;
msgLogIndex = 0;
stopListen = False;
class mqtt_User():

    def on_message(self,client, userdata, message):                 #define callback function
        #print("message received ", str(message.payload.decode("utf-8")))
        print("on_message started");
        global serverClient;
        global localClient;
        global recievedMsg;
        global recentMsg;
        global maxMsgLogs;
        global msgLogIndex;
        msg_topic = message.topic;
        #msg_qos = message.qos;
        msg_retain = message.retain;
        msg_payload = str(message.payload.decode("utf-8"));
        if not (msg_retain == 1):
            recievedMsg = True;
            print("message was not retained");
            if not (msg_payload == ''):
                print("on_message: payload not empty");
                #print(msg_payload);
                #temp_msg = [msg_payload, msg_topic, msg_qos, msg_retain];
                fileName = 'unknown_log';
                if (client == localClient):
                    fileName = 'local_log';
                elif (client == serverClient):
                    fileName = 'server_log';
                print("on_message: filename is " + fileName);
                partLoad = SL('load', fileName); #Loading up past variables
                finalMessage = (msg_payload, str(msg_topic), str(t.asctime(t.localtime())));
                if(partLoad == None):
                    print("on_message: partLoad was empty");
                    partLoad = [finalMessage];
                else:
                    print("on_message: partLoad not empty");
                    curLen = len(partLoad);
                    if not (partLoad[-1:][:1] == finalMessage[:1]):
                        print("on_message: new message not equal to last logged message");
                        if not (curLen < maxMsgLogs):
                            print("on_message: message log limit reached");
                            partLoad.remove(partLoad[0]);
                        else:
                            print("on_message: message log limit not reached");
                        partLoad.append(finalMessage);
                SL('save', fileName, variables = partLoad); # Saving Variables
                recentMsg = finalMessage;
        else:
            print("message was retained");
#            if (msg_retain == 1):
#                serverClient.publish(msg_topic, '', 0, True);
#                print("on_message: deleted retained message at " + msg_topic);
    
    def get_recentMsg(self):
        global recentMsg;
        global recievedMsg;
        recievedMsg = False;
        return recentMsg;

    def get_msgLog(self):
        msgLog = SL('load','server_log');
        return msgLog;
    
    def stop_listening(self):
        global stopListen;
        stopListen = True;
        
    def get_msgLog_size(self):
        msgLog = self.get_msgLog();
        length = len(msgLog);
        return length;

    def check_recievedMsg(self):
        global recievedMsg;
        return recievedMsg;
    
    def on_connect(self,mqttc, obj, flags, rc):
        global serverClient;
        print("obj: "+str(obj))
        print("rc: "+str(rc));
#        subs = SL('load', 'subscriptions');
#        serverClient.subscribe(subs);
    
    def on_publish(self,mqttc, obj, mid):
        print("mid: "+str(mid))
    
    def on_subscribe(self,mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))
    
    def on_log(self,mqttc, obj, level, string):
        print(string)
    

#    independent method for initializing connection to local server.
#    def init_localConnection(self, ip_mqtt = "127.0.0.1", userName = "thePlebian",passw ='', defaultTopic = "default"):
#        global localClient;
#        if not (serverIp == "none"):
#            ip_mqtt = serverIp;
#        if not (userInfo[0] == "none"):
#            userName = userInfo[0];
#        if not (userInfo[1] == "none"):
#            passw = userInfo[1];
#        if(passw == ''):
#            localClient.connect(ip_mqtt);
#        else:
#            localClient.username_pw_set(userName, passw);
#            localClient.connect(ip_mqtt, 1883);
    
    def init_messageLogs(self):
        SL('save','server_log');
        SL('save','local_log');
        SL('save','unknown_log');
    
    def init_serverConnection(self, ip_mqtt = "192.168.192.7",userName = "thePlebian",passw ='', defaultTopic = "default"):
        global serverClient;
        global serverIp;
        global userInfo;
        serverClient = mqttClient.Client();
        #print("USERDATA: "+ str(userInfo));
        if not (serverIp == "none"):
            ip_mqtt = serverIp;
        if not (userInfo[0] == "none"):
            userName = userInfo[0];
            #print("changed user name: "+str(userInfo[0]));
        if not (userInfo[1] == "none"):
            passw = userInfo[1];
            #print("changed user pass: "+str(userInfo[1]));
        if(passw == ''):
            serverClient.connect(ip_mqtt);
        else:
            serverClient.username_pw_set(userName, passw);
            serverClient.connect(ip_mqtt, 1883);
   
    def change_serverIp(self,newIp):
        global serverIp;
        serverIp = newIp;
        
    def change_userInfo(self, newUserName = "none", newUserPass = "none"):
        global userInfo;
        #print(newUserName + " ,  " + newUserPass);
        userInfo = (newUserName,newUserPass);

    
    def init_topics(self):
        SL('save','subscriptions', variables = [("default",0)]);
    
    def add_subTopics(self, newTopics):
        oldSubList = SL('load','subscriptions');
        for i in newTopics:
            duple = False;
            for g in oldSubList:
                if(i == g):
                    duple = True;
            if(not duple):
                oldSubList.append(i);
        SL('save','subscriptions', variables = oldSubList);
    
    def remove_subTopics(self, topics):
        oldSubList = SL('load','subscriptions');
        for i in topics:
            for g in oldSubList:
                if(i == g):
                    oldSubList.remove(g);
        SL('save','subscriptions', variables = oldSubList);

    

    def listen_server(self,seconds):
        global serverClient;
        subList = SL('load','subscriptions');
        self.init_serverConnection();
        
        serverClient.on_connect = self.on_connect;
        serverClient.on_message = self.on_message;
        serverClient.on_publish = self.on_publish;
        serverClient.on_subscribe = self.on_subscribe;
        serverClient.on_log = self.on_log;
        
        serverClient.publish('default', 'im listening');
        serverClient.loop_start();
        serverClient.subscribe(subList);
        serverClient.publish('default', 'testing1');
        t.sleep(seconds);
        serverClient.publish('default', 'testing1');
        serverClient.loop_stop();
        serverClient.publish('default', 'im not listening');
        msg = SL('load','server_log');
        #print(msg);

    def listen_until(self):
        global serverClient;
        global recievedMsg;
        global stopListen;
        subList = SL('load','subscriptions');
        self.init_serverConnection();
        serverClient.on_connect = self.on_connect;
        serverClient.on_message = self.on_message;
        serverClient.on_publish = self.on_publish;
        serverClient.on_subscribe = self.on_subscribe;
        serverClient.on_log = self.on_log;
        serverClient.loop_start();
        serverClient.subscribe(subList);
        while(not recievedMsg):
            if(stopListen):
                stopListen = False;
                serverClient.loop_stop();
                return;
            t.sleep(1);
        t.sleep(5);
        serverClient.loop_stop();
        t.sleep(5);
        #msg = SL('load','server_log');
        #print(msg);


def testin():
    import threading;
    import time;
    import socket;
    addr1 = socket.gethostbyname('ip.applause.no');
    print("started testing");
    user = mqtt_User();
    user.change_serverIp(addr1);
    user.change_userInfo('engineer', 'vykgVjYTPDcK');
    user.init_messageLogs();
    #user.add_subTopics([('#',0)]);
    t = threading.Thread(target = user.listen_until);
    print("is_alive = " + str(t.is_alive()));
    print("_initialized = " + str(t._initialized));
    t.start();
    print("is_alive = " + str(t.is_alive()));
    print("_initialized = " + str(t._initialized));
    i=0;
    while(t.isAlive()):
        if(user.check_recievedMsg()):
            print(user.get_recentMsg());
            i = 0;
        else:
            print("listening ... " + str(i));
            i += 1;
            time.sleep(5);
    print(user.get_recentMsg());
    print(addr1);
    print("finnished testing");
#testin();
    
#array = [('first1','second1'),
#         ('first2','second2'),
#         ('first3','second3'),
#         ('first4','second4'),
#         ('first5','second5'),];
#print(array[-1:]);
#print(array[0]);
#array.remove(array[0]);
#print(array[0]);

#init_topics();
#init_serverConnection();
#init_localConnection();
#
#
#serverClient.on_message = on_message;       #attach function to callback
#serverClient.loop_start();                     #start the loop
#
#serverClient.subscribe(('default',1));
#serverClient.publish('default', 'anyMessages');
#
#t.sleep(15);
#msg = SL('load','server_log');
#serverClient.loop_stop();
#
#print(msg);


#%% Save or load variables
#from opy.kb_utils import SaveLoad as SL
#SL('save','vars', variables = a) # Saving Variables
#b = SL('load','vars')
