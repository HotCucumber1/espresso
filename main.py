import sys
import sqlite3


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        try:
            self.connection = sqlite3.connect('coffee.db')
            self.cursor = self.connection.cursor()
            name = self.cursor.execute("""SELECT variety_name FROM coffee""").fetchall()
            name = [i[0] for i in name]
            self.sort.addItems(name)

        except Exception:
            self.statusbar.showMessage('Ошибка')

        self.showButton.clicked.connect(self.show_result)

    def show_result(self):
        try:
            result = self.cursor.execute(
                """SELECT id, degree_of_roast, grinding, taste_description, price, packing_volume 
                FROM coffee WHERE variety_name = ?""", (self.sort.currentText(),)
            ).fetchall()
            result = result[0]
            self.showID.setText(str(result[0]))
            self.showRoast.setText(str(result[1]))
            self.showGrind.setText(str(result[2]))
            self.showTaste.setText(str(result[3]))
            self.showPrice.setText(str(result[4]))
            self.showVolume.setText(str(result[5]))
        except Exception:
            self.statusbar.showMessage('Ошибка')

    def closeEvent(self, event) -> None:
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = NewWindow()
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
