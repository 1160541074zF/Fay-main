from kafka.admin import KafkaAdminClient

admin_client = KafkaAdminClient(bootstrap_servers='192.168.3.48:9092')

topics = admin_client.list_topics()
for topic in topics:
    print(topic)