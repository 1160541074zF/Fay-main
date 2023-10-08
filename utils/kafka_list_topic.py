from kafka.admin import KafkaAdminClient
import configparser
positionConfig = configparser.ConfigParser()
positionConfig.read(r"../config.ini")
kafka_ip = positionConfig.get("kafka","kafka_ip")
print(kafka_ip)
admin_client = KafkaAdminClient(bootstrap_servers=kafka_ip)

topics = admin_client.list_topics()
for topic in topics:
    print(topic)