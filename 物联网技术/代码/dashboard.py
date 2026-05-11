from flask import Flask, render_template,request
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f">>> MQTT 层收到数据: {payload}")

        # 修改：在 Flask 应用上下文中安全地 emit
        with app.app_context():
            socketio.emit('update_data', payload, namespace='/',room=None)
            # 打印发送状态
            print(f"已尝试广播 update_data")

    except Exception as e:
        print(f"数据处理异常: {e}")

mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f"前端已连接: {request.sid}")
    # 发送一条测试数据确认通路
    socketio.emit('update_data', {'temperature': 25, 'humidity': 60}, room=request.sid, namespace='/')

if __name__ == '__main__':
    try:
        mqtt_client.connect("127.0.0.1", 1883, 60)
        mqtt_client.subscribe("iot/sensor/data")
        mqtt_client.loop_start()
        print("后端已启动！访问 http://127.0.0.1:5000")
        socketio.run(app, host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        print(f"服务器启动失败: {e}")