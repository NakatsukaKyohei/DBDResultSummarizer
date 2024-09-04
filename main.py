import cv2
import os
import numpy as np

killer_template_path = "./database/killer/"
addon_template_path = "./database/addon/"
surviver_status_template_path = "./database/surviver_status/"
base_image_path = './database/result/怨霊.png'

# アイコンの位置ずれを想定した位置バッファ
location_buffer = 10

# アドオンアイコンの位置
# n個目のアドオン / 左上 or 右下 / x座標 or y座標
addon_location = [
    [[550 - location_buffer, 794 - location_buffer], [591 + location_buffer, 835 + location_buffer]],
    [[597 - location_buffer, 794 - location_buffer], [637 + location_buffer, 835 + location_buffer]]
]

# キラーアイコンの位置
killer_location = [[484 - location_buffer, 794 - location_buffer], [524 + location_buffer, 835 + location_buffer]] 

# サバイバーステータスのアイコンの位置
# n人目のステータス / 左上 or 右下 / x座標 or y座標
surviver_status_location = [
    [[180 - location_buffer, 264 - location_buffer], [212 + location_buffer, 289 + location_buffer]],
    [[180 - location_buffer, 378 - location_buffer], [212 + location_buffer, 408 + location_buffer]],
    [[180 - location_buffer, 499 - location_buffer], [212 + location_buffer, 526 + location_buffer]],
    [[180 - location_buffer, 619 - location_buffer], [212 + location_buffer, 647 + location_buffer]]
]

def main():
    base_image = imread(base_image_path)

    # キラーの画像認識
    killer_base_image = base_image[killer_location[0][1]:killer_location[1][1], killer_location[0][0]:killer_location[1][0]]
    killer_type = get_most_reliable_template(killer_template_path, os.listdir(killer_template_path), killer_base_image)
    print("キラー: {}".format(killer_type))

    rectangle(base_image, killer_location[0][0], killer_location[0][1], killer_location[1][0], killer_location[1][1])

    # アドオンの画像認識
    first_addon_base_image = base_image[addon_location[0][0][1]:addon_location[0][1][1], addon_location[0][0][0]:addon_location[0][1][0]]
    second_addon_base_image = base_image[addon_location[1][0][1]:addon_location[1][1][1], addon_location[1][0][0]:addon_location[1][1][0]]

    addon_path_list = os.listdir(addon_template_path + killer_type[0])
    first_addon = get_most_reliable_template(addon_template_path + killer_type[0], addon_path_list, first_addon_base_image)
    second_addon = get_most_reliable_template(addon_template_path + killer_type[0], addon_path_list, second_addon_base_image)
    print("使用アドオン1: {}".format(first_addon[0]))
    print("使用アドオン2: {}".format(second_addon[0]))

    rectangle(base_image, addon_location[0][0][0], addon_location[0][0][1], addon_location[0][1][0], addon_location[0][1][1])
    rectangle(base_image, addon_location[1][0][0], addon_location[1][0][1], addon_location[1][1][0], addon_location[1][1][1])

    # サバイバーステータスの画像認識
    first_surviver_base_image = base_image[surviver_status_location[0][0][1]:surviver_status_location[0][1][1], surviver_status_location[0][0][0]:surviver_status_location[0][1][0]]
    second_surviver_base_image = base_image[surviver_status_location[1][0][1]:surviver_status_location[1][1][1], surviver_status_location[1][0][0]:surviver_status_location[1][1][0]]
    third_surviver_base_image = base_image[surviver_status_location[2][0][1]:surviver_status_location[2][1][1], surviver_status_location[2][0][0]:surviver_status_location[2][1][0]]
    fourth_surviver_base_image = base_image[surviver_status_location[3][0][1]:surviver_status_location[3][1][1], surviver_status_location[3][0][0]:surviver_status_location[3][1][0]]

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
    # print(results)
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



if __name__ == "__main__":
    main()