from kafka import KafkaProducer
import json

def send_message_to_kafka(kafka_ip, topic_name, message):
    # 创建Kafka生产者
    producer = KafkaProducer(bootstrap_servers=kafka_ip, value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    # 将消息发送到指定主题
    producer.send(topic_name, message)
    # 等待消息发送成功
    producer.flush()
    # 关闭Kafka生产者
    producer.close()