import cv2
import numpy as np

scale_percent = 90

# Define global variables to store mouse click coordinates and HSV thresholds
start_point = None
end_point = None
clicked = False
hsv_lower = np.array([0, 0, 0])  # Initial HSV lower threshold
hsv_upper = np.array([120, 130, 140])  # Initial HSV upper threshold
img = None
pixel_per_cm = 10

# Function to calculate distance between two points
def calculate_distance(p1, p2):
    return (p2[0] - p1[0])

def main(WindowName, image, pixel_per_cm, hl, sl, vl, hu, su, vu):
    
    # Mouse callback function to capture mouse clicks
    def mouse_callback(event, x, y, flags, param):
        global start_point, end_point, clicked

        if event == cv2.EVENT_LBUTTONDOWN:
            start_point = (x, y)
            clicked = True

        elif event == cv2.EVENT_LBUTTONUP:
            end_point = (x, y)
            clicked = False
        
            # Add a new member to dark_spots based on the selected area
            if start_point and end_point:
                selected_area = image[start_point[1]:end_point[1], start_point[0]:end_point[0]]
                hsv_selected = cv2.cvtColor(selected_area, cv2.COLOR_BGR2HSV)
                mask_selected = cv2.inRange(hsv_selected, hsv_lower, hsv_upper)
                contours_selected, _ = cv2.findContours(mask_selected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours_selected) > 0:
                    # Take the first contour (assuming it's the dark spot)
                    contour = contours_selected[0]
                    perimeter = cv2.arcLength(contour, True)
                    area = cv2.contourArea(contour)

    
    # Trackbar callback function to update HSV thresholds
    def trackbar_callback(value):
        global hsv_lower, hsv_upper
        lower_hue = cv2.getTrackbarPos('Lower Hue', WindowName)
        upper_hue = cv2.getTrackbarPos('Upper Hue', WindowName)
        hsv_lower = np.array([lower_hue, 0, 0])
        hsv_upper = np.array([upper_hue, 255, 255])

    # Create trackbars for adjusting HSV thresholds
    cv2.createTrackbar('Lower Hue', WindowName, 0, 179, trackbar_callback)
    cv2.createTrackbar('Upper Hue', WindowName, 41, 179, trackbar_callback)
    
    
    a = 0
    #image_orig = image
    cv2.setMouseCallback(WindowName, mouse_callback)

    while True:
        clone = image.copy()
        
        #hsv_lower = np.array([hl, sl, vl])
        #hsv_upper = np.array([hu, su, vu])

        if start_point and end_point:
            cv2.rectangle(clone, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow(WindowName, clone)

        if not clicked and start_point and end_point:
            selected_area = clone[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            if selected_area.size == 0:
                break
            # Convert the selected area to HSV color space
            hsv = cv2.cvtColor(selected_area, cv2.COLOR_BGR2HSV)

            # Apply the HSV threshold to detect dark spots
            mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

            # Find contours in the thresholded image
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            max_contour = max(contours, key = cv2.contourArea) ###

            for contour in contours:
                cv2.drawContours(selected_area, [contour], -1, (0, 0, 255), 2)
            cv2.drawContours(selected_area, max_contour, -1, (7, 240, 197), 2)
            (x_cont, y_cont, w, h) = cv2.boundingRect(max(contours, key=cv2.contourArea))
            #x_cont += start_point[0]
            #y_cont += start_point[1]
            cv2.rectangle(selected_area, (x_cont, y_cont), (x_cont + w, y_cont + h), (237, 194, 24), 2)
           
            a = (x_cont, y_cont, w, h, (cv2.contourArea(max_contour)/pixel_per_cm**2))
        
        cv2.imshow(WindowName, clone)

        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' to exit
            break

    return a, start_point[0], start_point[1], max_contour

    cv2.destroyAllWindows()
    a = None
    x_cont = 0
    y_cont = 0
    max_contour = None
if __name__ == "__main__":
    img = cv2.imread('test2.jpg')
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

    b, x1, y1, cont = main('Image', img, 10, 0, 0, 0, 150, 130, 130)

cv2.destroyAllWindows()

