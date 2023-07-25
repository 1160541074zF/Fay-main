from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(bootstrap_servers='8.130.108.7:9092')
'''
已添加话题：
voice_tts 语音播报话题
'''

topic_name = "control"
num_partitions = 1
replication_factor = 1

topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
admin_client.create_topics(new_topics=[topic])