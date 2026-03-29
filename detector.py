import cv2
import easyocr

reader = easyocr.Reader(['en'])

def detect_ambulance(frame):
    results = reader.readtext(frame)
    found = False

    for (bbox, text, prob) in results:
        text = text.upper()

        if "AMBULANCE" in text:
            found = True

            (top_left, _, bottom_right, _) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(frame, text, top_left,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0), 2)

    return frame, found


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output, detected = detect_ambulance(frame)

    if detected:
        print("AMBULANCE DETECTED → GREEN SIGNAL")

    cv2.imshow("Detection", output)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()