import cv2
import numpy as np
import time
from src.process.process import process_single_image, resise_image
from src.process.train_process import load_models
from src.superpoint.superpoint import initialize_superpoint

def find_best_match(image_path, trained_models, superpoint):
    max_matches = 0
    best_matching_form = None
    best_kp_ref = None
    best_good_matches = None

    print(f"==> Finding best matching form for image: {image_path}...")
    start_time = time.time()

    keypoints, descriptors = process_single_image(image_path, superpoint, display=False)
    descriptors = np.ascontiguousarray(descriptors)

    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)


    for form_name, model_data in trained_models.items():
        desc_ref = model_data['desc']
        kp_ref = model_data['kp']

        ###Good matches
        matches = bf.knnMatch(np.float32(descriptors).T, np.float32(desc_ref).T, k=2)
        good_matches = [m for m, n in matches if m.distance < 0.70 * n.distance]

        nb_good_matches = len(good_matches)
        print(f"{nb_good_matches} good matches found for form {form_name}.")
        
        if nb_good_matches > max_matches:
            max_matches = nb_good_matches
            best_matching_form = form_name
            best_good_matches = good_matches
            best_kp_ref = kp_ref

    print(keypoints.shape)
    print(best_kp_ref.shape)
    
    src_pts = np.float32([[keypoints[0, m.queryIdx], keypoints[1, m.queryIdx]] for m in best_good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([[best_kp_ref[0, m.trainIdx], best_kp_ref[1, m.trainIdx]] for m in best_good_matches]).reshape(-1, 1, 2)
            
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    image = cv2.imread(image_path, 0)
    image = resise_image(image)

    print(best_kp_ref.shape)

    height, width = image.shape
    transformed_image = cv2.warpPerspective(image, H, (width, height))

    img_rgb = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB)

    print(f"==> Best matching form found. Time taken: {time.time() - start_time:.2f} seconds.")
    return best_matching_form, keypoints, img_rgb

def inference(test_image_path, path_models):
    superpoint = initialize_superpoint()
    trained_models = load_models(path_models)
    print("==> Starting inference phase...")
    start_time = time.time()

    best_matching_form, keypoints, img = find_best_match(test_image_path, trained_models, superpoint)

    print(f"The best matching form for the test image is {best_matching_form}.")
    print(f"==> Inference phase completed. Total time taken: {time.time() - start_time:.2f} seconds.")  

    return best_matching_form, keypoints, img