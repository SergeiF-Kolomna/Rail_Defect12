import cv2
import numpy as np

# Global variables
drawing = False
ix, iy = -1, -1
roi_enlarged = np.zeros((512, 512, 3), np.uint8)
contour_image = None
diameter = 5

# Mouse callback function for drawing on enlarged image
def draw_red(event, x, y, flags, param):
    global ix, iy, drawing, roi_enlarged

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(roi_enlarged, (x, y), diameter, (0, 0, 255), -1)
        cv2.imshow('Enlarged ROI', roi_enlarged)

# Mouse callback function for selecting area and drawing rectangles
def draw_rectangle(event, x, y, flags, param):
    global ix, iy,init_x, init_y, drawing, roi_enlarged, image1

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        init_x, init_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(image1, (ix-2, iy-2), (x+1, y+1), (0, 255, 0), 2)
        roi = image1[iy:y, ix:x]
        roi_enlarged = cv2.resize(roi, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
        cv2.imshow('Enlarged ROI', roi_enlarged)

def red_contour_detect(image):
    # Чтение изображения
    #image = cv2.imread(image)

    # Преобразование изображения из BGR в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Определение диапазона красного цвета в HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 100])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Объединение масок
    mask = mask1 + mask2

    # Применение морфологических операций для улучшения результата
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Нахождение контуров на изображении
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Отрисовка контуров на исходном изображении
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    # Отображение результатов
    #cv2.imshow('Original Image', image)
    #cv2.imshow('Mask', mask)
    return (contours)

def change_diameter(val):
    global diameter
    diameter = val

def main(WindowName, image):
    global image1
    # Create a window, and bind the function to the window
    cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
    image1 = image.copy()
    cv2.setMouseCallback(WindowName, draw_rectangle)

    while True:
        cv2.imshow(WindowName, image)
        k = cv2.waitKey(1) & 0xFF

        if k == 27:  # Press 'Esc' to exit
            break
        elif k == 114:  # Press 'r' to switch to drawing mode
            cv2.imshow('Enlarged ROI', np.zeros((512, 512, 3), np.uint8))  # Clear the enlarged ROI window
            cv2.createTrackbar('Size', 'Enlarged ROI', 1, 15, change_diameter)
            cv2.setMouseCallback('Enlarged ROI', draw_red)  # Switch to drawing on the enlarged image
            while True:
                cv2.imshow('Enlarged ROI', roi_enlarged)
                k2 = cv2.waitKey(1) & 0xFF
                if k2 == 27:  # Press 'Esc' to exit drawing mode
                    # Extract the red channel
                    contour_image = red_contour_detect(roi_enlarged)
                
                    cv2.drawContours(roi_enlarged, contour_image, -1, (0, 255, 0), 2)
                    #cv2.imshow('Outline of Red Image', roi_enlarged)
                    break

            # Switch back to selecting area and drawing rectangles
            cv2.setMouseCallback(WindowName, draw_rectangle)
        
            for result_contour in contour_image:
                result_contour[:, :, 0] = result_contour[:, :, 0] * 0.2
                result_contour[:, :, 1] = result_contour[:, :,  1] * 0.2
            cv2.drawContours(image, result_contour, -1, (11, 134, 235), 2, offset=(init_x, init_y))
    
    cv2.destroyAllWindows()
    return init_x, init_y, result_contour
    

if __name__ == "__main__":
    img = cv2.imread('test2.jpg')
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

    added_contour = main('Image', img)

cv2.destroyAllWindows()

