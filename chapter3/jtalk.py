import argparse
import subprocess

'''
発話させたい内容を受け取って音声ファイルを作成する関数
- text : 喋らせたいテキスト
- path : 音声ファイルの作成先
'''
def create_wave(text, path):
    # テキストをUTF-8に変換
    if isinstance(text, bytes):
        text = text.decode('utf-8')

    text = text.strip()
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.encode('utf-8')

    # コマンドを作成する部分。必要なコマンドとその引数やオプションを繋げているだけです。
    open_jtalk = ['open_jtalk']
    mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice']
    outwav = ['-ow', path]
    cmd = open_jtalk + mech + htsvoice + outwav

    # 作成したコマンドを子プロセスとして実行
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(text)
    c.stdin.close()
    c.wait()

    return path

def play(path):
    # aplayコマンドを実行する
    cmd = ['aplay', path]
    subprocess.call(cmd)

def jtalk(text, path='/tmp/jtalk.wav'):
    path = create_wave(text, path)
    play(path)


if __name__ == '__main__':
    # コマンドの引数を受け取る
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--text', required=True, help='発話させるテキスト')
    ap.add_argument('-p', '--path', default='/tmp/jtalk.wav',
            help='作成する音声ファイルへのパス')
    args = vars(ap.parse_args())

    jtalk(args['text'], args['path'])
