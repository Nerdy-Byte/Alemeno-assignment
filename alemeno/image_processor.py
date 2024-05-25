import cv2
import numpy as np

def process_image(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Image not found or unable to load.")
        return []
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 50, 50])
    upper_bound = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = image.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    block_colors = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        
        if len(approx) == 4:  
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if 0.3 <= aspect_ratio <= 3:  
                block = image[y:y+h, x:x+w]
                average_color = cv2.mean(block)[:3]
                average_color_rgb = (int(average_color[2]), int(average_color[1]), int(average_color[0]))
                block_colors.append(average_color_rgb)
    
    return block_colors
