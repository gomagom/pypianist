from score import Score
from prot import Prot
import score_generator as sg
import player.player as pl
import sys
import re

def main(path):
    # PATH = "./data/Original_Score/amefuri-1.png"
    file_name = re.sub(r"^.*[/\\]|\.[^.]+", "", path)
    score = Score(path)
    paragraph_data = score.detect_lines()

    score.labeling()
    imgs = [score.img, score.img_thresh_base, score.img_line_removed]

    prot = Prot()
    prot.export_img(imgs)
    prot.paragraph(paragraph_data, imgs[1])
    prot.marbles(score)

    sg.export_csv(score, file_name)
    pl.synthesizer(file_name)

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        main(args[1])
    else:
        print("引数が不足（入力ファイルパスを指定してください）")
