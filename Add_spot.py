import cv2
import numpy as np
scale_percent = 90

# Define global variables to store mouse click coordinates and HSV thresholds
start_point = None
end_point = None
clicked = False
hsv_lower = np.array([0, 0, 0])  # Initial HSV lower threshold
hsv_upper = np.array([255, 255, 255])  # Initial HSV upper threshold
img = None
pixel_per_cm = 10

# Function to calculate distance between two points
#def calculate_distance(p1, p2):
#    return (p2[0] - p1[0])

# Mouse callback function to capture mouse clicks
def mouse_callback(event, x, y, flags, param):
    global start_point, end_point, clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        clicked = True

    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        clicked = False

# Trackbar callback function to update HSV thresholds
#def trackbar_callback(value):
#    global hsv_lower, hsv_upper
#    lower_hue = cv2.getTrackbarPos('Lower Hue', 'Image')
#    upper_hue = cv2.getTrackbarPos('Upper Hue', 'Image')
#    hsv_lower = np.array([lower_hue, 0, 0])
#    hsv_upper = np.array([upper_hue, 255, 255])

def main(WindowName, image, pixel_per_cm, hl, sl, vl, hu, su, vu):
    a = 0
    image_orig = image
    cv2.setMouseCallback(WindowName, mouse_callback)

    while True:
        clone = image.copy()
        
        hsv_lower = np.array([hl, sl, vl])
        hsv_upper = np.array([hu, su, vu])

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

            #for contour in contours:
                # Calculate linear dimensions and area of each dark spot
                #perimeter = cv2.arcLength(contour, True)
                #area = cv2.contourArea(contour)
            area = cv2.contourArea(max(contours, key=cv2.contourArea))

                # Draw the contour and display dimensions and area
                #cv2.drawContours(selected_area, [contour], -1, (0, 0, 255), 2)

            (x, y, w, h) = cv2.boundingRect(max(contours, key=cv2.contourArea))
                
            a = (x, y, w, h, area)
                #cv2.putText(
                #    selected_area,
                #    f"Perimeter: {perimeter:.2f} pixels",
                #    (10, 30),
                #    cv2.FONT_HERSHEY_SIMPLEX,
                #    0.6,
                #    (0, 0, 255),
                #    2,
                #)
                #cv2.putText(
                #    selected_area,
                #    f"Area: {area:.2f} pixels^2",
                #    (10, 60),
                #    cv2.FONT_HERSHEY_SIMPLEX,
                #    0.6,
                #    (0, 0, 255),
                #    2,
                #)

        cv2.imshow(WindowName, clone)

        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' to exit
            break

    return a

    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = cv2.imread('test2.jpg')
    cv2.namedWindow('Image')

    b = main('Image', img, 10, 0, 0, 0, 150, 130, 130)

cv2.destroyAllWindows()
