import json
import boto3
from datetime import datetime

iot = boto3.client('iot-data')
 
def lambda_handler(event, context):
    topic = 'speaker/voice-kit/say'
    payload = {
        'text': _get_text(event['event'])
    }
    try:
        iot.publish(
            topic=topic,
            qos=0,
            payload=json.dumps(payload, ensure_ascii=False)
        )
 
        return {
            'statusCode': 200,
            'body': 'Succeeded.'
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Failed.'
        }

def _get_text(button):
    if button == 'Back':
        text = 'おはよう'
    elif button == 'A':
        text = 'こんにちは'
    elif button == 'B':
        text = 'こんばんは'
    elif button == 'C':
        text = 'IoT'
    elif button == 'D':
        text = 'プログラミング'
    else:
        text = 'ものづくり'
        
    return text
