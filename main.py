from score import Score
from prot import Prot
import score_generator as sg
import player.player as pl


def main():
    PATH = "./data/Original_Score/amefuri-1.png"
    score = Score(PATH)
    paragraph_data, pitch = score.detect_lines()

    print(paragraph_data)
    score.labeling()
    imgs = [score.img, score.img_thresh_base, score.img_line_removed]

    prot = Prot()
    prot.export_img(imgs)
    prot.paragraph(paragraph_data, imgs[1])
    prot.marbles(score)

    EXPORT_NAME = "score"
    sg.export_csv(score, EXPORT_NAME)
    pl.synthesizer(EXPORT_NAME)

if __name__ == '__main__':
    main()