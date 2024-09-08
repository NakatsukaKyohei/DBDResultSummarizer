import cv2
import os
import numpy as np
import json

killer_perk_template_path = "./database/killer/perk"
killer_icon_template_path = "./database/killer/icon"
killer_addon_template_path = "./database/killer/addon/"
surviver_status_template_path = "./database/surviver/status/"
surviver_perk_template_path = "./database/surviver/perk"
surviver_item_template_path = "./database/surviver/item"
surviver_addon_template_path = "./database/surviver/addon"
base_image_path = './database/result/381210_20240907153516_1.png'
item_type_path = "./database/surviver/surviver_item_type.json"

# base_image_path = './database/killer_reference/スカルマーチャント.png'

# アイコンの位置ずれを想定した位置バッファ
location_buffer = 16

# パークアイコンの位置
killer_perk_location = [
    [[187 - location_buffer, 792 - location_buffer], [233 + location_buffer, 838 + location_buffer]],
    [[243 - location_buffer, 792 - location_buffer], [289 + location_buffer, 838 + location_buffer]],
    [[298 - location_buffer, 792 - location_buffer], [344 + location_buffer, 838 + location_buffer]],
    [[354 - location_buffer, 792 - location_buffer], [400 + location_buffer, 838 + location_buffer]],
]

# キラーアイコンの位置
killer_icon_location = [[484 - location_buffer, 794 - location_buffer], [524 + location_buffer, 835 + location_buffer]] 

# キラーアドオンアイコンの位置
# n個目のアドオン / 左上 or 右下 / x座標 or y座標
killer_addon_location = [
    [[550 - location_buffer, 794 - location_buffer], [591 + location_buffer, 835 + location_buffer]],
    [[597 - location_buffer, 794 - location_buffer], [637 + location_buffer, 835 + location_buffer]]
]

# サバイバーステータスのアイコンの位置
# n人目のステータス / 左上 or 右下 / x座標 or y座標
surviver_status_location = [
    [[180 - location_buffer, 264 - location_buffer], [212 + location_buffer, 289 + location_buffer]],
    [[180 - location_buffer, 378 - location_buffer], [212 + location_buffer, 408 + location_buffer]],
    [[180 - location_buffer, 499 - location_buffer], [212 + location_buffer, 526 + location_buffer]],
    [[180 - location_buffer, 619 - location_buffer], [212 + location_buffer, 647 + location_buffer]]
]

# サバイバーパークの位置(左上)
# 列ごとのx座標 / 行ごとのy座標
surviver_perk_location = [
    [187, 243, 298, 354],
    [310, 430, 551, 672]
]

# サバイバーアイテムの位置
surviver_item_width = 41
surviver_item_location_x = 484
surviver_item_location_y = [312, 432, 552, 674]

# サバイバーアドオンの位置
surviver_addon_width = 41
surviver_addon_location_x = [550, 597]
surviver_addon_location_y = [312, 432, 552, 674]


def main():
    base_image = imread(base_image_path)
    preprocessed_image_for_perk = image_preprocess(base_image, 2)
    preprocessed_image_for_other = image_preprocess(base_image)

    # キラーパークの画像認識
    first_killer_perk_base_image = preprocessed_image_for_perk[killer_perk_location[0][0][1]:killer_perk_location[0][1][1], killer_perk_location[0][0][0]:killer_perk_location[0][1][0]]
    second_killer_perk_base_image = preprocessed_image_for_perk[killer_perk_location[1][0][1]:killer_perk_location[1][1][1], killer_perk_location[1][0][0]:killer_perk_location[1][1][0]]
    third_killer_perk_base_image = preprocessed_image_for_perk[killer_perk_location[2][0][1]:killer_perk_location[2][1][1], killer_perk_location[2][0][0]:killer_perk_location[2][1][0]]
    fourth_killer_perk_base_image = preprocessed_image_for_perk[killer_perk_location[3][0][1]:killer_perk_location[3][1][1], killer_perk_location[3][0][0]:killer_perk_location[3][1][0]]

    killer_perk_path_list = os.listdir(killer_perk_template_path)
    first_killer_perk = get_most_reliable_template(killer_perk_template_path, killer_perk_path_list, first_killer_perk_base_image, 2)
    second_killer_perk = get_most_reliable_template(killer_perk_template_path, killer_perk_path_list, second_killer_perk_base_image, 2)
    third_killer_perk = get_most_reliable_template(killer_perk_template_path, killer_perk_path_list, third_killer_perk_base_image, 2)
    fourth_killer_perk = get_most_reliable_template(killer_perk_template_path, killer_perk_path_list, fourth_killer_perk_base_image, 2)

    print("キラーパーク1: {}".format(first_killer_perk[0]))
    print("キラーパーク2: {}".format(second_killer_perk[0]))
    print("キラーパーク3: {}".format(third_killer_perk[0]))
    print("キラーパーク4: {}".format(fourth_killer_perk[0]))

    rectangle(base_image, killer_perk_location[0][0][0], killer_perk_location[0][0][1], killer_perk_location[0][1][0], killer_perk_location[0][1][1])
    rectangle(base_image, killer_perk_location[1][0][0], killer_perk_location[1][0][1], killer_perk_location[1][1][0], killer_perk_location[1][1][1])
    rectangle(base_image, killer_perk_location[2][0][0], killer_perk_location[2][0][1], killer_perk_location[2][1][0], killer_perk_location[2][1][1])
    rectangle(base_image, killer_perk_location[3][0][0], killer_perk_location[3][0][1], killer_perk_location[3][1][0], killer_perk_location[3][1][1])

    # キラーの画像認識
    killer_base_image = preprocessed_image_for_other[killer_icon_location[0][1]:killer_icon_location[1][1], killer_icon_location[0][0]:killer_icon_location[1][0]]
    killer_type = get_most_reliable_template(killer_icon_template_path, os.listdir(killer_icon_template_path), killer_base_image)
    print("キラー: {}".format(killer_type[0]))

    rectangle(base_image, killer_icon_location[0][0], killer_icon_location[0][1], killer_icon_location[1][0], killer_icon_location[1][1])

    # アドオンの画像認識
    first_addon_base_image = preprocessed_image_for_other[killer_addon_location[0][0][1]:killer_addon_location[0][1][1], killer_addon_location[0][0][0]:killer_addon_location[0][1][0]]
    second_addon_base_image = preprocessed_image_for_other[killer_addon_location[1][0][1]:killer_addon_location[1][1][1], killer_addon_location[1][0][0]:killer_addon_location[1][1][0]]

    addon_path_list = os.listdir(killer_addon_template_path + killer_type[0])
    first_addon = get_most_reliable_template(killer_addon_template_path + killer_type[0], addon_path_list, first_addon_base_image)
    second_addon = get_most_reliable_template(killer_addon_template_path + killer_type[0], addon_path_list, second_addon_base_image)
    print("使用アドオン1: {}".format(first_addon[0]))
    print("使用アドオン2: {}".format(second_addon[0]))

    rectangle(base_image, killer_addon_location[0][0][0], killer_addon_location[0][0][1], killer_addon_location[0][1][0], killer_addon_location[0][1][1])
    rectangle(base_image, killer_addon_location[1][0][0], killer_addon_location[1][0][1], killer_addon_location[1][1][0], killer_addon_location[1][1][1])

    # サバイバーステータスの画像認識
    first_surviver_base_image = preprocessed_image_for_other[surviver_status_location[0][0][1]:surviver_status_location[0][1][1], surviver_status_location[0][0][0]:surviver_status_location[0][1][0]]
    second_surviver_base_image = preprocessed_image_for_other[surviver_status_location[1][0][1]:surviver_status_location[1][1][1], surviver_status_location[1][0][0]:surviver_status_location[1][1][0]]
    third_surviver_base_image = preprocessed_image_for_other[surviver_status_location[2][0][1]:surviver_status_location[2][1][1], surviver_status_location[2][0][0]:surviver_status_location[2][1][0]]
    fourth_surviver_base_image = preprocessed_image_for_other[surviver_status_location[3][0][1]:surviver_status_location[3][1][1], surviver_status_location[3][0][0]:surviver_status_location[3][1][0]]

    surviver_status_path_list = os.listdir(surviver_status_template_path)
    first_surviver_status = get_most_reliable_template(surviver_status_template_path, surviver_status_path_list, first_surviver_base_image)
    second_surviver_status = get_most_reliable_template(surviver_status_template_path, surviver_status_path_list, second_surviver_base_image)
    third_surviver_status = get_most_reliable_template(surviver_status_template_path, surviver_status_path_list, third_surviver_base_image)
    fourth_surviver_status = get_most_reliable_template(surviver_status_template_path, surviver_status_path_list, fourth_surviver_base_image)

    print("サバイバーステータス1: {}".format(first_surviver_status[0]))
    print("サバイバーステータス2: {}".format(second_surviver_status[0]))
    print("サバイバーステータス3: {}".format(third_surviver_status[0]))
    print("サバイバーステータス4: {}".format(fourth_surviver_status[0]))

    rectangle(base_image, surviver_status_location[0][0][0], surviver_status_location[0][0][1], surviver_status_location[0][1][0], surviver_status_location[0][1][1])
    rectangle(base_image, surviver_status_location[1][0][0], surviver_status_location[1][0][1], surviver_status_location[1][1][0], surviver_status_location[1][1][1])
    rectangle(base_image, surviver_status_location[2][0][0], surviver_status_location[2][0][1], surviver_status_location[2][1][0], surviver_status_location[2][1][1])
    rectangle(base_image, surviver_status_location[3][0][0], surviver_status_location[3][0][1], surviver_status_location[3][1][0], surviver_status_location[3][1][1])

    # サバイバーパークの画像認識
    surviver_perks = []
    surviver_perk_path_list = os.listdir(surviver_perk_template_path)
    # i人目のパーク
    for i in range(4):
        surviver_perks_i = []
        # j個目のパーク
        for j in range(4):
            left_top_x = surviver_perk_location[0][j] - location_buffer
            left_top_y = surviver_perk_location[1][i] - location_buffer
            bottom_right_x = left_top_x + 46 + (location_buffer * 2)
            bottom_right_y = left_top_y + 46 + (location_buffer * 2)
            
            perk_base_image = preprocessed_image_for_perk[left_top_y:bottom_right_y, left_top_x:bottom_right_x]

            rectangle(base_image, left_top_x, left_top_y, bottom_right_x, bottom_right_y)

            surviver_perks_i.append(get_most_reliable_template(surviver_perk_template_path, surviver_perk_path_list, perk_base_image, 2))
        surviver_perks.append(surviver_perks.append(surviver_perks_i))
        print("{}人目サバイバーパーク: {} / {} / {} / {}".format(i+1, surviver_perks_i[0][0], surviver_perks_i[1][0], surviver_perks_i[2][0], surviver_perks_i[3][0]))

    # サバイバーアイテムの画像認識
    surviver_items = []
    surviver_item_types = []
    surviver_item_path_list = os.listdir(surviver_item_template_path)
    # i人目のアイテム
    for i in range(4):
        left_top_x = surviver_item_location_x - location_buffer
        left_top_y = surviver_item_location_y[i] - location_buffer
        bottom_right_x = left_top_x + surviver_item_width + (location_buffer * 2)
        bottom_right_y = left_top_y + surviver_item_width + (location_buffer * 2)
        
        item_base_image = preprocessed_image_for_other[left_top_y:bottom_right_y, left_top_x:bottom_right_x]

        rectangle(base_image, left_top_x, left_top_y, bottom_right_x, bottom_right_y)
        result = get_most_reliable_template(surviver_item_template_path, surviver_item_path_list, item_base_image)
        f = open(item_type_path, 'r', encoding='utf-8')
        surviver_item_type_dict = json.load(f)
        surviver_item_types.append(surviver_item_type_dict[result[0]])
        surviver_items.append((result[0]))
        print("{}人目サバイバーアイテム: {}".format(i+1, surviver_items[i]))

    # サバイバーアドオンの画像認識
    surviver_addons = []
    for i in range(4):
        surviver_addon_path_i = "{}/{}".format(surviver_addon_template_path, surviver_item_types[i])
        surviver_addon_path_list = os.listdir(surviver_addon_path_i)
        surviver_addon_i = []
        for j in range(2):
            left_top_x = surviver_addon_location_x[j] - location_buffer
            left_top_y = surviver_addon_location_y[i] - location_buffer
            bottom_right_x = left_top_x + surviver_addon_width + (location_buffer * 2)
            bottom_right_y = left_top_y + surviver_addon_width + (location_buffer * 2)

            addon_base_image = preprocessed_image_for_other[left_top_y:bottom_right_y, left_top_x:bottom_right_x]
            rectangle(base_image, left_top_x, left_top_y, bottom_right_x, bottom_right_y)
            result = get_most_reliable_template(surviver_addon_path_i, surviver_addon_path_list, addon_base_image)
            surviver_addon_i.append(result[0])
        surviver_addons.append(surviver_addon_i)
        print("{}人目アイテムアドオン: {} / {}".format(i+1, surviver_addons[i][0], surviver_addons[i][1]))



            


    show_image(base_image)

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def image_preprocess(img, C=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
    threshold = cv2.adaptiveThreshold(gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, C)
    return threshold

def get_most_reliable_template(base_path, template_path_list, base_image, C=None):
    results = {}
    for i in template_path_list:
        path = "{}/{}".format(base_path, i)
        template = image_preprocess(imread(path), C)
        result = template_match(template, base_image)
        basename = i.split('.')[0]
        results[basename] = result
    results = sorted(results.items(), key=lambda x:x[1], reverse=True)

    return results[0]

def template_match(template, base_image):
    result = cv2.matchTemplate(base_image, template, cv2.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc, min_val

def rectangle(base_image, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    top_left = (top_left_x, top_left_y)
    bottom_right = (bottom_right_x, bottom_right_y)
    cv2.rectangle(base_image, top_left, bottom_right, (255, 255, 0), 2)
    return

def show_image(image, title="base"):
    cv2.imshow(title, image)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()