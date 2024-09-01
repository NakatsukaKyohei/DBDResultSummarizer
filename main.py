import cv2
import os
import numpy as np

killer_template_path = "./database/killer/"
addon_template_path = "./database/addon/"
base_image_path = './database/test.jpg'
# n個目のアドオン / 左上 or 右下 / x座標 or y座標
addon_location = [[[550, 794], [591, 835]], [[597, 794], [637, 835]]]
killer_location = [[484, 794], [524, 835]] 

def main():
    base_image = imread(base_image_path)

    killer_base_image = base_image[killer_location[0][1]:killer_location[1][1], killer_location[0][0]:killer_location[1][0]]
    killer_type = get_most_reliable_template(killer_template_path, os.listdir(killer_template_path), killer_base_image)
    print("キラー: {}".format(killer_type))

    first_addon_base_image = base_image[addon_location[0][0][1]:addon_location[0][1][1], addon_location[0][0][0]:addon_location[0][1][0]]
    second_addon_base_image = base_image[addon_location[1][0][1]:addon_location[1][1][1], addon_location[1][0][0]:addon_location[1][1][0]]

    addon_path_list = os.listdir(addon_template_path + killer_type[0])
    first_addon = get_most_reliable_template(addon_template_path + killer_type[0], addon_path_list, first_addon_base_image)
    second_addon = get_most_reliable_template(addon_template_path + killer_type[0], addon_path_list, second_addon_base_image)
    print("使用アドオン1: {}".format(first_addon[0]))
    print("使用アドオン2: {}".format(second_addon[0]))

    killer_top_left = (killer_location[0][0] + killer_type[1][1][0], killer_location[0][1] + killer_type[1][1][1])
    killer_bottom_right = (killer_top_left[0] + 37, killer_top_left[1] + 37)
    cv2.rectangle(base_image, killer_top_left, killer_bottom_right, (255, 255, 0), 2)

    first_addon_top_left = (addon_location[0][0][0] + first_addon[1][1][0], addon_location[0][0][1] + first_addon[1][1][1])
    first_addon_bottom_right = (first_addon_top_left[0] + 37, first_addon_top_left[1] + 37)
    cv2.rectangle(base_image, first_addon_top_left, first_addon_bottom_right, (255, 255, 0), 2)

    second_addon_top_left = (addon_location[1][0][0] + second_addon[1][1][0], addon_location[1][0][1] + first_addon[1][1][1])
    second_addon_bottom_right = (second_addon_top_left[0] + 37, second_addon_top_left[1] + 37)
    cv2.rectangle(base_image, second_addon_top_left, second_addon_bottom_right, (255, 255, 0), 2)

    # 画像を表示
    cv2.imshow('base_image', base_image)
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

def get_most_reliable_template(base_path, template_path_list, base_image):
    results = {}
    for i in template_path_list:
        path = "{}/{}".format(base_path, i)
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