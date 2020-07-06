import sys
from PIL import Image
import pytesseract
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog
from PyQt5.QtWidgets import QLabel, QGridLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


class ImageDropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText('Drag and Drop Image Here.')
        self.setStyleSheet('''
            QLabel{
                font-size: 27px;
                font-weight: 450;
                border: 4px dashed #aaa;
            } 
        ''')


class OutField(QTextEdit):
    def __init__(self):
        super().__init__()
        # self.setAlignment(Qt.AlignCenter)
        self.setPlaceholderText("Extracted Text Will Be Shown Here")
        self.setStyleSheet('''
            font-size : 20px;
        ''')


class ImgOcrui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("texTract")
        self.setWindowIcon(QIcon('favicon.ico'))
        # self.setStyleSheet('''background-color: #f1faee''')
        self.setGeometry(500, 200, 850, 750)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QGridLayout()
        self.setAcceptDrops(True)
        self.imagelabel = ImageDropLabel()
        self.orlable = QLabel("Or select an image file: ")
        self.orlable.setStyleSheet('''
                    font-size: 18px;
                    
                ''')
        self.btn = QPushButton("Open File")
        self.btn.setStyleSheet('''
            background-color: #275efe;
            padding : 10px;
            border-radius: 18px;
            color : white;
            font-weight: 500;
            ''')
        self.btn.clicked.connect(self.opfile)
        self.savebtn = QPushButton("Save Text")
        self.savebtn.setStyleSheet('''
                    background-color: green;
                    padding : 10px;
                    border-radius: 20px;
                    color : white;
                    font-size: 18px;
                    font-weight: 500;
                    ''')
        self.savebtn.clicked.connect(self.savefile)
        self.outputfield = OutField()
        self.generalLayout.addWidget(self.imagelabel, 0, 0, 5, 4)
        self.generalLayout.addWidget(self.orlable, 5, 1, 2, 1)
        self.generalLayout.addWidget(self.btn, 5, 2, 2, 1)
        self.generalLayout.addWidget(self.outputfield, 7, 0, 6, 4)
        self.generalLayout.addWidget(self.savebtn, 13, 1, 2, 2)
        self._centralWidget.setLayout(self.generalLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            # event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.getoutput(file_path)
            event.accept()
        else:
            event.ignore()

    def paste(self):
        clipboard = QApplication.clipboard()
        md = clipboard.mimeData()
        if md.hasImage():
            img = QImage(md.imageData())
            print("image pasted")
            if not img.isNull():
                # self.undo_stack.push(Replace(img, _('Paste image'), self))
                print("NO IMAGE")
        else:
            # error_dialog(self, _('No image'), _(
            #     'No image available in the clipboard'), show=True)
            print("ERROR")

    # event handler for open file button
    def opfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Image',
                                            'c:\\',
                                            "(*.jpg *.jpeg *.tif *.tiff *.eps *.gif *.bmp *.ico *.icns *.png *.webp)")
        # print(fname)
        file_path = fname[0]
        if len(file_path):
            self.getoutput(file_path)
        else:
            self.outputfield.setText("No Image Selected")

    def getoutput(self, file_path):
        imgtext = pytesseract.image_to_string(Image.open(file_path))
        pixmap = QPixmap(file_path)
        if pixmap.height() >= self.imagelabel.height():
            small_pixmap = pixmap.scaledToHeight(self.imagelabel.height(), Qt.FastTransformation)
        elif pixmap.width() >= self.imagelabel.width():
            small_pixmap = pixmap.scaledToWidth(self.imagelabel.width(), Qt.FastTransformation)
        else:
            small_pixmap = pixmap
        # self.imagelabel.setPixmap(QPixmap(file_path))
        self.imagelabel.setPixmap(small_pixmap)
        self.outputfield.setText(imgtext)

    # event handler for save button
    def savefile(self):
        op = self.outputfield.toPlainText()
        if len(op):
            fname = QFileDialog.getSaveFileName(self, 'Save Text', 'c:\\', '*.txt')
            file_path = fname[0]
            if len(file_path):
                with open(file_path, 'w') as f:
                    f.write(op)


def main():
    imgocr = QApplication(sys.argv)
    view = ImgOcrui()
    view.show()
    sys.exit(imgocr.exec_())


if __name__ == '__main__':
    main()
