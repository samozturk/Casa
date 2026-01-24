





def publish_mqtt_message(topic: str, message: str, port: int = 1883, ip_address: str = "tnas"):
    '''Publish a single MQTT message to a topic.
    Args:
        topic (str): AMQTT topic to publish the message to.
        message (str): The message payload to send.
        port (int): port number of the MQTT broker. Defaults to 1883.
        ip_address (str, optional): IP address of the MQTT broker. Defaults to "tnas".
    '''
    import paho.mqtt.client as mqtt

    # Create an MQTT client instance
    client = mqtt.Client(protocol=mqtt.MQTTv311) 

    # Connect to the broker (replace with your broker's address & port)
    client.connect(ip_address, port, 60)

    # Publish a single message to a topic
    client.publish(topic, payload=message, qos=0)

# TODO: add subscribe to an ACK topic to confirm message delivery and function completion

def print_sth(a="hello"):
    print(f"{a} from utils.py")




