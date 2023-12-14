import cv2
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
import pyperclip


def openedImg(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (300, int(img.shape[0] * (300 / img.shape[1]))), interpolation=cv2.INTER_AREA)
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
    return img - open_morph


def doubleSobelEx(img):
    x = sobelEx(img, xaxis=1, yaxis=0)
    y = sobelEx(img, xaxis=0, yaxis=1)
    return x + y


def closedImg(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    imgMorph = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    ret, img = cv2.threshold(imgMorph, 70, 255, cv2.THRESH_BINARY)
    return img


class ImgProcessing:
    def __init__(self):
        self.imgPIL = None
        self.file_path = None
        self.imgCV = None
        self.code = None
        self.label = None
        self.goodBox = []

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

    @staticmethod
    def initTemple():
        template = cv2.imread("assets/cardnumber.png")
        gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        gray_temp = cv2.threshold(gray_temp, 10, 255, cv2.THRESH_BINARY_INV)[1]
        contours = cv2.findContours(gray_temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0]
        digitsbox = [cv2.boundingRect(contour) for contour in contours]
        digitsbox = sorted(digitsbox, key=lambda x: x[0])
        maxwidth = max([digit[2] for digit in digitsbox])
        maxheight = max([digit[3] for digit in digitsbox])
        digits = {}  # krotka
        for (index, box) in enumerate(digitsbox):
            (x, y, w, h) = box
            roi = gray_temp[y:y + h, x:x + w]
            roi = cv2.resize(roi, (maxwidth, maxheight))
            roi = cv2.threshold(roi, 10, 255, cv2.THRESH_BINARY_INV)[1]
            digits[index] = roi
        return digits

    def getContours(self, img):
        con = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        con = con[0]
        goodBox = []
        for index, contour in enumerate(con):
            (x, y, w, h) = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if 2.5 < aspect_ratio < 4.0:
                if (40 < w < 55) and (10 < h < 20):
                    goodBox.append((x, y, w, h))
        self.goodBox = sorted(goodBox, key=lambda x: x[0])
        # return goodBox

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
            print(len(digit))
            ret, thresh_group = cv2.threshold(thresh_group, 127, 255, cv2.THRESH_BINARY_INV)
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
                digits = self.initTemple()
                for (digit, digitRoi) in digits.items():
                    result = cv2.matchTemplate(roi, digitRoi, cv2.TM_CCOEFF)
                    (_, score, _, _) = cv2.minMaxLoc(result)
                    predict.append(score)
                group_result.append(str(np.argmax(predict)))
                org_img = cv2.rectangle(org_img, (xB - 5, yB - 5), (xB + wB + 5, yB + hB + 5), color=(0, 255, 0))
                org_img = cv2.putText(org_img, "".join(group_result), (xB, yB - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                                      (0, 255, 0), 2)
                if j == 3:
                    break
            # numer do skopiowania
            cardNumber.extend(group_result)
        self.code = str(" ".join(cardNumber))
        pyperclip.copy(self.code)
        print(self.code)
        return org_img

    def OCR(self):
        if self.file_path is None:
            print("Nie wybrano obrazu")
            self.label = "Nie wybrano obrazu"
        else:
            self.imgCV = cv2.imread(self.file_path)
            self.imgCV = cv2.cvtColor(self.imgCV, cv2.COLOR_BGR2RGB)
            self.imgCV = cv2.resize(self.imgCV, (600, 400), interpolation=cv2.INTER_CUBIC)
            img = self.imgCV
            print(f"Po wysokość: {img.shape[0]} szerokość: {img.shape[1]}")
            # imgOrg = cv2.resize(img, (300, int(img.shape[0] * (300 / img.shape[1]))), interpolation=cv2.INTER_AREA)
            img = openedImg(img)
            img = extract(img)
            img = doubleSobelEx(img)
            img = closedImg(img)
            self.getContours(img)
            img = self.getDigit(self.imgCV)
            self.imgPIL = Image.fromarray(img)
            print(f"2 Po wysokość: {self.imgPIL.height} szerokość: {self.imgPIL.width}")
        return self.imgPIL, self.label
