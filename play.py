import sys
import player.player as pl

# csv形式のファイル名を指定して./player/player.pyを呼び出し、音源を直接生成
if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        pl.synthesizer(args[1])
    else:
        print("引数が不足（入力ファイルパスを指定してください）")