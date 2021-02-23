# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lrc.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re
import setting as st

def setPix(this: QtWidgets.QWidget, url):
    pal = this.palette()
    pal.setBrush(this.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(url)))
    this.setPalette(pal)


class Ui_pop(QWidget):
    sendclickitem = QtCore.pyqtSignal(str)

    def __init__(self, name_list: list, x, y):
        super().__init__(None)
        self.setStyleSheet("QListWidget::Item { border:0px solid rgb(175, 177, 179);"
                           "border-bottom:1px solid rgb(175, 177, 179);}"
                           "QListWidget::Item:hover{background:rgb(75, 110, 175); }"
                           "QListWidget{background-color:rgb(60,63,65);color:white;outline:0px};")
        self.v = QVBoxLayout(self)
        self.v.setObjectName("v")
        self.lw = QListWidget(parent=self)
        self.lw.setObjectName('lw')
        self.setLayout(self.v)
        self.v.addWidget(self.lw)
        max_len = 0
        for xx in name_list:
            l = 0
            for xxx in xx:
                if u'\u4e00' <= xxx <= u'\u9fff':
                    l += 2
                else:
                    l += 1
            if l > max_len:
                max_len = l
        self.lw.setFixedWidth(max_len * 10)
        self.lw.setFixedHeight(len(name_list) * 25)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.lw.addItems(name_list)
        self.move(x, y)
        self.setGeometry(x, y, self.sizeHint().width(), self.sizeHint().height())
        self.lw.itemClicked.connect(self.getclickitem)
        self.show()

    def getclickitem(self, item: QListWidgetItem):
        self.sendclickitem.emit(item.text())
        self.close()


class MC:
    H = 1
    V = 0
    BD = -1

    def __init__(self):
        pass


class Lrc(QtWidgets.QFrame):
    sendnext = QtCore.pyqtSignal(int)


    def __init__(self):
        super().__init__()
        self.bjs = st.conf.get('lrc_section', 'bjs')
        self.fc1 = st.conf.get('lrc_section', 'fc1')
        self.fc2 = st.conf.get('lrc_section', 'fc2')
        self.ml = False
        self.lrc = []
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon('resource/Yuyeicon.ico'))
        self.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(719, 149)
        Form.setWindowTitle("")

        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 40))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setStyleSheet("QTableWidget::Item{max-width:20px}\n"
                                       "QTableWidget::Item:hover,QTableWidget::Item:selected {\n"
                                       "    background-color:rgb(135, 135, 135)\n"
                                       "}\n"
                                       "QTableWidget::Item{border:0px solid rgb(255,0,0);}\n"
                                       "QScrollBar{background-color:white; height:10px; }\n"
                                       "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px; }\n"
                                       "QScrollBar::handle:hover{background:gray; }\n"
                                       "QScrollBar::sub-line{background:transparent;}\n"
                                       "QScrollBar::add-line{background:transparent;}"
                                       "QTableWidget{background-color:rgb(135, 135, 135)}")
        self.tableWidget.setMidLineWidth(0)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setShowGrid(False)
        # self.setFrameShape(QtWidgets.QFrame.Panel)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 6, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(10)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.w = QtWidgets.QWidget(self)
        self.w.setStyleSheet("background-color:rgb(%s)" % self.bjs)
        self.h = QtWidgets.QHBoxLayout(self)
        self.h.addWidget(self.tableWidget, 0, QtCore.Qt.AlignHCenter)
        self.w.setLayout(self.h)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.w.setMinimumHeight(40)
        self.verticalLayout_2.addWidget(self.w)
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.setLayout(self.verticalLayout_2)
        self.mysetup()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def mysetup(self):
        self.setMouseTracking(True)
        self.verticalLayout_2.setSpacing(0)
        self.setAttribute(QtCore.Qt.WA_Hover, True)  # 开启悬停事件
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.installEventFilter(self)
        f = Lrc.onLoadFont('resource/淘气黑体.ttf', 20, 75)
        if f is not None:
            self.label.setFont(f)
            self.label_2.setFont(f)
        self.tableWidget.setStyleSheet("QTableWidget{background-color:rgb(43, 43, 43,0);border:0px solid white;color:white}")
        self.w.hide()
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setMaximumWidth(500)
        self.tableWidget.setMinimumWidth(500)
        self.tableWidget.setMinimumHeight(45)
        self.setGeometry((QtWidgets.QDesktopWidget().screenGeometry().width() - self.width()) / 2,
                         (QtWidgets.QDesktopWidget().screenGeometry().height() - self.height()) / 2,
                         self.sizeHint().width(), self.sizeHint().height())
        self.tableWidget.itemClicked.connect(self.tc)
        self.label.setStyleSheet('color:rgb(%s)' % self.fc1)
        self.label_2.setStyleSheet('color:rgb(%s)' % self.fc2)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 只读

    def reset(self):
        self.lrc.clear()
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(
            _translate("Form", "<html><head/><body><p align=\"center\">Yuye</p></body></html>" ))
        self.label_2.setText(
            _translate("Form", "<html><head/><body><p align=\"center\"></p></body></html>" ))

    def setFixedSize_my(self, a0: QtCore.QSize) -> None:
        if self.label.pos().y() < 42 or a0.width() < 350:
            if a0.width() < self.size().width() or a0.height() < self.height():
                return
        self.setFixedSize(a0)
        f = self.label.font()
        f.setPointSize((a0.height() - self.tableWidget.height() - 10) / 4)
        self.label.setFont(f)
        self.label_2.setFont(f)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">Yuye</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"center\"></p></body></html>"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "新建行"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", "上一首"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", "播放"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", "下一首"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Form", "-"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Form", "+"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("Form", "设置"))
        item = self.tableWidget.item(0, 6)
        item.setText(_translate("Form", "关闭"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    def settext(self, index):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(
            _translate("Form", "<html><head/><body><p align=\"center\">%s</p></body></html>" % self.lrc[index]))
        if index + 1 < len(self.lrc):
            self.label_2.setText(
                _translate("Form", "<html><head/><body><p align=\"center\">%s</p></body></html>" % self.lrc[index + 1]))

    def tc(self, item: QtWidgets.QTableWidgetItem):
        y = item.column()
        if y == 0:
            self.sendnext.emit(-1)
        if y == 1:
            self.sendnext.emit(0)
        if y == 2:
            self.sendnext.emit(1)
        if y == 3:
            f = self.label.font()
            f.setPointSize(f.pointSize() - 2)
            self.label.setFont(f)
            self.label_2.setFont(f)
        if y == 4:
            f = self.label.font()
            f.setPointSize(f.pointSize() + 2)
            self.label.setFont(f)
            self.label_2.setFont(f)
        if y == 5:
            c = self.cursor().pos()
            self.set = Ui_pop(['设置颜色'], c.x(), c.y())
            self.set.sendclickitem.connect(self.changeset)
        if y == 6:
            self.close()

    def changeset(self, name):
        if name == '设置颜色':
            self.set.close()
            p = re.compile(r"(\d+),(\d+),(\d+),(\d+)")
            fcl1 = re.findall(p, self.fc1)
            fcl2 = re.findall(p, self.fc2)
            self.c = QColorDialog.getColor(QtGui.QColor(int(fcl1[0][0]), int(fcl1[0][1]), int(fcl1[0][2])))
            self.fc1 = '%d,%d,%d,%d' % (self.c.red(), self.c.green(), self.c.blue(), 255)
            self.label.setStyleSheet('color:rgb(%s)' % self.fc1)
            st.set_confi('lrc_section', 'fc1', self.fc1)
            self.c = QColorDialog.getColor(QtGui.QColor(int(fcl2[0][0]), int(fcl2[0][1]), int(fcl2[0][2])))
            self.fc2 = '%d,%d,%d,%d' % (self.c.red(), self.c.green(), self.c.blue(), 255)
            self.label_2.setStyleSheet('color:rgb(%s)' % self.fc2)
            st.set_confi('lrc_section', 'fc2', self.fc2)

    def eventFilter(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:
        if a0 == self or a0 == self.label or a0 == self.label_2:
            if a1.type() == QtCore.QEvent.HoverEnter:
                self.setStyleSheet("QFrame{background-color:rgb(%s)}" % self.bjs)
                self.w.show()
            else:
                if a1.type() == QtCore.QEvent.HoverLeave:
                    self.setStyleSheet("QFrame{}")
                    self.w.hide()
                else:
                    if a1.type() == QtCore.QEvent.HoverMove:
                        if a1.pos().x() < 15:
                            if a1.pos().y() < 15:
                                self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
                                self.mc = MC.BD
                            else:
                                if self.height() - a1.pos().y() < 15:
                                    self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
                                    self.mc = MC.BD
                                else:
                                    self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
                                    self.mc = MC.H
                        else:
                            if self.width() - a1.pos().x() < 15:
                                if a1.pos().y() < 15:
                                    self.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
                                    self.mc = MC.BD
                                else:
                                    if self.height() - a1.pos().y() < 15:
                                        self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
                                        self.mc = MC.BD
                                    else:
                                        self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
                                        self.mc = MC.H
                            else:
                                if self.height() - a1.pos().y() < 15 or a1.pos().y() < 15:
                                    self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
                                    self.mc = MC.V
                                else:
                                    self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))  # QtCore.Qt.OpenHandCursor

                        if self.ml:
                            c = self.cursor().pos()
                            if self.cursor().shape() == QtCore.Qt.ArrowCursor:
                                self.move(self.p + c - self.mp)
                            else:

                                if self.mc == MC.BD:
                                    self.setFixedSize_my(
                                        self.size() + QtCore.QSize(c.x() - self.mp.x(), c.y() - self.mp.y()))
                                else:
                                    if self.mc == MC.H:
                                        self.setFixedSize_my(self.size() + QtCore.QSize(c.x() - self.mp.x(), 0))
                                    else:
                                        self.setFixedSize_my(self.size() + QtCore.QSize(0, c.y() - self.mp.y()))
                            self.p = self.pos()
                            self.mp = c

                    else:
                        if a1.type() == QtCore.QEvent.MouseButtonRelease:
                            self.ml = False

        return QtWidgets.QWidget.eventFilter(self, a0, a1)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.ml = False
        if a0.button() == QtCore.Qt.LeftButton:
            self.ml = True
            self.mp = a0.globalPos()
            self.p = self.pos()

    def Move(self, p: QtCore.QPoint):
        self.move(p.x(), p.y())
        self.ml = False

    @staticmethod
    def onLoadFont(strPath, *args):
        dFontFile = QtCore.QFile(strPath)
        if not dFontFile.open(QtCore.QIODevice.ReadOnly):
            return None  # 说明打开字体文件失败了
        nFontId = QtGui.QFontDatabase.addApplicationFontFromData(dFontFile.readAll())
        if nFontId == -1:
            return None  # 说明加载字体文件失败了，该字体不可用
        lFontFamily = QtGui.QFontDatabase.applicationFontFamilies(nFontId)
        if len(lFontFamily) == 0:
            return None  # 说明从字体中获取字体簇失败了
        font = QtGui.QFont(lFontFamily[0], *args)

        return font
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if not self.set.isHidden():
            self.set.close()