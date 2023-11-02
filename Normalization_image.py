import cv2

def main_resize(image, short_size_in_pixels):
    # Load the image
    
    #image = cv2.imread(image_name)

    if image is None:
        print('Image not found or cannot be loaded.')
    else:
        # Get the original resolution
        original_height, original_width, _ = image.shape
        print(f'Original Resolution: {original_width}x{original_height}')

        # Determine the target short side length
        target_short_side = short_size_in_pixels

        # Calculate the new dimensions while preserving the aspect ratio
        if original_width < original_height:
            new_width = target_short_side
            new_height = int(original_height * (target_short_side / original_width))
        else:
            new_height = target_short_side
            new_width = int(original_width * (target_short_side / original_height))

        # Resize the image
        resized_image = cv2.resize(image, (new_width, new_height))
        
        # Display the resized image (optional)
        #cv2.imshow('Resized Image', resized_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # Save the resized image
        #cv2.imwrite('resized_image.jpg', resized_image)

        # Print the new resolution
        print(f'New Resolution: {new_width}x{new_height}')

        #Return the resized image (optional)
        return(resized_image)

if __name__ == "__main__":
    image = cv2.imread('test4.jpg')
    img = main_resize(image , 700)
    cv2.imshow('Resized Image', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()

