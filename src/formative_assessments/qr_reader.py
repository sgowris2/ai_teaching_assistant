import json

import cv2


def get_metadata_from_qr(img_or_path):

    if isinstance(img_or_path, str):
        image = cv2.imread(img_or_path)
    else:
        image = img_or_path
    image = image[0:image.shape[0]//2, image.shape[1]//2: image.shape[1]]
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is None:
        print("ERROR: Could not find a QR code in the image - {}".format(img_or_path))
    metadata = json.loads(data)
    return metadata
