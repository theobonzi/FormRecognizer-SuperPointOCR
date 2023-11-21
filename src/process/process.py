# resize image
# process_single_image
# process_form_folder

import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import os

def resise_image(image, scale_percent=40):
    """Resize an image to a given scale."""
    #width = int(image.shape[1] * scale_percent / 100)
    #height = int(image.shape[0] * scale_percent / 100)

    width = 1970
    height = 1436
    #print(f"==> Image resized : ({height}x{width})")
    dim = (width, height)
    resized_image = cv2.resize(image, dim)
    return resized_image

def process_single_image(image_path, superpoint, display=False, resize=40):
    """Process an individual image to extract keypoints and descriptors."""

    print(f"==> Processing image: {image_path}...")
    start_time = time.time()
    image = cv2.imread(image_path, 0)
    image = np.float32(image) / 255.0
    
    resised_image = resise_image(image, resize)
    #resised_image = image
    keypoints, descriptors, _ = superpoint.run(resised_image)
        
    if display:
        plt.figure(figsize=(10,10))
        plt.imshow(resised_image, cmap='gray')
        plt.scatter(keypoints[0,:], keypoints[1,:], color='r', s=3)
        plt.show()
        
    print(f"==> Finished processing image. Time taken: {time.time() - start_time:.2f} seconds.")
    return keypoints, descriptors

def process_form_folder(form_folder_path, superpoint):
    """Process all images within a folder."""

    print(f"==> Processing form folder: {form_folder_path}...")
    start_time = time.time()
    keypoints_list, descriptors_list = [], []
    desc_ref = None
    kp_ref = None
    
    folder_name = os.path.basename(form_folder_path)
    
    for image_name in os.listdir(form_folder_path):
        image_path = os.path.join(form_folder_path, image_name)
        
        # Check if the image has the same name as the folder (without file extension)
        name_without_extension, _ = os.path.splitext(image_name)
        
        if image_path.lower().endswith(('.png', '.jpg', '.tif')):
            keypoints, descriptors = process_single_image(image_path, superpoint)
            
            print(folder_name)
            print(name_without_extension)
            if name_without_extension == folder_name:
                print('save ref')
                desc_ref = descriptors
                kp_ref = keypoints
            else:
                keypoints_list.append(keypoints)
                descriptors_list.append(descriptors)
    
    print(f"==> Finished processing form folder. Time taken: {time.time() - start_time:.2f} seconds.")
    
    return keypoints_list, descriptors_list, desc_ref, kp_ref