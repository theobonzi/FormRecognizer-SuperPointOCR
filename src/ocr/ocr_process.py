import os
import json
from io import BytesIO
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from src.ocr.ocr_google import extract_text_from_image_google

def draw_boxes_on_image(image, json_data, nb_ocr):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    elif isinstance(image, str):
        image = Image.open(image)

    draw = ImageDraw.Draw(image)
    strings = []
    data_dict = {}

    for item in json_data:
        for annotation in item['annotations']:
            for result in annotation['result']:
                if result['type'] == 'labels':

                    value = result['value']
                    labels = value['labels']
                    
                    x = value['x'] * image.width / 100
                    y = value['y'] * image.height / 100
                    width = value['width'] * image.width / 100
                    height = value['height'] * image.height / 100
                    
                    print('x:', x)
                    print('y:', y)
                    print('width:', width)
                    print('height:', height)

                    padding = 5
                    # Cropper l'image selon le rectangle
                    cropped = image.crop((x - padding, y - padding, x-padding + width+padding, y-padding + height+padding))
                        
                    # Extraire le texte de l'image recadrée
                    extracted_text = "No text found in the image."
                        
                    if (len(strings) < nb_ocr):
                        print('labels:', labels)
                        extracted_text = extract_text_from_image_google(cropped)
                        strings.append(extracted_text)
                        print(extracted_text)

                    # Choisir la couleur en fonction du texte extrait
                    if extracted_text == "No text found in the image.":
                        color = "red"
                        data_dict[labels[0]] = ''
                    else:
                        color = "green"
                        if len(labels) > 0 and labels[0] not in data_dict:
                            extracted_text = extract_text_from_image_google(cropped)
                            data_dict[labels[0]] = extracted_text

                    # Dessiner le rectangle avec la couleur appropriée
                    draw.rectangle([(x - padding, y - padding), (x-padding + width+padding, y-padding + height+padding)], outline=color)
    
    df = pd.DataFrame([data_dict])
    return image, strings, df

from PIL import Image
import os

def filter_labels(data):
    with open('checkbox_labels.json', 'r') as file:
        data = json.load(file)
    valid_labels = set(data["2042"])
    for item in data:
        annotations = item.get("annotations", [])
        for annotation in annotations:
            results = annotation.get("result", [])
            # Filter out labels not in valid_labels
            annotation["result"] = [r for r in results if "labels" in r and any(lbl in valid_labels for lbl in r["value"].get("labels", []))]
    return data

def cut_boxes_on_image(image, json_data):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    elif isinstance(image, str):
        image = Image.open(image)

    strings = []
    data_dict = {}
    cropped_images = []

    # Filter the json_data to only keep checkboxes
    json_data = filter_labels(json_data)

    # Ensure the folder for saving cropped images exists
    save_directory = "cropped_images"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for index, item in enumerate(json_data):
        for annotation in item['annotations']:
            for result in annotation['result']:
                if result['type'] == 'labels':
                    value = result['value']
                    labels = value['labels']
                    
                    x = value['x'] * image.width / 100
                    y = value['y'] * image.height / 100
                    width = value['width'] * image.width / 100
                    height = value['height'] * image.height / 100
                    
                    print('x:', x)
                    print('y:', y)
                    print('width:', width)
                    print('height:', height)

                    padding = 5
                    # Cropping the image according to the rectangle
                    cropped = image.crop((x - padding, y - padding, x + width + padding, y + height + padding))
                    cropped_images.append(cropped)

                    # Save each cropped image
                    save_path = os.path.join(save_directory, f"{image}_{index}.jpg")
                    cropped.save(save_path)


    df = pd.DataFrame([data_dict])
    return cropped_images, strings, df




def draw_boxes(img_path, good_forms, nb_ocr=0):
    base_path = "json_labels"
    image_file_name = f"{good_forms}.json"
    
    full_path_json = os.path.join(base_path, image_file_name)
    with open(full_path_json, 'r') as json_file:
        data = json.load(json_file)
    
    img, strings, df = cut_boxes_on_image(img_path, data, nb_ocr)
    
    return img, strings, df

