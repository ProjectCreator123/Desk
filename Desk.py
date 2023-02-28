import sys
import os.path

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPainter, QImage, QFont, QColor, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QAction, QMenu, QToolBar, QMenuBar, \
    QUndoCommand, QUndoStack, QSpinBox, QComboBox, QCheckBox, QMessageBox, QFormLayout, QVBoxLayout, QHBoxLayout, qApp, \
    QFileDialog


class UndoCommand(QUndoCommand):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mPrevImage = parent.image.copy()
        self.mCurrImage = parent.image.copy()

    def undo(self):
        self.mCurrImage = self.parent.image.copy()
        self.parent.image = self.mPrevImage
        self.parent.update()

    def redo(self):
        self.parent.image = self.mCurrImage
        self.parent.update()


class Desk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setWindowTitle("Graphic editor - Desk")
        self.setStyleSheet("background-color: #777777")
        self.mUndoStack = QUndoStack(self)
        self.mUndoStack.setUndoLimit(30)
        self.mUndoStack.canUndoChanged.connect(self.can_undo_changed)
        self.mUndoStack.canRedoChanged.connect(self.can_redo_changed)
        self.image = QImage(QApplication.desktop().width() - 200,
                            QApplication.desktop().height() - 160,
                            QImage.Format_ARGB32)
        self.now_background = QColor(255, 255, 255)
        self.image.fill(self.now_background)
        self.configure()
        self.actions()
        self.icon_actions()
        self.menu_bar()
        self.tool_bar()
        self.can_undo_changed(self.mUndoStack.canUndo())
        self.can_redo_changed(self.mUndoStack.canRedo())
        self.start_pos = QPoint()
        self.checkered_or_lined, self.mode = "", ""
        self.opening_file_name, self.saving_file_name, self.now_file_name = "", "", ""
        self.now_size, self.now_color, self.drawing, self.size = None, None, False, 3
        self.color_theme, self.fill_color, self.instrument = "Dark", "transparent", "brush"
        self.brush_color, self.eraser_color = QColor(0, 0, 0), QColor(255, 255, 255)

    def actions(self):
        self.new = QAction("New", self)
        self.new.triggered.connect(self.new_paper)
        self.new.setShortcut("Ctrl+N")
        self.open = QAction("Open", self)
        self.open.triggered.connect(self.opening)
        self.open.setShortcut("Ctrl+O")
        self.save = QAction("Save as", self)
        self.save.triggered.connect(self.saving)
        self.save.setShortcut("Ctrl+S")
        self.settings = QAction("Settings", self)
        self.settings.triggered.connect(self.show_settings)
        self.settings.setShortcut("Ctrl+Alt+S")
        self.clear = QAction("Clear")
        self.clear.triggered.connect(self.clearing)
        self.clear.setShortcut("Del")
        self.actionUndo = QAction("Undo")
        self.actionUndo.triggered.connect(self.mUndoStack.undo)
        self.actionUndo.setShortcut("Ctrl+Z")
        self.actionRedo = QAction("Redo")
        self.actionRedo.triggered.connect(self.mUndoStack.redo)
        self.actionRedo.setShortcut("Ctrl+Y")
        self.exit = QAction("Exit", self)
        self.exit.triggered.connect(self.exiting)
        self.exit.setShortcut("Esc")

        self.brush = QAction("Brush", self)
        self.brush.triggered.connect(self.brushing)
        self.eraser = QAction("Eraser", self)
        self.eraser.triggered.connect(self.erasing)
        self.line = QAction("Line", self)
        self.line.triggered.connect(self.draw_line)
        self.rectangle = QAction("Rectangle", self)
        self.rectangle.triggered.connect(self.draw_rectangle)
        self.circle = QAction("Circle", self)
        self.circle.triggered.connect(self.draw_circle)

        self.pink = QAction("Pink", self)
        self.pink.triggered.connect(self.made_pink)
        self.red = QAction("Red", self)
        self.red.triggered.connect(self.made_red)
        self.orange = QAction("Orange", self)
        self.orange.triggered.connect(self.made_orange)
        self.yellow = QAction("Yellow", self)
        self.yellow.triggered.connect(self.made_yellow)
        self.green = QAction("Green", self)
        self.green.triggered.connect(self.made_green)
        self.light_blue = QAction("Light blue", self)
        self.light_blue.triggered.connect(self.made_light_blue)
        self.blue = QAction("Blue", self)
        self.blue.triggered.connect(self.made_blue)
        self.violet = QAction("Violet", self)
        self.violet.triggered.connect(self.made_violet)
        self.brown = QAction("Brown", self)
        self.brown.triggered.connect(self.made_brown)
        self.grey = QAction("Grey", self)
        self.grey.triggered.connect(self.made_grey)
        self.white = QAction("White", self)
        self.white.triggered.connect(self.made_white)
        self.black = QAction("Black", self)
        self.black.triggered.connect(self.made_black)

    def icon_actions(self):
        self.new.setIcon(QIcon(os.path.join("icons", "new.png")))
        self.open.setIcon(QIcon(os.path.join("icons", "open.png")))
        self.save.setIcon(QIcon(os.path.join("icons", "save.png")))
        self.settings.setIcon(QIcon(os.path.join("icons", "settings.png")))
        self.exit.setIcon(QIcon(os.path.join("icons", "exit.png")))

        self.actionUndo.setIcon(QIcon(os.path.join("icons", "undo.png")))
        self.actionRedo.setIcon(QIcon(os.path.join("icons", "redo.png")))
        self.clear.setIcon(QIcon(os.path.join("icons", "clear.png")))

        self.brush.setIcon(QIcon(os.path.join("icons", "brush.png")))
        self.eraser.setIcon(QIcon(os.path.join("icons", "eraser.png")))
        self.line.setIcon(QIcon(os.path.join("icons", "line.png")))
        self.rectangle.setIcon(QIcon(os.path.join("icons", "rectangle.png")))
        self.circle.setIcon(QIcon(os.path.join("icons", "circle.png")))

        self.pink.setIcon(QIcon(os.path.join("icons", "pink.png")))
        self.red.setIcon(QIcon(os.path.join("icons", "red.png")))
        self.orange.setIcon(QIcon(os.path.join("icons", "orange.png")))
        self.yellow.setIcon(QIcon(os.path.join("icons", "yellow.png")))
        self.green.setIcon(QIcon(os.path.join("icons", "green.png")))
        self.light_blue.setIcon(QIcon(os.path.join("icons", "light_blue.png")))
        self.blue.setIcon(QIcon(os.path.join("icons", "blue.png")))
        self.violet.setIcon(QIcon(os.path.join("icons", "violet.png")))
        self.brown.setIcon(QIcon(os.path.join("icons", "brown.png")))
        self.grey.setIcon(QIcon(os.path.join("icons", "grey.png")))
        self.white.setIcon(QIcon(os.path.join("icons", "white.png")))
        self.black.setIcon(QIcon(os.path.join("icons", "black.png")))

    def menu_bar(self):
        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        self.menu.setStyleSheet("color: white; background-color: #333333")

        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(self.new)
        file_menu.addAction(self.open)
        file_menu.addAction(self.save)
        file_menu.addAction(self.settings)
        file_menu.addSeparator()
        file_menu.addAction(self.exit)

        edit_menu = self.menu.addMenu("&Edit")
        edit_menu.addAction(self.actionUndo)
        edit_menu.addAction(self.actionRedo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.clear)

    def contextMenuEvent(self, event):
        separator_1 = QAction(self)
        separator_1.setSeparator(True)
        separator_2 = QAction(self)
        separator_2.setSeparator(True)

        self.context_menu = QMenu(self.centralWidget())
        self.context_menu.setStyleSheet("background: #333333; color: white")
        self.context_menu.addAction(self.new)
        self.context_menu.addAction(self.open)
        self.context_menu.addAction(self.save)
        self.context_menu.addAction(self.settings)
        self.context_menu.addAction(separator_1)
        self.context_menu.addAction(self.actionUndo)
        self.context_menu.addAction(self.actionRedo)
        self.context_menu.addAction(self.clear)
        self.context_menu.addAction(separator_2)
        self.context_menu.addAction(self.exit)
        self.context_menu.exec(event.globalPos())

    def tool_bar(self):
        self.instruments = QToolBar("Instruments", self)
        self.instruments.setStyleSheet("background-color: #555555")
        self.instruments.setMovable(False)
        self.instruments.addAction(self.brush)
        self.instruments.addAction(self.eraser)
        self.instruments.addAction(self.line)
        self.instruments.addAction(self.rectangle)
        self.instruments.addAction(self.circle)
        self.instruments.addWidget(self.spin)

        self.label = QLabel("Filling shapes:")
        self.label.setStyleSheet("color: white")
        self.label.setFont(QFont("Arial", 10))
        self.label.setAlignment(Qt.AlignHCenter)
        self.colors = QToolBar("Colors", self)
        self.colors.setStyleSheet("background-color: #555555")
        self.colors.setMovable(False)
        self.colors.addAction(self.pink)
        self.colors.addAction(self.red)
        self.colors.addAction(self.orange)
        self.colors.addAction(self.yellow)
        self.colors.addAction(self.green)
        self.colors.addAction(self.light_blue)
        self.colors.addAction(self.blue)
        self.colors.addAction(self.violet)
        self.colors.addAction(self.brown)
        self.colors.addAction(self.grey)
        self.colors.addAction(self.white)
        self.colors.addAction(self.black)
        self.colors.addWidget(self.label)
        self.colors.addWidget(self.combo)

        self.file = QToolBar("File", self)
        self.file.setStyleSheet("background-color: #555555")
        self.file.setMovable(False)
        self.file.addAction(self.clear)
        self.file.addAction(self.actionUndo)
        self.file.addAction(self.actionRedo)
        self.file.addAction(self.new)

        self.addToolBar(Qt.TopToolBarArea, self.instruments)
        self.addToolBar(Qt.LeftToolBarArea, self.colors)
        self.addToolBar(Qt.BottomToolBarArea, self.file)

    def can_undo_changed(self, enabled):
        self.actionUndo.setEnabled(enabled)

    def can_redo_changed(self, enabled):
        self.actionRedo.setEnabled(enabled)

    def make_undo_command(self):
        self.mUndoStack.push(UndoCommand(self))

    def set_width(self, v):
        self.new_width = v
        self.button_3.setEnabled(True)

    def set_height(self, v):
        self.new_height = v
        self.button_3.setEnabled(True)

    def result(self):
        self.make_undo_command()
        if self.aspect:
            self.image = self.image.scaled(self.new_width, self.new_height, Qt.KeepAspectRatio)
        else:
            self.image = self.image.scaled(self.new_width, self.new_height)
        if self.color_theme == "Dark":
            self.setStyleSheet("background-color: #777777")
            self.instruments.setStyleSheet("background-color: #555555")
            self.colors.setStyleSheet("background-color: #555555")
            self.file.setStyleSheet("background-color: #555555")
        elif self.color_theme == "Violet":
            self.setStyleSheet("background-color: #7851A9")
            self.instruments.setStyleSheet("background-color: #46394B")
            self.colors.setStyleSheet("background-color: #46394B")
            self.file.setStyleSheet("background-color: #46394B")
        elif self.color_theme == "Blue":
            self.setStyleSheet("background-color: #606E8C")
            self.instruments.setStyleSheet("background-color: #2c3337")
            self.colors.setStyleSheet("background-color: #2c3337")
            self.file.setStyleSheet("background-color: #2c3337")
        elif self.color_theme == "Green":
            self.setStyleSheet("background-color: #355E3B")
            self.instruments.setStyleSheet("background-color: #2F4538")
            self.colors.setStyleSheet("background-color: #2F4538")
            self.file.setStyleSheet("background-color: #2F4538")
        if self.selected_background == QColor(255, 255, 255):
            if self.mode == "checkered":
                self.light_checkered()
            elif self.mode == "lined":
                self.light_lined()
            else:
                self.made_white_background()
        elif self.selected_background == QColor(100, 150, 100):
            if self.mode == "checkered":
                self.dark_checkered()
            elif self.mode == "lined":
                self.dark_lined()
        elif self.selected_background == QColor(255, 100, 150):
            self.made_pink_background()
        elif self.selected_background == QColor(255, 0, 0):
            self.made_red_background()
        elif self.selected_background == QColor(255, 150, 0):
            self.made_orange_background()
        elif self.selected_background == QColor(255, 255, 0):
            self.made_yellow_background()
        elif self.selected_background == QColor(0, 255, 0):
            self.made_green_background()
        elif self.selected_background == QColor(0, 255, 255):
            self.made_light_blue_background()
        elif self.selected_background == QColor(0, 0, 255):
            self.made_blue_background()
        elif self.selected_background == QColor(150, 0, 255):
            self.made_violet_background()
        elif self.selected_background == QColor(150, 75, 0):
            self.made_brown_background()
        elif self.selected_background == QColor(100, 100, 100):
            self.made_grey_background()
        elif self.selected_background == QColor(0, 0, 0):
            self.made_black_background()
        self.spin_1.setValue(self.image.width())
        self.spin_2.setValue(self.image.height())
        self.button_3.setEnabled(False)
        self.update()

    def check_changed(self, f):
        if f == Qt.Checked:
            self.aspect = True
        else:
            self.aspect = False

    def value_changed(self, x):
        self.size = x

    def text_changed(self, y):
        if y == "Empty":
            self.fill_color = "transparent"
        elif y == "Pink":
            self.fill_color = QColor(255, 100, 150)
        elif y == "Red":
            self.fill_color = QColor(255, 0, 0)
        elif y == "Orange":
            self.fill_color = QColor(255, 150, 0)
        elif y == "Yellow":
            self.fill_color = QColor(255, 255, 0)
        elif y == "Green":
            self.fill_color = QColor(0, 255, 0)
        elif y == "Light blue":
            self.fill_color = QColor(0, 255, 255)
        elif y == "Blue":
            self.fill_color = QColor(0, 0, 255)
        elif y == "Violet":
            self.fill_color = QColor(150, 0, 255)
        elif y == "Brown":
            self.fill_color = QColor(150, 75, 0)
        elif y == "Grey":
            self.fill_color = QColor(100, 100, 100)
        elif y == "White":
            self.fill_color = QColor(255, 255, 255)
        elif y == "Black":
            self.fill_color = QColor(0, 0, 0)

    def color_changed(self, c):
        self.instrument = "brush"
        self.button_3.setEnabled(True)
        if c == "White":
            self.selected_background = QColor(255, 255, 255)
            self.mode = ""
        elif c in ["Light checkered", "Light lined"]:
            self.selected_background = QColor(255, 255, 255)
            if c == "Light checkered":
                self.mode = "checkered"
            else:
                self.mode = "lined"
        elif c in ["Dark checkered", "Dark lined"]:
            self.selected_background = QColor(100, 150, 100)
            if c == "Dark checkered":
                self.mode = "checkered"
            else:
                self.mode = "lined"
        elif c == "Pink":
            self.selected_background = QColor(255, 100, 150)
            self.mode = ""
        elif c == "Red":
            self.selected_background = QColor(255, 0, 0)
            self.mode = ""
        elif c == "Orange":
            self.selected_background = QColor(255, 150, 0)
            self.mode = ""
        elif c == "Yellow":
            self.selected_background = QColor(255, 255, 0)
            self.mode = ""
        elif c == "Green":
            self.selected_background = QColor(0, 255, 0)
            self.mode = ""
        elif c == "Light blue":
            self.selected_background = QColor(0, 255, 255)
            self.mode = ""
        elif c == "Blue":
            self.selected_background = QColor(0, 0, 255)
            self.mode = ""
        elif c == "Violet":
            self.selected_background = QColor(150, 0, 255)
            self.mode = ""
        elif c == "Brown":
            self.selected_background = QColor(150, 75, 0)
            self.mode = ""
        elif c == "Grey":
            self.selected_background = QColor(100, 100, 100)
            self.mode = ""
        elif c == "Black":
            self.selected_background = QColor(0, 0, 0)
            self.mode = ""

    def theme_changed(self, t):
        if t == "Dark":
            self.color_theme = "Dark"
        elif t == "Violet":
            self.color_theme = "Violet"
        elif t == "Blue":
            self.color_theme = "Blue"
        elif t == "Green":
            self.color_theme = "Green"
        self.button_3.setEnabled(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(160, 90, self.image)
        painter.setBackground(QColor(255, 255, 255))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.make_undo_command()
            self.start_pos = (event.x() - 160, event.y() - 90)
            self.drawing = True
            if self.instrument == "eraser":
                self.now_color = self.eraser_color
                self.now_size = self.size * 2
            else:
                self.now_color = self.brush_color
                self.now_size = self.size

            if self.instrument in ["brush", "eraser"]:
                painter = QPainter(self.image)
                painter.setPen(QPen(self.now_color, self.now_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawPoint(event.x() - 160, event.y() - 90)
            elif self.instrument in ["line", "rectangle", "circle"]:
                self.image.save(os.path.join("time", "time.png"))
            self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            if self.instrument == "eraser":
                self.now_color = self.eraser_color
                self.now_size = self.size * 2
                painter = QPainter(self.image)
                painter.setPen(QPen(self.now_color, self.now_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.start_pos[0], self.start_pos[1], event.x() - 160, event.y() - 90)
                self.start_pos = (event.x() - 160, event.y() - 90)
            else:
                self.now_color = self.brush_color
                self.now_size = self.size
                if self.instrument == "brush":
                    painter = QPainter(self.image)
                    painter.setPen(QPen(self.now_color, self.now_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    painter.drawLine(self.start_pos[0], self.start_pos[1], event.x() - 160, event.y() - 90)
                    self.start_pos = (event.x() - 160, event.y() - 90)
                elif self.instrument == "line":
                    self.image = QImage(os.path.join("time", "time.png"))
                    painter = QPainter(self.image)
                    painter.setPen(QPen(self.now_color, self.now_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    painter.drawLine(self.start_pos[0], self.start_pos[1], event.x() - 160, event.y() - 90)
                elif self.instrument == "rectangle":
                    self.image = QImage(os.path.join("time", "time.png"))
                    painter = QPainter(self.image)
                    painter.setPen(QPen(self.now_color, self.now_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    if self.fill_color != "transparent":
                        painter.setBrush(QBrush(self.fill_color, Qt.SolidPattern))
                    painter.drawRect(self.start_pos[0], self.start_pos[1],
                                     event.x() - self.start_pos[0] - 160, event.y() - self.start_pos[1] - 90)
                elif self.instrument == "circle":
                    self.image = QImage(os.path.join("time", "time.png"))
                    painter = QPainter(self.image)
                    painter.setPen(QPen(self.now_color, self.now_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    if self.fill_color != "transparent":
                        painter.setBrush(QBrush(self.fill_color, Qt.SolidPattern))
                    painter.drawEllipse(self.start_pos[0], self.start_pos[1],
                                        event.x() - self.start_pos[0] - 160, event.y() - self.start_pos[1] - 90)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_N and event.modifiers() == Qt.ControlModifier:
            self.new_paper()
        elif event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.opening()
        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.saving()
        elif event.key() == Qt.Key_S and event.modifiers() == (Qt.ControlModifier and Qt.AltModifier):
            self.show_settings()
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.mUndoStack.undo()
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self.mUndoStack.redo()
        elif event.key() == Qt.Key_Delete:
            self.clearing()
        elif event.key() == Qt.Key_Escape:
            self.exiting()

    def new_paper(self):
        self.make_undo_command()
        self.eraser.setEnabled(True)
        self.background_color.setCurrentText("White")
        self.image = QImage(QApplication.desktop().width() - 200, QApplication.desktop().height() - 160,
                            QImage.Format_ARGB32)
        self.now_background = QColor(255, 255, 255)
        self.image.fill(self.now_background)
        self.selected_background, self.mode = "", ""
        self.checkered_or_lined = ""
        self.opening_file_name = ""
        self.saving_file_name = ""
        self.now_file_name = ""
        self.update()

    def opening(self):
        self.opening_file_name = QFileDialog.getOpenFileName(self, "Opening", "", "Image (*.jpeg;*.jpg;*.png)")[0]
        if self.opening_file_name:
            self.make_undo_command()
            self.now_file_name = self.opening_file_name
            self.image = QImage(self.opening_file_name)

    def saving(self):
        self.saving_file_name = QFileDialog.getSaveFileName(self, "Saving", "", "Image (*.jpeg;*.jpg;*.png)")[0]
        if self.saving_file_name:
            self.now_file_name = self.saving_file_name
            self.image.save(self.saving_file_name)

    def configure(self):
        self.spin = QSpinBox()
        self.combo = QComboBox()

        self.combo.addItem(QIcon(os.path.join("icons", "transparent.png")), "Empty")
        self.combo.addItem(QIcon(os.path.join("icons", "pink.png")), "Pink")
        self.combo.addItem(QIcon(os.path.join("icons", "red.png")), "Red")
        self.combo.addItem(QIcon(os.path.join("icons", "orange.png")), "Orange")
        self.combo.addItem(QIcon(os.path.join("icons", "yellow.png")), "Yellow")
        self.combo.addItem(QIcon(os.path.join("icons", "green.png")), "Green")
        self.combo.addItem(QIcon(os.path.join("icons", "light_blue.png")), "Light blue")
        self.combo.addItem(QIcon(os.path.join("icons", "blue.png")), "Blue")
        self.combo.addItem(QIcon(os.path.join("icons", "violet.png")), "Violet")
        self.combo.addItem(QIcon(os.path.join("icons", "brown.png")), "Brown")
        self.combo.addItem(QIcon(os.path.join("icons", "grey.png")), "Grey")
        self.combo.addItem(QIcon(os.path.join("icons", "white.png")), "White")
        self.combo.addItem(QIcon(os.path.join("icons", "black.png")), "Black")

        self.spin.setRange(3, 17)
        self.spin.setSingleStep(2)
        self.spin.setFocusPolicy(Qt.NoFocus)
        self.spin.lineEdit().setReadOnly(True)
        self.spin.lineEdit().setStyleSheet("color: white")
        self.spin.valueChanged.connect(self.value_changed)
        self.combo.setFocusPolicy(Qt.NoFocus)
        self.combo.setStyleSheet("color: white")
        self.combo.currentTextChanged.connect(self.text_changed)

        self.new_win = QWidget(self, Qt.Window)
        self.new_win.setWindowModality(Qt.WindowModal)
        self.new_win.setWindowTitle("Settings")

        main_label_1 = QLabel("Scale", self.new_win)
        main_label_2 = QLabel("Background", self.new_win)
        main_label_3 = QLabel("Theme", self.new_win)
        label_1 = QLabel("Width:", self.new_win)
        label_2 = QLabel("Height:", self.new_win)
        label_3 = QLabel("Choose color:", self.new_win)
        label_4 = QLabel("Choose style:", self.new_win)
        self.spin_1 = QSpinBox(self.new_win)
        self.spin_2 = QSpinBox(self.new_win)
        self.check = QCheckBox("Keep Aspect Ratio", self.new_win)
        self.background_color = QComboBox(self.new_win)
        self.theme = QComboBox(self.new_win)
        button_1 = QPushButton("OK", self.new_win)
        button_2 = QPushButton("Cancel", self.new_win)
        self.button_3 = QPushButton("Apply", self.new_win)
        self.selected_background, self.mode = "", ""

        self.spin_1.setRange(1, QApplication.desktop().width() - 200)
        self.spin_2.setRange(1, QApplication.desktop().height() - 160)
        self.background_color.addItem(QIcon(os.path.join("icons", "white.png")), "White")
        self.background_color.addItem(QIcon(os.path.join("icons", "light_checkered.png")), "Light checkered")
        self.background_color.addItem(QIcon(os.path.join("icons", "dark_checkered.png")), "Dark checkered")
        self.background_color.addItem(QIcon(os.path.join("icons", "light_lined.png")), "Light lined")
        self.background_color.addItem(QIcon(os.path.join("icons", "dark_lined.png")), "Dark lined")
        self.background_color.addItem(QIcon(os.path.join("icons", "pink.png")), "Pink")
        self.background_color.addItem(QIcon(os.path.join("icons", "red.png")), "Red")
        self.background_color.addItem(QIcon(os.path.join("icons", "orange.png")), "Orange")
        self.background_color.addItem(QIcon(os.path.join("icons", "yellow.png")), "Yellow")
        self.background_color.addItem(QIcon(os.path.join("icons", "green.png")), "Green")
        self.background_color.addItem(QIcon(os.path.join("icons", "light_blue.png")), "Light blue")
        self.background_color.addItem(QIcon(os.path.join("icons", "blue.png")), "Blue")
        self.background_color.addItem(QIcon(os.path.join("icons", "violet.png")), "Violet")
        self.background_color.addItem(QIcon(os.path.join("icons", "brown.png")), "Brown")
        self.background_color.addItem(QIcon(os.path.join("icons", "grey.png")), "Grey")
        self.background_color.addItem(QIcon(os.path.join("icons", "black.png")), "Black")
        self.theme.addItem(QIcon(os.path.join("icons", "black.png")), "Dark")
        self.theme.addItem(QIcon(os.path.join("icons", "violet.png")), "Violet")
        self.theme.addItem(QIcon(os.path.join("icons", "blue.png")), "Blue")
        self.theme.addItem(QIcon(os.path.join("icons", "green.png")), "Green")

        layout1 = QFormLayout()
        layout1.addRow(label_1, self.spin_1)
        layout1.addRow(label_2, self.spin_2)
        layout1.addWidget(self.check)
        layout2 = QFormLayout()
        layout2.addRow(label_3, self.background_color)
        layout3 = QFormLayout()
        layout3.addRow(label_4, self.theme)
        layout4 = QHBoxLayout()
        layout4.addWidget(button_1)
        layout4.addWidget(button_2)
        layout4.addWidget(self.button_3)
        main_layout = QVBoxLayout(self.new_win)
        main_layout.addWidget(main_label_1)
        main_layout.addLayout(layout1)
        main_layout.addWidget(main_label_2)
        main_layout.addLayout(layout2)
        main_layout.addWidget(main_label_3)
        main_layout.addLayout(layout3)
        main_layout.addLayout(layout4)
        self.new_win.setLayout(main_layout)

        main_label_1.setAlignment(Qt.AlignCenter)
        main_label_2.setAlignment(Qt.AlignCenter)
        main_label_3.setAlignment(Qt.AlignCenter)
        main_label_1.setFont(QFont("Arial", 20))
        main_label_2.setFont(QFont("Arial", 20))
        main_label_3.setFont(QFont("Arial", 20))
        label_1.setFont(QFont("Arial", 10))
        label_2.setFont(QFont("Arial", 10))
        label_3.setFont(QFont("Arial", 10))
        label_4.setFont(QFont("Arial", 10))
        self.spin_1.setFont(QFont("Arial", 10))
        self.spin_2.setFont(QFont("Arial", 10))
        self.check.setFont(QFont("Arial", 10))
        self.background_color.setFont(QFont("Arial", 10))
        self.theme.setFont(QFont("Arial", 10))
        main_label_1.setStyleSheet("color: white")
        main_label_2.setStyleSheet("color: white")
        main_label_3.setStyleSheet("color: white")
        label_1.setStyleSheet("color: white")
        label_2.setStyleSheet("color: white")
        label_3.setStyleSheet("color: white")
        label_4.setStyleSheet("color: white")
        self.spin_1.setStyleSheet("color: white")
        self.spin_2.setStyleSheet("color: white")
        self.check.setStyleSheet("color: white")
        self.background_color.setStyleSheet("color: white")
        self.theme.setStyleSheet("color: white")
        button_1.setStyleSheet("color: white")
        button_2.setStyleSheet("color: white")
        self.button_3.setStyleSheet("color: white")

        self.spin_1.valueChanged.connect(self.set_width)
        self.spin_2.valueChanged.connect(self.set_height)
        self.check.stateChanged.connect(self.check_changed)
        self.background_color.currentTextChanged.connect(self.color_changed)
        self.theme.currentTextChanged.connect(self.theme_changed)
        button_1.clicked.connect(self.hide_settings)
        button_2.clicked.connect(self.hide_settings)
        self.button_3.clicked.connect(self.result)

    def show_settings(self):
        self.aspect = True
        self.spin_1.setValue(self.image.width())
        self.spin_2.setValue(self.image.height())
        self.check.setCheckState(Qt.Checked)
        self.button_3.setEnabled(False)
        self.new_win.show()

    def hide_settings(self):
        sender = self.sender()
        if sender.text() == "OK":
            self.result()
        self.aspect = True
        self.check.setCheckState(Qt.Checked)
        self.button_3.setEnabled(False)
        self.new_win.hide()

    def clearing(self):
        self.make_undo_command()
        if self.now_file_name:
            self.image = QImage(self.now_file_name)
        else:
            self.image.fill(self.now_background)
            if self.now_background == QColor(100, 150, 100):
                if self.checkered_or_lined == "checkered":
                    self.made_checkered("dark")
                elif self.checkered_or_lined == "lined":
                    self.made_lined("dark")
            elif self.now_background == QColor(255, 255, 255):
                if self.checkered_or_lined == "checkered":
                    self.made_checkered("light")
                elif self.checkered_or_lined == "lined":
                    self.made_lined("light")
        self.update()

    def exiting(self):
        msg = QMessageBox(QMessageBox.Question, "Exit", "Are you sure you want to get out?",
                          buttons=QMessageBox.Yes | QMessageBox.No, parent=self)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("color: #ffffff")
        qApp.setStyleSheet("QMessageBox QPushButton{color: white}")
        msg.exec()
        ans = msg.standardButton(msg.clickedButton())
        if ans == QMessageBox.Yes:
            exit()

    def brushing(self):
        self.instrument = "brush"

    def erasing(self):
        self.instrument = "eraser"

    def draw_line(self):
        self.instrument = "line"

    def draw_rectangle(self):
        self.instrument = "rectangle"

    def draw_circle(self):
        self.instrument = "circle"

    def made_pink(self):
        self.brush_color = QColor(255, 100, 150)

    def made_red(self):
        self.brush_color = QColor(255, 0, 0)

    def made_orange(self):
        self.brush_color = QColor(255, 150, 0)

    def made_yellow(self):
        self.brush_color = QColor(255, 255, 0)

    def made_green(self):
        self.brush_color = QColor(0, 255, 0)

    def made_light_blue(self):
        self.brush_color = QColor(0, 255, 255)

    def made_blue(self):
        self.brush_color = QColor(0, 0, 255)

    def made_violet(self):
        self.brush_color = QColor(150, 0, 255)

    def made_brown(self):
        self.brush_color = QColor(150, 75, 0)

    def made_grey(self):
        self.brush_color = QColor(100, 100, 100)

    def made_white(self):
        self.brush_color = QColor(255, 255, 255)

    def made_black(self):
        self.brush_color = QColor(0, 0, 0)

    def made_lined(self, color):
        painter = QPainter(self.image)
        self.checkered_or_lined = "lined"
        if color == "light":
            painter.setPen(QPen(QColor(0, 150, 150), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            painter.setPen(QPen(QColor(255, 255, 255), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for y in range(0, QApplication.desktop().height() - 160, 60):
            painter.drawLine(0, y, QApplication.desktop().width() - 200, y)

    def made_checkered(self, color):
        painter = QPainter(self.image)
        self.checkered_or_lined = "checkered"
        if color == "light":
            painter.setPen(QPen(QColor(0, 150, 150), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            painter.setPen(QPen(QColor(255, 255, 255), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for x in range(0, QApplication.desktop().width() - 200, 45):
            painter.drawLine(x, 0, x, QApplication.desktop().height() - 160)
        for y in range(0, QApplication.desktop().height() - 160, 45):
            painter.drawLine(0, y, QApplication.desktop().width() - 200, y)

    def light_lined(self):
        self.make_undo_command()
        self.now_background = QColor(255, 255, 255)
        self.instrument = "brush"
        self.eraser.setEnabled(False)
        self.image.fill(self.now_background)
        self.made_lined("light")

    def dark_lined(self):
        self.make_undo_command()
        self.now_background = QColor(100, 150, 100)
        self.instrument = "brush"
        self.eraser.setEnabled(False)
        self.image.fill(self.now_background)
        self.made_lined("dark")

    def light_checkered(self):
        self.make_undo_command()
        self.now_background = QColor(255, 255, 255)
        self.instrument = "brush"
        self.eraser.setEnabled(False)
        self.image.fill(self.now_background)
        self.made_checkered("light")

    def dark_checkered(self):
        self.make_undo_command()
        self.now_background = QColor(100, 150, 100)
        self.instrument = "brush"
        self.eraser.setEnabled(False)
        self.image.fill(self.now_background)
        self.made_checkered("dark")

    def made_pink_background(self):
        self.make_undo_command()
        self.now_background = QColor(255, 100, 150)
        self.eraser_color = QColor(255, 100, 150)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_red_background(self):
        self.make_undo_command()
        self.now_background = QColor(255, 0, 0)
        self.eraser_color = QColor(255, 0, 0)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_orange_background(self):
        self.make_undo_command()
        self.now_background = QColor(255, 150, 0)
        self.eraser_color = QColor(255, 150, 0)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_yellow_background(self):
        self.make_undo_command()
        self.now_background = QColor(255, 255, 0)
        self.eraser_color = QColor(255, 255, 0)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_green_background(self):
        self.make_undo_command()
        self.now_background = QColor(0, 255, 0)
        self.eraser_color = QColor(0, 255, 0)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_light_blue_background(self):
        self.make_undo_command()
        self.now_background = QColor(0, 255, 255)
        self.eraser_color = QColor(0, 255, 255)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_blue_background(self):
        self.make_undo_command()
        self.now_background = QColor(0, 0, 255)
        self.eraser_color = QColor(0, 0, 255)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_violet_background(self):
        self.make_undo_command()
        self.now_background = QColor(150, 0, 255)
        self.eraser_color = QColor(150, 0, 255)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_brown_background(self):
        self.make_undo_command()
        self.now_background = QColor(150, 75, 0)
        self.eraser_color = QColor(150, 75, 0)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_grey_background(self):
        self.make_undo_command()
        self.now_background = QColor(100, 100, 100)
        self.eraser_color = QColor(100, 100, 100)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_white_background(self):
        self.make_undo_command()
        self.checkered_or_lined = ""
        self.now_background = QColor(255, 255, 255)
        self.eraser_color = QColor(255, 255, 255)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)

    def made_black_background(self):
        self.make_undo_command()
        self.now_background = QColor(0, 0, 0)
        self.eraser_color = QColor(0, 0, 0)
        self.eraser.setEnabled(True)
        self.image.fill(self.now_background)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = Desk()
    my_app.setFixedWidth(QApplication.desktop().width())
    my_app.setFixedHeight(QApplication.desktop().height())
    my_app.showFullScreen()
    my_app.show()
    sys.exit(app.exec_())
