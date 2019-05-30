import time
from aiy.voice import audio


def wait():
    time.sleep(3)

def main():
    print('Start recording for 3 seconds...')
    audio.record_file(audio.AudioFormat.CD,
                      filename='sample.wav',
                      wait=wait,
                      filetype='wav')
    print('Done.')


if __name__ == '__main__':
    main()
