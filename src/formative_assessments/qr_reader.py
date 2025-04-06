import json

import cv2


def get_metadata_from_qr(image_filepath):

    image = cv2.imread(image_filepath)
    image = image[0:image.shape[0]//2, image.shape[1]//2: image.shape[1]]
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is None:
        print("ERROR: Could not find a QR code in the image - {}".format(image_filepath))
    metadata = json.loads(data)
    return metadata
