import cv2 

class CAMINIT():
    def __init__(self):
        self.camera = cv2.VideoCapture(1)

    
    def generate_frames(self):
        while True:
            ret, frame = self.camera.read()
            buffer,jpeg = cv2.imencode('.jpg',frame)
            if jpeg is not None:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
            


if __name__ == "__main__":
    mylist = [f for f in glob.glob("*.txt")]
        

            