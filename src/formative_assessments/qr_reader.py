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
    try:
        metadata = json.loads(data)
    except Exception as e:
        raise Exception('Invalid QR code data: {}'.format(e))
    return metadata
