import argparse
import numpy as np
from pdf2image import convert_from_path


def in_range(arr, low, high):
    if low[0] <= arr[0] <= high[0] and low[1] <= arr[1] <= high[1] and low[2] <= arr[2] <= high[2]:
        return True
    return False


def count_range(colors, low, high):
    count = 0
    if colors is None:
        return 0
    for a in colors:
        if in_range(a[1], low, high):
            count += a[0]
    return count


def scan_Test(file):
    lower_red = [0, 0, 100]
    upper_red = [0, 0, 255]

    lower_blue = [100, 0, 0]
    upper_blue = [255, 0, 0]

    lower_green = [0, 100, 0]
    upper_green = [0, 255, 0]
    pages = convert_from_path(file, 100)
    ret = []
    page_number = 1
    for page in pages:
        colors = page.getcolors(9999999)
        count_red = count_range(colors, lower_red, upper_red)
        count_blue = count_range(colors, lower_blue, upper_blue)
        count_green = count_range(colors, lower_green, upper_green)
        sum_color = np.sum((count_red, count_green, count_blue))

        if sum_color > 0:
            ret.append((page_number, count_red, count_green, count_blue, sum_color))
            # print(page_number, count_red, count_green, count_blue, sum_color)
        page_number = page_number + 1
    if len(ret) > 0:
        pages_found = ",".join(map(lambda x: str(x[0]), ret));
        print(f"corrupt on pages {pages_found}")
    return ret


def FindCorrupt(file, poppler_path, no_print=False):


    red_low = [50, 0, 0]
    red_high = [255, 0, 0]
    red_light = [255, 0, 0]
    red_dark = [255, 100, 100]

    orange_low = [255, 128, 0]
    orange_high = [255, 173, 90]
    orange_light = [156, 78, 0]
    orange_dark = [255, 128, 0]
    orange_mod_light = [255, 200, 0]
    orange_mod_dark = [255, 255, 100]

    blue_low = [0, 0, 100]
    blue_high = [0, 0, 255]
    blue_light = [0, 0, 255]
    blue_dark = [100, 100, 255]

    green_low = [0, 100, 0]
    green_high = [0, 255, 0]
    green_light = [0, 255, 0]
    green_dark = [100, 255, 100]

    pink_low = [255, 0, 255]
    pink_high = [255, 200, 255]
    pink_light = [150, 0, 150]
    pink_dark = [255, 0, 255]

    yellow_low = [255, 255, 0]
    yellow_high = [255, 255, 100]
    yellow_light = [150, 150, 0]
    yellow_dark = [255, 255, 0]

    white_low = [240, 240, 240]
    white_high = [256, 256, 256]

    black_low = [0, 0, 0]
    black_high = [100, 100, 100]
    gray_low = [126, 126, 126]
    gray_high = [130, 130, 130]

    pages = convert_from_path(file, 100, poppler_path=poppler_path)
    results = []
    page_number = 1
    for page in pages:
        arr = page.getcolors(9999999)
        amount_red = count_range(arr, red_low, red_high)
        amount_red2 = count_range(arr, red_light, red_dark)

        amount_blue = count_range(arr, blue_low, blue_high)
        amount_blue2 = count_range(arr, blue_light, blue_dark)

        amount_orange = count_range(arr, orange_low, orange_high)
        amount_orange2 = count_range(arr, orange_light, orange_dark)
        amount_orange_3 = count_range(arr, orange_mod_light, orange_mod_dark)

        amount_green = count_range(arr, green_low, green_high)
        amount_green2 = count_range(arr, green_light, green_dark)

        amount_pink = count_range(arr, pink_low, pink_high)
        amount_pink2 = count_range(arr, pink_light, pink_dark)

        amount_yellow = count_range(arr, yellow_low, yellow_high)
        amount_yellow2 = count_range(arr, yellow_light, yellow_dark)

        amount_white = count_range(arr, white_low, white_high)
        amount_black = count_range(arr, black_low, black_high)
        amount_gray = count_range(arr, gray_low, gray_high)

        sum_color = np.sum((amount_red, amount_red2, amount_green, amount_green2, amount_blue,
                            amount_blue2, amount_pink, amount_pink2, amount_yellow, amount_yellow2,
                            amount_orange, amount_orange2, amount_orange_3))
        sum_white_black = np.sum((amount_white, amount_black))

        if sum_color > sum_white_black:
            results.append((page_number))
        elif amount_gray > sum_white_black:
            results.append((page_number))
        page_number = page_number + 1
    if not no_print and len(results) > 0:
        print('Corrupt Pages:', results)
        return results
    else:

        return 'None'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pdf", help="path to pdf",required=True)
    ap.add_argument("-l", "--poppler", help="path to poppler",required=True)
    args = vars(ap.parse_args())
    # scan_Test(args["pdf"]);
    FindCorrupt(args["pdf"], args["poppler"])
