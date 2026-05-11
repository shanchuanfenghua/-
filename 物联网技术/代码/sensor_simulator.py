import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import json
import time
import random

# 配置信息
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_DATA = "iot/sensor/data"

# 回调函数：连接成功时触发
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("虚拟设备已上线，开始传输数据...")
    else:
        print(f"连接失败，状态码: {rc}")

# 初始化客户端 (适配 paho-mqtt v2.x)
client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id="Simulated_Sensor_01")
client.on_connect = on_connect

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # 开启后台循环

    while True:
        # 模拟生成传感器数据
        temp = round(random.uniform(20.0, 30.0), 2)
        # 模拟 10% 概率出现异常高温（用于演示报警）
        if random.random() > 0.9:
            temp = round(random.uniform(45.0, 55.0), 2)
            
        payload = {
            "device_id": "sensor_v01",
            "temperature": temp,
            "humidity": round(random.uniform(40, 70), 2),
            "timestamp": time.time()
        }
        
        # 发布消息
        client.publish(TOPIC_DATA, json.dumps(payload))
        print(f"发送数据: {payload}")
        time.sleep(2)

except KeyboardInterrupt:
    print("设备已停止")
    client.loop_stop()
    client.disconnect()