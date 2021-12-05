from ppadb.client import Client as AdbClient
from PIL import Image
import io, time
import cv2  
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def handler(connection):
	# while True:
	#	 data = connection.read(1024)
	#	 if not data:
	#		 break
	#	 print(data.decode('utf-8'))

	# connection.close()
	file_obj = connection.socket.makefile()
	while True:
		line = file_obj.readline().strip()
		if line == "":
			break
		print(line)

client = AdbClient(host="127.0.0.1", port=5037)
print("Connected")

print("Devices:",client.devices())

device = client.device("127.0.0.1:5555")

# device.shell('pm list packages -f',handler=handler)

device.shell("monkey -p com.easybrain.nonogram -c android.intent.category.LAUNCHER 1",handler=handler)
time.sleep(1)
device.input_tap(450,1250)

result = device.screencap()

# img = Image.open(io.BytesIO(result))
img = cv2.imdecode(np.frombuffer(result, np.uint8), cv2.IMREAD_COLOR)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# cv2.imshow('img', img)
# cv2.waitKey(0)
# image = cv2.imread("Large.png")
# template = cv2.imread("small.png")
# result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)  
# print(np.unravel_index(result.argmax(),result.shape))
width,height = 70,156
x,y = 169,300
for i in range(10):
	x1,y1,x2,y2 = x+width*i, y, x+width*(i+1), y+height
	org_crop = img[y1:y2, x1:x2]
	crop = cv2.resize(org_crop, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
	crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
	ret,crop = cv2.threshold(crop,127,255,cv2.THRESH_BINARY)

	# blackY, blackX = np.where(np.all(crop==[0,0,0],axis=2))
	# top, bottom = blackY[0], blackY[-1]
	# left, right = blackX[0], blackX[-1]
	# crop=crop[top:bottom, left:right]

	contours = cv2.findContours(crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # [-2] indexing takes return value before last (due to OpenCV compatibility issues).
	cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
	x, y, w, h = cv2.boundingRect(contours[0])

	cv2.imshow('crop', crop)
	cv2.imshow('original', org_crop)
	cv2.waitKey(0)
	break
	# crop = img.crop((x1,y1,x2,y2))
	data = pytesseract.image_to_string(crop,config=' --psm 3')# -c tessedit_char_whitelist=0123456789')
	print(data)
# img.show(title="yooo")#169,300 - 237,456 / 242,300 - 307,456 / 313,300 -> 875,456 - 378,456 - 65x156 + 5