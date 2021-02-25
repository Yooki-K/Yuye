import sys
from PyQt5.QtWidgets import QApplication
from Yuye import Ui_Widget
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_w = Ui_Widget()
    main_w.show()
    sys.exit(app.exec_())
