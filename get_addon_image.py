import cv2
import os
import numpy as np

addon_reference_path = "./database/addon_reference"
output_path = "./database/addon"

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

def main():
    addon_reference_path_list = os.listdir(addon_reference_path)
    print(addon_reference_path_list)
    for i in addon_reference_path_list:
        preference_list = os.listdir("{}/{}".format(addon_reference_path, i))
        print("{}/{}/{}".format(addon_reference_path, i, preference_list[0]))
        base_image_1 = imread("{}/{}/{}".format(addon_reference_path, i, preference_list[0]))
        
        for j in range(15):
            addon_image = base_image_1[addon_location[j][0][1]:addon_location[j][1][1], addon_location[j][0][0]:addon_location[j][1][0]]
            addon_image = cv2.resize(addon_image, (37, 37))
            imwrite("{}/{}/{}.png".format(output_path, i, j), addon_image)

        base_image_2 = imread("{}/{}/{}".format(addon_reference_path, i, preference_list[1]))
        for j in range(5):
            addon_image = base_image_2[addon_location[j][0][1]:addon_location[j][1][1], addon_location[j][0][0]:addon_location[j][1][0]]
            addon_image = cv2.resize(addon_image, (37, 37))
            imwrite("{}/{}/{}.png".format(output_path, i, j + 15), addon_image)


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