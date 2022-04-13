from view.create_window import *

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = Window()
    ex.show()

    sys.exit(app.exec_())
