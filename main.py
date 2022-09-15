import argparse

import cv2


def scan_pdf(file):
    import numpy as np
    from pdf2image import convert_from_path
    lower_red = np.array([0, 0, 100], dtype="uint8")
    upper_red = np.array([0, 0, 255], dtype="uint8")

    lower_blue = np.array([100, 0, 0], dtype="uint8")
    upper_blue = np.array([255, 0, 0], dtype="uint8")

    lower_green = np.array([0, 100, 0], dtype="uint8")
    upper_green = np.array([0, 255, 0], dtype="uint8")
    pages = convert_from_path(file, 500)
    ret = []
    page_number = 1
    for page in pages:
        arr = np.asarray(page)

        mask_red = cv2.inRange(arr, lower_red, upper_red)
        mask_blue = cv2.inRange(arr, lower_blue, upper_blue)
        mask_green = cv2.inRange(arr, lower_green, upper_green)
        count_red = np.count_nonzero(mask_red)
        count_blue = np.count_nonzero(mask_blue)
        count_green = np.count_nonzero(mask_green)
        # print(count_red, count_green, count_blue)
        sum_color = np.sum((count_red, count_green, count_blue))

        if sum_color > 0:
            ret.append((page_number, count_red, count_green, count_blue, sum_color))
            # print(page_number, count_red, count_green, count_blue, sum_color)
        page_number = page_number + 1
    if len(ret) > 0:
        pages_found = ",".join(map(lambda x: str(x[0]), ret));
        print(f"corrupt on pages {pages_found}")
    return ret


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pdf", help="path to the pdf")
    args = vars(ap.parse_args())

    print(scan_pdf(args["pdf"]))
