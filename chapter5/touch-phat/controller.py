import argparse
import json
import signal
import sys
import touchphat
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# アプリケーションのコマンドライン化
ap = argparse.ArgumentParser()
ap.add_argument('-n', '--name', required=True, dest='name')
ap.add_argument('-e', '--endpoint', required=True, dest='endpoint')
ap.add_argument('-r', '--rootca', required=True, dest='rootca')
ap.add_argument('-k', '--key', required=True, dest='key', help='Path to private key.')
ap.add_argument('-c', '--cert', required=True, dest='cert')
args = ap.parse_args()
# AWS IoTのクライアント作成
client = AWSIoTMQTTClient(args.name)
# クライアントの初期設定    
client.configureEndpoint(args.endpoint, 8883)
client.configureCredentials(args.rootca, args.key, args.cert)
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(300)
client.configureMQTTOperationTimeout(10)


@touchphat.on_release(['Back', 'A', 'B', 'C', 'D', 'Enter'])
def handle_touch(event):
    payload = {"event": event.name}
    client.publish(
        topic='button/'+args.name+'/event',
        payload=json.dumps(payload),
        QoS=1
    )

def main():
    client.connect(60)
    client.publish('button/'+args.name+'/stat', 'connected.', 1) 
    try:
        signal.pause()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
