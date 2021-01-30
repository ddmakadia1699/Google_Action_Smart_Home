import paho.mqtt.client as mqtt
import logging
import time
import json
import uuid
import requests
import random
import colorsys
import boto3
from boto3.dynamodb.conditions import Key, Attr
from validation import validate_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def on_connect(client, userdata, flags, rc) :
    print ("Connected!", str(rc))
def lambda_handler(request, context):
    global names
    mqtt_broker_ip = "tailor.cloudmqtt.com"
    client = mqtt.Client("cloudmqtt"  + str(random.randint(1,1000)))
    client.username_pw_set("ffbqwwfa","PAC8F72zynig")
    client.on_connect = on_connect
    client.connect(mqtt_broker_ip, 13582)
    # client.publish("test",str(request))
    try:
        if request["inputs"][0]["intent"] == "action.devices.SYNC":
            user = '4'
            client = boto3.client('dynamodb')
            DB =     boto3.resource('dynamodb')
            table = DB.Table('device')
            response = table.scan(
                FilterExpression=Attr('user').eq(user)
            )
            items = response['Items']
            #print (items)
            print (len(items))
            device =  '{"devices" : []}'
            yx = json.loads(device)
            temp1 = yx['devices']
            for a in range(len(items)):
                endpointId = items[a]['api_key']
                displayCategories = items[a]['displayCategories']
                description = items[a]['description']
                friendlyName = items[a]['friendlyName']
                print (endpointId)
                print (displayCategories)
                print (description)
                print (friendlyName)
                mqtt_broker_ip = "tailor.cloudmqtt.com"
                client = mqtt.Client("cloudmqtt"  + str(random.randint(1,1000)))
                client.username_pw_set("ffbqwwfa","PAC8F72zynig")
                client.on_connect = on_connect
                client.connect(mqtt_broker_ip, 13582)
                # client.publish("test",str(endpointId))
                # client.publish("test",str(displayCategories))
                # client.publish("test",str(description))
                # client.publish("test",str(friendlyName))
                trait =  '{"traits" : []}'
                y = json.loads(trait)
                temp = y['traits']
                Brightness = 'action.devices.traits.Brightness'
                ColorSetting = 'action.devices.traits.ColorSetting'
                ColorTemperature = 'action.devices.traits.ColorTemperature'
                FanSpeed = 'action.devices.traits.FanSpeed'
                OnOff = 'action.devices.traits.OnOff'
                # if(displayCategories == "LIGHT"):
                #     x = json.loads(PowerController)
                #     temp.append(x)
                #     x = json.loads(BrightnessController)
                #     temp.append(x)
                #     x = json.loads(ColorController)
                #     temp.append(x)
                
                
            return {
              "requestId": request["requestId"],
              "payload": {
                "agentUserId": user,
                "devices": [
                  {
                    "id": "cap1",
                    "type": "action.devices.types.SWITCH",
                    "traits": [
                      "action.devices.traits.OnOff"
                    ],
                    "name": {
                      "defaultNames": [
                        "Switch 1"
                      ],
                      "name": "Switch 1",
                      "nicknames": [
                        "Switch One"
                      ]
                    },
                    "willReportState": False,
                    "roomHint": "kitchen",
                    "deviceInfo": {
                      "manufacturer": "dhrumil-makadia",
                      "model": "dm12",
                      "hwVersion": "1.0",
                      "swVersion": "12.4"
                    },
                    "otherDeviceIds": [
                      {
                        "deviceId": "local-device-id"
                      }
                    ],
                    "customData": {
                      "fooValue": 74,
                      "barValue": True,
                      "bazValue": "foo"
                    }
                  },
                  {
                    "id": "cap2",
                    "type": "action.devices.types.SWITCH",
                    "traits": [
                      "action.devices.traits.OnOff"
                    ],
                    "name": {
                      "defaultNames": [
                        "Switch 2"
                      ],
                      "name": "Switch 1",
                      "nicknames": [
                        "Switch Two"
                      ]
                    },
                    "willReportState": False,
                    "roomHint": "kitchen",
                    "deviceInfo": {
                      "manufacturer": "dhrumil-makadia",
                      "model": "dm12",
                      "hwVersion": "1.0",
                      "swVersion": "12.4"
                    },
                    "otherDeviceIds": [
                      {
                        "deviceId": "local-device-id"
                      }
                    ],
                    "customData": {
                      "fooValue": 74,
                      "barValue": True,
                      "bazValue": "foo"
                    }
                  }
                ]
              }
            }
            
        elif request["inputs"][0]["intent"] == "action.devices.QUERY":
            topic =  (request["inputs"][0]["payload"]["devices"][0]["id"])
            print (topic)
            client = boto3.client('dynamodb')
            DB =     boto3.resource('dynamodb')
            table = DB.Table('device')
            response = table.scan(
                FilterExpression=Key('api_key').eq(topic)
            )
            
            valuePower = response['Items'][0]['statusPower']
            print(valuePower)
            if(valuePower == "ON"):
                valuePower1 = True
            else:
                valuePower1 = False
        
            return{
              "requestId": request["requestId"],
              "payload": {
                "devices": {
                  topic: {
                    "status": "SUCCESS",
                    "online": True,
                    "on": valuePower1
                  }
                }
              }
            }

        elif request["inputs"][0]["intent"] == "action.devices.EXECUTE":
            msg = "error"
            topic =  (request["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"])
            if(topic == "cap1"):
                msg =  (request["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"])
                if(str(msg) == "True"):
                    value = "ON"
                    msg = "TURNON"
                    client = boto3.client('dynamodb')
                    DB =     boto3.resource('dynamodb')
                    table = DB.Table('device')
                    response = table.update_item(
                        Key={
                            'api_key': 'cap1'
                        },
                        UpdateExpression="set statusPower=:p",
                        ExpressionAttributeValues={
                            ':p': value
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                else:
                    msg = "TURNOFF"
                    value = "OFF"
                    client = boto3.client('dynamodb')
                    DB =     boto3.resource('dynamodb')
                    table = DB.Table('device')
                    response = table.update_item(
                        Key={
                            'api_key': 'cap1'
                        },
                        UpdateExpression="set statusPower=:p",
                        ExpressionAttributeValues={
                            ':p': value
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                # topic = "PSOC6"
            if(topic == "cap2"):
                msg =  (request["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"])
                if(str(msg) == "True"):
                    msg = "TURNON"
                    value = "ON"
                    client = boto3.client('dynamodb')
                    DB =     boto3.resource('dynamodb')
                    table = DB.Table('device')
                    response = table.update_item(
                        Key={
                            'api_key': 'cap2'
                        },
                        UpdateExpression="set statusPower=:p",
                        ExpressionAttributeValues={
                            ':p': value
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                else:
                    msg = "TURNOFF"
                    value = "OFF"
                    client = boto3.client('dynamodb')
                    DB =     boto3.resource('dynamodb')
                    table = DB.Table('device')
                    response = table.update_item(
                        Key={
                            'api_key': 'cap2'
                        },
                        UpdateExpression="set statusPower=:p",
                        ExpressionAttributeValues={
                            ':p': value
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                # topic = "PSOC6"
                
            mqtt_broker_ip = "tailor.cloudmqtt.com"
            client = mqtt.Client("cloudmqtt"  + str(random.randint(1,1000)))
            client.username_pw_set("ffbqwwfa","PAC8F72zynig")
            client.on_connect = on_connect
            client.connect(mqtt_broker_ip, 13582)
            client.publish(topic,msg)
            
            return {
              "requestId": request["requestId"],
              "payload": {
                "commands": [
                  {
                    "ids": [
                      request["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"]
                    ],
                    "status": "SUCCESS",
                    "states": {
                      "online": True,
                      "on": True
                    }
                  }
                ]
              }
            }
        
    except ValueError as error:
        logger.error(error)
        raise