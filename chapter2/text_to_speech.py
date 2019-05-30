import subprocess
from aiy.voice import tts

def main():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    text = 'My IP address is %s' % ip_address.decode('utf-8')
    print(text)
    tts.say(text)

if __name__ == '__main__':
    main()
