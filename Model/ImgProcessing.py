from tkinter import filedialog
import cv2
import numpy as np
import pyperclip
from PIL import Image, ImageTk
from Model.LoadJson import LoadJson


def goodSize(img):
    ret, imgThresh = cv2.threshold(img, 200, 255, type=cv2.THRESH_BINARY_INV)
    con = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    con = con[0]
    newSize = []
    for index, contour in enumerate(con):
        (x, y, w, h) = cv2.boundingRect(contour)
        newSize = (x, y, w, h)
    return newSize
def openedImg(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img
def sobelEx(img, xaxis=1, yaxis=0):
    x = cv2.Sobel(img, ddepth=cv2.CV_64F, dx=xaxis, dy=yaxis, ksize=-1)
    x = np.absolute(x)
    (min_val, max_val) = (np.min(x), np.max(x))
    x = (255 * ((x - min_val) / (max_val - min_val)))
    x = x.astype(np.uint8)
    return x


def extract(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    open_morph = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    o = img - open_morph
    cv2.imwrite("C:/Users/Lenovo/Desktop/open_morph.jpg", o)
    return img - open_morph


def doubleSobelEx(img):
    x = sobelEx(img, xaxis=1, yaxis=0)
    y = sobelEx(img, xaxis=0, yaxis=1)
    return x + y


def closedImg(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 15))
    imgMorph = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    ret, img = cv2.threshold(imgMorph, 70, 255, cv2.THRESH_BINARY)
    cv2.imwrite("C:/Users/Lenovo/Desktop/close.jpg", img)
    return img


def initTemple():
    template = cv2.imread("assets/cardnumber.png")
    gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    gray_temp = cv2.threshold(gray_temp, 10, 255, cv2.THRESH_BINARY_INV)[1]
    contours = cv2.findContours(gray_temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    digitsBox = [cv2.boundingRect(contour) for contour in contours]
    digitsBox = sorted(digitsBox, key=lambda x: x[0])
    maxWidth = max([digit[2] for digit in digitsBox])
    maxHeight = max([digit[3] for digit in digitsBox])
    digits = {}  # krotka
    for (index, box) in enumerate(digitsBox):
        (x, y, w, h) = box
        roi = gray_temp[y:y + h, x:x + w]
        roi = cv2.resize(roi, (maxWidth, maxHeight))
        roi = cv2.threshold(roi, 10, 255, cv2.THRESH_BINARY_INV)[1]
        digits[index] = roi
    return digits


class ImgProcessing:
    def __init__(self):
        self.imgPIL = None
        self.file_path = None
        self.file_pathJson = None
        self.imgCV = None
        self.code = None
        self.label = None
        self.goodBox = []
        self.ratio1 = None
        self.ratio2 = None
        self.w1 = None
        self.w2 = None
        self.h1 = None
        self.h2 = None
        self.thresh = None
        self.loadJson = LoadJson()
        self.importSettings()

    def setParameter(self, setting):
        self.ratio1 = setting["ratio1"]
        self.ratio2 = setting["ratio2"]
        self.w1 = setting["w1"]
        self.w2 = setting["w2"]
        self.h1 = setting["h1"]
        self.h2 = setting["h2"]
        self.thresh = setting["thresh"]
    def importSettings(self):
        setting, _ = self.loadJson.importSetting(
            path=r"C:\Users\Lenovo\Desktop\pythonProject\Assets\cardcode_setting.json")
        if setting is not None:
            self.setParameter(setting)
        print(f"IMPORT: {self.ratio1}")
    def useSettings(self, setting):
        if setting is not None:
            self.setParameter(setting)
        print(f"USE: {self.ratio1}")

    def openTk(self, w, h):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.file_path:
            self.imgPIL = Image.open(self.file_path)
            img = self.imgPIL.resize((w, h))
            tk_image = ImageTk.PhotoImage(img)
            return tk_image

    def saveTk(self):
        if self.code is not None:
            pyperclip.copy(self.code)
        if self.imgPIL is not None:
            new_path = self.file_path.split("/")
            new_path[-1] = "TEST_" + new_path[-1]
            new_path = "/".join(new_path)
            self.imgPIL.save(new_path)
            self.label = "Zapisano plik oraz skopiowano kod"
        else:
            self.label = "Nie wybrano pliku"
        return self.label

    def getContours(self, img):
        con = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        con = con[0]
        print(f"con: {len(con)}")
        goodBox = []
        for index, contour in enumerate(con):
            (x, y, w, h) = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            print(f"aspect_ratio:{aspect_ratio}")
            if self.ratio1 < aspect_ratio < self.ratio2:
                print(f"w:{w} h:{h}")
                if (self.w1 < w < self.w2) and (self.h1 < h <self.h2):
                    goodBox.append((x, y, w, h))
        self.goodBox = sorted(goodBox, key=lambda x: x[0])

    def getDigit(self, org_img):
        cardNumber = []
        gray_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
        for (i, (xB, yB, wB, hB)) in enumerate(self.goodBox):
            group_result = []
            # z orginalnego obrazu wycinamy tylko fragmenty, które nas interesują + padding 5px
            group = gray_img[yB - 5:yB + hB + 5, xB - 5:xB + wB + 5]
            ret, thresh_group = cv2.threshold(group, 141, 255, cv2.THRESH_BINARY)

            # na czarno-bialy lepiej wyciaga się kontury
            digit = cv2.findContours(thresh_group, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            digit = digit[0]
            ret, thresh_group = cv2.threshold(thresh_group, self.thresh, 255, cv2.THRESH_BINARY_INV)
            # boxujemy każda cyfre je i sortujemy
            digitBox = [cv2.boundingRect(contour) for contour in digit]
            digitBox = sorted(digitBox, key=lambda x: x[0])
            # wyciagamy kazda cyfre i resizujemy ja do wielkosci wzornika
            for j, box in enumerate(digitBox):
                (x, y, w, h) = box
                # wycinamy cyfry z czarno-białego boxa
                roi = thresh_group[y:y + h, x:x + w]
                roi = cv2.resize(roi, (54, 85))

                predict = []
                digits = initTemple()
                for (digit, digitRoi) in digits.items():
                    result = cv2.matchTemplate(roi, digitRoi, cv2.TM_CCOEFF)
                    (_, score, _, _) = cv2.minMaxLoc(result)
                    predict.append(score)
                group_result.append(str(np.argmax(predict)))
                org_img = cv2.rectangle(org_img, (xB - 5, yB - 5), (xB + wB + 5, yB + hB + 5), color=(0, 255, 0))
                org_img = cv2.putText(org_img, "".join(group_result), (xB, yB - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                                      (0, 255, 0), 2)
                if j == 3:
                    break
            cardNumber.extend(group_result)
        self.code = str("".join(cardNumber))
        pyperclip.copy(self.code)
        return org_img

    def OCR(self):
        if self.file_path is None:
            print("Nie wybrano obrazu")
            self.label = "Nie wybrano obrazu"
        else:
            self.imgCV = cv2.imread(self.file_path)
            imgGraySIZE = cv2.cvtColor(self.imgCV, cv2.COLOR_BGR2GRAY)
            self.imgCV = cv2.cvtColor(self.imgCV, cv2.COLOR_BGR2RGB)
            cv2.imwrite("C:/Users/Lenovo/Desktop/oldSizeSelf.jpg", self.imgCV)
            size = goodSize(imgGraySIZE)
            (x, y, w, h) = size
            self.imgCV = self.imgCV[y:h, x:w]
            cv2.imwrite("C:/Users/Lenovo/Desktop/cutSelf.jpg",self.imgCV)
            self.imgCV = cv2.resize(self.imgCV, (600, 400), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("C:/Users/Lenovo/Desktop/newSizeSelf.jpg", self.imgCV)
            img = self.imgCV
            cv2.imwrite("C:/Users/Lenovo/Desktop/newSizeIMG.jpg", img)
            img = openedImg(img)
            img = extract(img)
            img = doubleSobelEx(img)
            img = closedImg(img)
            self.getContours(img)
            img = self.getDigit(self.imgCV)
            self.imgPIL = Image.fromarray(img)

        return self.imgPIL, self.label
