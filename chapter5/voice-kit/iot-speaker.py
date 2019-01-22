from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from jtalk import jtalk
import time
import signal
import sys

def getClient(name, endpoint, rootca, key, cert):
    """
        AWSIoTのクライアントを作成する関数
    """
    client = AWSIoTMQTTClient(name)
    client.configureEndpoint(endpoint, 8883)
    client.configureCredentials(rootca, key, cert)

    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(300)
    client.configureMQTTOperationTimeout(10)

    return client

def say(client, userdata, message):
    """
        jtalk関数を呼び出すコールバック
    """
    jtalk(message.payload)


if __name__ == '__main__':
    import argparse
    
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--name', required=True, dest='name')
    ap.add_argument('-e', '--endpoint', required=True, dest='endpoint')
    ap.add_argument('-r', '--rootca', required=True, dest='rootca')
    ap.add_argument('-k', '--key', required=True, dest='key')
    ap.add_argument('-c', '--cert', required=True, dest='cert')
    args = ap.parse_args()

    name = args.name
    endpoint = args.endpoint
    rootca = args.rootca
    key = args.key
    cert = args.cert

    client = getClient(name, endpoint, rootca, key, cert)
    client.subscribe('command/'+name+'/say', 1, say)
    client.connect(60)
    time.sleep(2)
    client.publish('stat/'+name+'/connection', 'connected.', 1)

    try:
        signal.pause()
    except KeyboardInterrupt:
        sys.exit(0)
