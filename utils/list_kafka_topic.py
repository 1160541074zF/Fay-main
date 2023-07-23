from kafka.admin import KafkaAdminClient

admin_client = KafkaAdminClient(bootstrap_servers='8.130.108.7:9092')

topics = admin_client.list_topics()
for topic in topics:
    print(topic)