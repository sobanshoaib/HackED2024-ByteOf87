import cv2


def barcode_reader(image):
    #decodedImage = cv2.imread(image)
    result, *_ = cv2.barcode.BarcodeDetector().detectAndDecode(image)
    return result


def capture_image():
    capture = cv2.VideoCapture(0)
    print("---------Searching for Barcode---------")
    while True:
        _, babyAbdul = capture.read()
        result = barcode_reader(babyAbdul)
        if len(result) > 0:
            print(result)
            break
        cv2.imshow("Barcode Scanner", babyAbdul)
        if cv2.waitKey(1) == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()
    return result
