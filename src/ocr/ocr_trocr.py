import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import concurrent.futures

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def extract_text_from_image(cropped_image):
    # Convertir l'image PIL en tensor de pixels pour le modèle TrOCR
    pixel_values = processor(cropped_image, return_tensors="pt").pixel_values

    # Générer les IDs à partir du modèle
    generated_ids = model.generate(pixel_values, max_new_tokens=100)

    # Décoder les IDs en texte
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    print(f"Extracted text: {generated_text[:50]}")  # Imprime les 50 premiers caractères du texte extrait
    if len(generated_text) > 50:
        print("...")

    return generated_text.strip() or "No text found in the image."


def draw_boxes_on_image_trocr(image, json_data, nb_ocr):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    elif isinstance(image, str):
        image = Image.open(image)

    draw = ImageDraw.Draw(image)
    strings = []
    data_dict = {}
    cropped_images = []

    # Préparer la liste des images recadrées pour le traitement OCR
    for item in json_data:
        for annotation in item['annotations']:
            for result in annotation['result']:
                if result['type'] == 'labels':

                    value = result['value']
                    x = value['x'] * image.width / 100
                    y = value['y'] * image.height / 100
                    width = value['width'] * image.width / 100
                    height = value['height'] * image.height / 100
                    padding = 5

                    cropped = image.crop((x - padding, y - padding, x + width + padding, y + height + padding))
                    labels = value['labels']
                    if labels:  # Assurez-vous que les étiquettes existent avant de les ajouter.
                        cropped_images.append((cropped, labels[0]))

    print('start parallèle')
    # Exécuter le traitement OCR en parallèle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_ocr = {executor.submit(extract_text_from_image, img): label for img, label in cropped_images}
        for future in concurrent.futures.as_completed(future_to_ocr):
            label = future_to_ocr[future]
            try:
                extracted_text = future.result()
                if extracted_text != "No text found in the image.":
                    strings.append(extracted_text)
                    data_dict[label] = extracted_text
                    color = "green"
                else:
                    color = "red"
                    data_dict[label] = ''
            except Exception as e:
                print(f"An error occurred: {e}")

    # Retourner l'image avec les boîtes dessinées, les chaînes extraites et le dataframe
    df = pd.DataFrame([data_dict])
    return image, strings, df