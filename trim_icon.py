import cv2
import os
import numpy as np

addon_reference_path = "./database/reference/surviver/addon/light"
perk_reference_path = "./database/reference/killer/perk"
output_path = "./database/surviver/addon/light/"
# killer addon 0 / surviver addon 1 / perk 2 / surviver item 3 / 単発アドオン 3
trim_mode = 3

addon_location = [
    [[398, 561], [486, 649]],
    [[510, 561], [598, 649]],
    [[622, 561], [710, 649]],
    [[736, 561], [824, 649]],
    [[848, 561], [936, 649]],
    [[398, 671], [486, 759]],
    [[510, 671], [598, 759]],
    [[622, 671], [710, 759]],
    [[736, 671], [824, 759]],
    [[848, 671], [936, 759]],
    [[398, 781], [486, 869]],
    [[510, 781], [598, 869]],
    [[622, 781], [710, 869]],
    [[736, 781], [824, 869]],
    [[848, 781], [936, 869]]
]

# パークはすべて100×100のためrightDownの座標は(+100, +100)
perk_base_left_top_location = [
    [333, 562],
    [458, 562],
    [582, 562],
    [706, 562],
    [831, 562],
    [397, 653],
    [522, 653],
    [646, 653],
    [770, 653],
    [894, 653],
    [333, 747],
    [458, 747],
    [582, 747],
    [706, 747],
    [831, 747],
]

crop_location = np.array([
    (0, 50),
    (50, 100),
    (100, 50),
    (50, 0)
])

def main():
    if trim_mode == 0 or trim_mode == 1 or trim_mode == 3:
        addon_reference_path_list = os.listdir(addon_reference_path)
        print(addon_reference_path_list)
        if trim_mode == 3:
            for index, i in enumerate(addon_reference_path_list):
                base_image = imread("{}/{}".format(addon_reference_path, i))
                for j in range(15):
                    addon_image = base_image[addon_location[j][0][1]:addon_location[j][1][1], addon_location[j][0][0]:addon_location[j][1][0]]
                    addon_image = cv2.resize(addon_image, (37, 37))
                    imwrite("{}{}_{}.png".format(output_path, index, j), addon_image)
        else:
            for i in addon_reference_path_list:
                preference_list = os.listdir("{}/{}".format(addon_reference_path, i))
                print("{}/{}/{}".format(addon_reference_path, i, preference_list[0]))
                base_image_1 = imread("{}/{}/{}".format(addon_reference_path, i, preference_list[0]))
                
                for j in range(15):
                    addon_image = base_image_1[addon_location[j][0][1]:addon_location[j][1][1], addon_location[j][0][0]:addon_location[j][1][0]]
                    addon_image = cv2.resize(addon_image, (37, 37))
                    imwrite("{}/{}/{}.png".format(output_path, i, j), addon_image)

                if trim_mode == 0:
                    base_image_2 = imread("{}/{}/{}".format(addon_reference_path, i, preference_list[1]))
                    for j in range(5):
                        addon_image = base_image_2[addon_location[j][0][1]:addon_location[j][1][1], addon_location[j][0][0]:addon_location[j][1][0]]
                        addon_image = cv2.resize(addon_image, (37, 37))
                        imwrite("{}/{}/{}.png".format(output_path, i, j + 15), addon_image)
    elif trim_mode == 2:
        perk_reference_list = os.listdir(perk_reference_path)
        for i, file in enumerate(perk_reference_list):
            base_image = imread("{}/{}".format(perk_reference_path, file))
            
            for j in range(15):
                left_top_x = perk_base_left_top_location[j][0]
                left_top_y = perk_base_left_top_location[j][1]
                bottom_right_x = left_top_x + 100
                bottom_right_y = left_top_y + 100
                base_perk_image = base_image[left_top_y:bottom_right_y, left_top_x:bottom_right_x]
                base_perk_image = cv2.cvtColor(base_perk_image, cv2.COLOR_BGR2BGRA)
                mask = np.ones((100, 100), dtype=np.uint8)
                gb_mask = cv2.fillConvexPoly(np.tile(np.array([0, 255, 0], dtype=np.uint8), (100, 100, 1)), crop_location, (0.0, 0.0, 0.0), cv2.LINE_AA)
                
                cv2.fillConvexPoly(mask, crop_location, (0.0, 0.0, 0.0), cv2.LINE_AA)
                mask = mask == 1

                base_perk_image[mask, :] = [0, 0, 0, 0]
                imwrite("{}/{}_{}.png".format(output_path, i, j), base_perk_image)

                # cv2.imshow("test2", base_perk_image)
                # cv2.waitKey(0) 
                # cv2.destroyAllWindows()
                


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    main()