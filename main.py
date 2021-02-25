import sys
from PyQt5.QtWidgets import QApplication
from Yuye import Ui_Widget
from lrc import Lrc
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_w = Ui_Widget()
    main_w.show()
    # w = Lrc()
    sys.exit(app.exec_())
