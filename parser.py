from PIL import Image
import os
import json

CAPTCHA_DIM = (120, 40)
CHARACTER_DIM = (16, 29)
FPATH = os.path.dirname(os.path.realpath(__file__))
start=30
end=94


def parse_captcha(img):

    captcha = ""

    img_width = CAPTCHA_DIM[0]
    img_height = CAPTCHA_DIM[1]

    char_width = CHARACTER_DIM[0]
    char_height = CHARACTER_DIM[1]

    char_crop_threshold = {'upper': 9, 'lower': 38}

    img_matrix = img.convert('L').load()

    bitmaps_fpath = os.path.join(FPATH, "bitmaps.json")

    bitmaps = json.load(open(bitmaps_fpath))
    ct=0

    # remove single pixel width noise + thresholding
    for column in range(0, img.height):
        for row in range(0, img.width):
            if img_matrix[row, column] >= 29 and img_matrix[row, column] <= 110  :
                img_matrix[row, column] = 0
            else:
                img_matrix[row, column] = 255

    # loop through individual characters
    for i in range(start, end, char_width):
        

        # crop with left, top, right, bottom coordinates
        
        img_char_matrix = img.crop(
            (i, char_crop_threshold['upper'], i+char_width, char_crop_threshold['lower'])).convert('L').load()
        matches = {}
        for column in range(0, char_height):
            for row in range(0, char_width):
                if img_char_matrix[row, column] >= 29 and img_char_matrix[row, column] <= 110  :
                    img_char_matrix[row, column] = 0
                else:
                   img_char_matrix[row, column] = 255


        for character in bitmaps:
            match_count = 0
            black_count = 0

            lib_char_matrix = bitmaps[character]
            for y in range(0, char_height):
                for x in range(0, char_width):
                    ct+=1

                    if img_char_matrix[x, y] == lib_char_matrix[y][x]  == 0:

                        match_count += 1
                    if lib_char_matrix[y][x] == 0:
                        black_count += 1

            perc = float(match_count)/float(black_count)

            matches.update({perc: character})

        try:
            captcha += matches[max(matches.keys())]

            
        except ValueError:
            captcha += "0"
    return captcha.lower()


if __name__ == '__main__':
    img = Image.open(os.path.join(FPATH, "test.png"))
    print(parse_captcha(img))
