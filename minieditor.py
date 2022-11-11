# нужные библиотеки
import sys

import sqlite3
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui_1 import Ui_MainWindow


# класс главного окна приложения
class Editor(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # промежуточное изображение
        self.intermediate_img = 'inter.jpg'
        # конечный результат
        self.new_img = 'final.jpg'
        self.initUI()

    def initUI(self):
        # логотип программы
        self.setWindowIcon(QIcon('logo/logo.ico'))
        self.blur_s.adjustSize()
        self.rotate.adjustSize()
        self.open.clicked.connect(self.open_image)
        self.save.clicked.connect(self.save_image)
        self.red.clicked.connect(self.r_color)
        self.red_slider.valueChanged.connect(self.change_r)
        self.green.clicked.connect(self.g_color)
        self.green_slider.valueChanged.connect(self.change_g)
        self.blue.clicked.connect(self.b_color)
        self.blue_slider.valueChanged.connect(self.change_b)
        self.back.clicked.connect(self.get_back)
        self.rotate_l.clicked.connect(self.l_turn)
        self.rotate_r.clicked.connect(self.r_turn)
        self.negative.clicked.connect(self.negativity)
        self.black_white.clicked.connect(self.black_and_white)
        self.blue_inversion.clicked.connect(self.cl_blue_inversion)
        self.retro_1.clicked.connect(self.cl_retro_1)
        self.retro_2.clicked.connect(self.cl_retro_2)
        self.retro_3.clicked.connect(self.cl_retro_3)
        self.ef_3d1.clicked.connect(self.cl_ef_3d1)
        self.ef_rez.clicked.connect(self.cl_ef_rez)
        self.ef_contur.clicked.connect(self.cl_ef_contur)
        self.pres_retro.clicked.connect(self.cl_pres_retro)
        self.exit.clicked.connect(self.end_of_programm)
        self.BlurSlider.valueChanged.connect(self.change_BlurSlider)
        self.RotateSlider.valueChanged.connect(self.change_RotateSlider)
        self.pres_sakura.clicked.connect(self.cl_pres_sakura)
        self.f_blue.clicked.connect(self.sad_blue)
        self.f_green.clicked.connect(self.sad_green)
        self.f_drawn.clicked.connect(self.cl_f_drawn)
        self.ef_3d2.clicked.connect(self.cl_ef_3d2)
        self.ef_3d3.clicked.connect(self.cl_ef_3d3)
        self.save_as.clicked.connect(self.save_image_as)
        # коэф. поворота
        self.im_ugol = 0

    # cохранения изображения
    def save_image(self):
        new_img = Image.open(self.new_img)
        new_img.save('final.jpg')
        self.save.setText('Сохраненно')
        with open("log.txt", 'a') as file:
            file.write('Сохранить\n')

    # сохранить изображение как
    def save_image_as(self):
        if self.save_as_name.text() and self.save_as_name.text()[-4:] == '.jpg':
            new_img = Image.open(self.new_img)
            new_img.save(self.save_as_name.text())
            self.save_as.setText('Сохраненно')
            self.actions_line.setText('Изображение удачно сохраненно.')
            self.actions_line.setStyleSheet('QLabel {color: green;}')
        elif self.save_as_name.text()[-4:] != '.jpg':
            self.actions_line.setText('Добавьте расширение .jpg, чтобы файл сохранился!')
            self.actions_line.setStyleSheet('QLabel {color: red;}')
        else:
            self.actions_line.setText('Вы не назвали свой файл!')
            self.actions_line.setStyleSheet('QLabel {color: red;}')
        with open("log.txt", 'a') as file:
            file.write('Сохранить как\n')

    # открытие изображения
    def open_image(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выберете изображение:', '',
            'Картинка (*.jpg);;Картинка (*.jpg);;Все файлы (*)')[0]
        '''self.fname.move(300, 300)'''
        if fname:
            self.start_image = fname
            img = Image.open(self.start_image)
            img.save(self.new_img)
            img.save(self.intermediate_img)
            self.pixmap = QPixmap(self.start_image)
            self.image.setPixmap(self.pixmap)
            self.save.setText('Сохранить')
            self.save_as.setText('Сохранить как')
        else:
            self.start_image = self.start_image
        with open("log.txt", 'a') as file:
            file.write('Открыть\n')

    # Обработка клавиатуры
    def keyPressEvent(self, event):
        # Открыть файл
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_F:
                self.open_image()
                with open("log.txt", 'a') as file:
                    file.write('Открыть\n')
        # Сохранить файл
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_S:
                self.save_image()
                with open("log.txt", 'a') as file:
                    file.write('Сохранить\n')
        # Сохранить файл как
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.save_image_as()
                with open("log.txt", 'a') as file:
                    file.write('Сохранить как\n')
        # Закрыть приложение
        if int(event.modifiers()) == Qt.AltModifier:
            if event.key() == Qt.Key_F4:
                self.end_of_programm()
                with open("log.txt", 'a') as file:
                    file.write('Закрыть\n')
        # Вернуть картинку в исходное положение
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_Z:
                self.get_back()
                with open("log.txt", 'a') as file:
                    file.write('Вернуть\n')
        # поворот вправо
        if int(event.modifiers()) == Qt.AltModifier:
            if event.key() == Qt.Key_Right:
                self.r_turn()
                with open("log.txt", 'a') as file:
                    file.write('Вправо\n')
        # поворот влево
        if int(event.modifiers()) == Qt.AltModifier:
            if event.key() == Qt.Key_Left:
                self.l_turn()
                with open("log.txt", 'a') as file:
                    file.write('Влево\n')

    # негатив
    def negativity(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 255 - r, 255 - g, 255 - b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Негатив\n')

    # делает изображение черно-белым
    def black_and_white(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = (r + g + b) // 3, (r + g + b) // 3, (r + g + b) // 3
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Черно-белый\n')

    # фильтр инверсирующий синий
    def cl_blue_inversion(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, g, 255 - b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Инверсия\n')

    # фильтр ретро
    def cl_retro_1(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                if (r + g + b) >= 400:
                    pixels[i, j] = 255, 255, 255
                elif (r + g + b) >= 200:
                    pixels[i, j] = 130, 130, 130
                else:
                    pixels[i, j] = 0, 0, 0
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Ретро\n')

    # фильтр ретро 2
    def cl_retro_2(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                a, b, c = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
                a += 50
                b -= 50
                c = 255 - c
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                pixels[i, j] = a, b, c
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Ретро №2\n')

    # фильтр ретро 3
    def cl_retro_3(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                a, b, c = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
                a -= 50
                b += 50
                c = 255 - c
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                pixels[i, j] = a, b, c
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Ретро №3\n')

    # красный цвет
    def r_color(self):
        img = Image.open(self.start_image)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, 0, 0
        img = img.rotate(self.im_ugol)
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Красный\n')

    # зеленый цвет
    def g_color(self):
        img = Image.open(self.start_image)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 0, g, 0
        img = img.rotate(self.im_ugol)
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Зеленый\n')

    # синий цвет
    def b_color(self):
        img = Image.open(self.start_image)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 0, 0, b
        img = img.rotate(self.im_ugol)
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Синий\n')

    # восстановление изображения
    def get_back(self):
        img = Image.open(self.start_image)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, g, b
        self.im_ugol = 0
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Вернуть\n')

    # 3D
    def cl_ef_3d1(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size

        for i in range(x - 1, 20 - 1, -1):
            for j in range(y):
                r = pixels[i - 20, j][0]
                r, g, b = pixels[i, j]
                pixels[i, j] = r, g, b
        for i in range(20):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 0, g, b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('3D\n')

    # поворот налево
    def l_turn(self):
        img = Image.open(self.new_img)
        img = img.rotate(90)
        self.im_ugol += 90
        self.im_ugol %= 360
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Налево\n')

    # поворот направо
    def r_turn(self):
        img = Image.open(self.new_img)
        img = img.rotate(90)
        self.im_ugol -= 90
        self.im_ugol %= 360
        img = img.transpose(Image.ROTATE_180)
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Направо\n')

    # поворот по слайдеру
    def change_RotateSlider(self):
        slider_value = int(self.RotateSlider.value())
        img = Image.open(self.intermediate_img)
        img = img.rotate(slider_value)
        img.save(self.new_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Поворот по слайдеру\n')

    # изменение кол-ва красного по слайдеру
    def change_r(self):
        slider_value = int(self.red_slider.value())
        self.im_curr = Image.open(self.intermediate_img)
        pixels = self.im_curr.load()
        x, y = self.im_curr.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = slider_value, g, b
        self.im_curr.save(self.new_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Кол-во красного\n')

    # изменение зеленого по слайдеру
    def change_g(self):
        slider_value = int(self.green_slider.value())
        self.im_curr = Image.open(self.intermediate_img)
        pixels = self.im_curr.load()
        x, y = self.im_curr.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, slider_value, b
        self.im_curr.save(self.new_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Кол-во зеленого\n')

    # изменение синего по слайдеру
    def change_b(self):
        slider_value = int(self.blue_slider.value())
        self.im_curr = Image.open(self.intermediate_img)
        pixels = self.im_curr.load()
        x, y = self.im_curr.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, g, slider_value
        self.im_curr.save(self.new_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Кол-во синего\n')

    # размытие по слайдеру
    def change_BlurSlider(self):
        slider_value = int(self.BlurSlider.value())
        img = Image.open(self.intermediate_img)
        img = img.filter(ImageFilter.GaussianBlur(radius=slider_value))
        img.save(self.new_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Размытие\n')

    # резкость
    def cl_ef_rez(self):
        img = Image.open(self.new_img)
        img = img.filter(ImageFilter.SHARPEN)
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Резкость\n')

    # контур
    def cl_ef_contur(self):
        img = Image.open(self.new_img)
        img = img.filter(ImageFilter.CONTOUR)
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Контур\n')

    # 3D №2
    def cl_ef_3d2(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x - 1, 20 - 1, -1):
            for j in range(y):
                g = pixels[i - 20, j][1]
                r, G, b = pixels[i, j]
                pixels[i, j] = r, g, b
        for i in range(20):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, 0, b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('3D №2\n')

    # 3D №3
    def cl_ef_3d3(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x - 1, 20 - 1, -1):
            for j in range(y):
                b = pixels[i - 20, j][2]
                r, g, b = pixels[i, j]
                pixels[i, j] = r, g, b
        for i in range(20):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, g, 0
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('3D №3\n')

    # фильтр "Рисование"
    def cl_f_drawn(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                if (r + g + b) >= 400:
                    pixels[i, j] = 255, 255, 255
                else:
                    pixels[i, j] = 0, 0, 0
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Нарисовать\n')

    # фильтр "Зеленый"
    def sad_green(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = b, g, b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Зеленый\n')

    # фильтр "Синий"
    def sad_blue(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = g, g, b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)
        with open("log.txt", 'a') as file:
            file.write('Синий\n')

    # фильтр для пресета "Сакура"
    def sad_red(self):
        img = Image.open(self.new_img)
        pixels = img.load()
        x, y = img.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, b, b
        img.save(self.new_img)
        img.save(self.intermediate_img)
        self.pixmap = QPixmap(self.new_img)
        self.image.setPixmap(self.pixmap)

    # пресет "Сакура"
    def cl_pres_sakura(self):
        con = sqlite3.connect('sets.db')
        cur = con.cursor()
        result = cur.execute("""SELECT sakura_center FROM NAME_sets""").fetchall()
        for a in result:
            for b in a:
                eval(b)()
        con.close()
        with open("log.txt", 'a') as file:
            file.write('Пресет Сакура\n')

    # пресет "Ретро"
    def cl_pres_retro(self):
        con = sqlite3.connect('sets.db')
        cur = con.cursor()
        result = cur.execute("""SELECT retro_80 FROM NAME_sets""").fetchall()
        for a in result:
            for b in a:
                eval(b)()
        con.close()
        with open("log.txt", 'a') as file:
            file.write('Пресет Ретро\n')

    # пустота для базы данных
    def k(self):
        pass

    # выход
    def end_of_programm(self):
        sys.exit(1)


# проверка исключений
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# функция запуска программы
def main():
    app = QApplication(sys.argv)
    ex = Editor()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


# запуск программы
if __name__ == "__main__":
    main()
