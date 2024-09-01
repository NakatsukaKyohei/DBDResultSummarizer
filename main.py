import cv2
import os
import numpy as np

template_file_path = "./database/add_on/cannibal"
base_image_path = './database/search_image.jpg'
first_addon_location_left_up = (550, 794)
first_addon_location_right_down = (591, 835)
second_addon_location_left_up = (597, 794)
second_addon_location_right_down = (637, 835)
# n個目のアドオン / 左上 or 右下 / x座標 or y座標
addon_location = [[[550, 794], [591, 835]], [[597, 794], [637, 835]]]

def main():
    killer_addon_path_list = os.listdir(template_file_path)
    base_image = imread(base_image_path)

    first_addon_base = base_image[addon_location[0][0][1]:addon_location[0][1][1], addon_location[0][0][0]:addon_location[0][1][0]]
    second_addon_base = base_image[addon_location[1][0][1]:addon_location[1][1][1], addon_location[1][0][0]:addon_location[1][1][0]]

    first_addon = get_most_reliable_addon(killer_addon_path_list, first_addon_base)
    second_addon = get_most_reliable_addon(killer_addon_path_list, second_addon_base)
    print("使用アドオン1: {}".format(first_addon[0]))
    print("使用アドオン2: {}".format(second_addon[0]))

    # 画像を表示
    cv2.imshow('base_image', second_addon_base)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def get_most_reliable_addon(template_path_list, base_image):
    results = {}
    for i in template_path_list:
        path = "{}/{}".format(template_file_path, i)
        template = imread(path)
        result = template_match(template, base_image)
        basename = i.split('.')[0]
        results[basename] = result
    results = sorted(results.items(), key=lambda x:x[1], reverse=True)
    return results[0]

def template_match(template, base_image):

    result = cv2.matchTemplate(base_image, template, cv2.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

if __name__ == "__main__":
    main()