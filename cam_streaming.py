import cv2
import socket
import struct
import traceback


class Cam_Streaming:

    TARGET_IP = "127.0.0.1" 
    TARGET_PORT = 5005
    

    def __init__(self):
        self.seq_id = 0
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.initialized = True
        except Exception as ex:
            self.initialized = False
            traceback.print_exception(ex)

    def run(self):
        try:
            while(self.initialized):
                ret, frame = self.cap.read()
                if ret:
                    print(f"Streaming to {self.TARGET_IP}:{self.TARGET_PORT}...")
                    _, img_encoded = cv2.imencode(".jpg",frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                    data = img_encoded.tobytes()

                    header = struct.pack('<I', self.seq_id)
                    self.udp_socket.sendto(header+data, (self.TARGET_IP, self.TARGET_PORT))
                    self.seq_id+=1
        except Exception as ex:
            traceback.print_exception(ex)
        finally:
            self.close()
        

    def close(self):
        self.initialized = False
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'udp_socket'):
            self.udp_socket.close()

def main():
    cam_streaming = Cam_Streaming()
    cam_streaming.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        traceback.print_exception()
