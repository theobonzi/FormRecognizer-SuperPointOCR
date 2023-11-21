from google.cloud import vision_v1
from google.oauth2 import service_account
from google.cloud.vision_v1 import types

import os
import json
from io import BytesIO
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw


def extract_text_from_image_google(image, language_hints='fr', bounding_poly=None):
    """
    Extracts text from an image file using Google Cloud Vision API.

    Parameters:
        image_path (str): The path to the image file.
        credentials_path (str): The path to the service account key file.
        language_hints (list of str): Optional - BCP-47 language codes.
        bounding_poly (list of dict): Optional - Vertices of the bounding polygon.

    Returns:
        str: Extracted text from the image.
    """
    credentials_path = 'google-cloud-vision/mythical-temple-398110-51b8df2184f0.json'

    # Specify the path to the service account key file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )

    # Instantiates a client
    client = vision_v1.ImageAnnotatorClient(credentials=credentials)

    content = image_to_byte_array(image)

    image = types.Image(content=content)

    # Prepare image context using language hints and bounding polygon if provided
    image_context = types.ImageContext(
        language_hints=language_hints,
        text_detection_params=types.TextDetectionParams(
            polygon_vertex_constraints=bounding_poly
        ) if bounding_poly else None
    )

    # Performs text detection on the image file
    response = client.document_text_detection(image=image, image_context=image_context)
    texts = response.text_annotations

    # Extract and return the text from the response
    if texts:
        return texts[0].description
    else:
        return "No text found in the image."
    
def image_to_byte_array(image: Image.Image) -> bytes:
    img_byte_arr = BytesIO()
    image = image.convert('RGB')
    image.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()