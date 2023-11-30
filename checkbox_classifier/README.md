# DGFIP Checkbox Classifier

## Overview
Binary classifier for checkboxes in DGFIP forms

## Retrieving the Model File

To run the project, you need to download the necessary `.h5` model file. Follow the steps below to download the file using Python.

### Prerequisites

Ensure you have Python installed on your system. You'll also need the `gdown` package to download the file from Google Drive. You can install it using pip:

 ``pip install gdown``  

### Downloading the File

Run the following Python script to download the `.h5` model file:

```import gdown

url = 'https://drive.google.com/uc?id=1dd_xtCT8Uxi386e2kkZeGSAi5V4Hh9Xv'
output = 'model.h5'
gdown.download(url, output, quiet=False)





