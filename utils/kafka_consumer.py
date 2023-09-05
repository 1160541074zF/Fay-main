from kafka import KafkaConsumer
from kafka import KafkaConsumer

# 创建一个 Kafka 消费者
consumer = KafkaConsumer('reminder', bootstrap_servers='192.168.3.48:9092')

# 启动消费者监听
for message in consumer:
    # 打印接收到的消息
    print(f"Received: {message.value.decode('utf-8')}")