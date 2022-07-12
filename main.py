from score import Score
from prot import Prot


def main():
    PATH = "./data/Original_Score/0001.jpg"
    score = Score(PATH)
    paragraph_data, pitch = score.detect_lines()

    print(paragraph_data)
    imgs = [score.img, score.img_thresh_base]
    prot = Prot()
    prot.export_img(imgs)
    prot.paragraph(paragraph_data, imgs[1])

    marbles = score.labeling(pitch)
    prot.marbles(marbles)


if __name__ == '__main__':
    main()