from typing import List

from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Chargez votre template à partir d'un fichier .html
        with open("helb_manager/project_detail.html") as f:
            template = f.read()

        # Créez un widget pour afficher votre template
        template_widget = QtWidgets.QTextEdit(template)
        template_widget.setReadOnly(True)

        # Récupérez les widgets "todo" et "status" de votre template
        self.todos = template_widget.findChildren(QtWidgets.QLabel, "todo")
        self.all_status = template_widget.findChildren(QtWidgets.QLabel, "status")
        self.draggable_todo = None

        for todo in self.todos:
            todo.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            todo.setAcceptDrops(True)
            todo.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
            todo.installEventFilter(self)

        for status in self.all_status:
            status.installEventFilter(self)

        # Ajoutez le widget au layout de la fenêtre principale
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(template_widget)
        self.setLayout(layout)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.DragEnter:
            self.drag_enter_event(obj, event)
            return True
        elif event.type() == QtCore.QEvent.DragLeave:
            self.drag_leave_event(obj, event)
            return True
        elif event.type() == QtCore.QEvent.Drop:
            self.drop_event(obj, event)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            self.mouse_press_event(obj, event)
            return True
        elif event.type() == QtCore.QEvent.MouseMove:
            self.mouse_move_event(obj, event)
            return True
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.mouse_release_event(obj, event)
            return True

        return super().eventFilter(obj, event)

    def drag_enter_event(self, obj, event):
        if isinstance(obj, QtWidgets.QLabel):
            obj.setStyleSheet("border: 1px dashed #ccc;")
            event.accept()

    def drag_leave_event(self, obj, event):
        if isinstance(obj, QtWidgets.QLabel):
            obj.setStyleSheet("border: none;")
            event.accept()

    def drop_event(self, obj, event):
        if isinstance(obj, QtWidgets.QLabel):
            obj.setStyleSheet("border: none;")
            event.accept()
            self.draggable_todo.setParent(obj)
            self.draggable_todo.move(event.pos())

            # Récupérez le titre de la tâche ici
            title_task = self.draggable_todo.text()
            # Récupérez le titre de la colonne ici
            new_status = obj.text()

            self.draggable_todo = None

    def mouse_press_event(self, obj, event):
        if isinstance(obj, QtWidgets.QLabel):
            self.draggable_todo = obj
            self.drag_start_pos = event.pos()

    def mouse_move_event(self, obj, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.draggable_todo:
            distance = (event.pos() - self.drag_start_pos).manhattanLength()
            if distance >= QtWidgets.QApplication.startDragDistance():
                self.perform_drag()

    def mouse_release_event(self, obj, event):
        self.draggable_todo = None

    def perform_drag(self):
        mime_data = QtCore.QMimeData()
        mime_data.setText(self.draggable_todo.text())
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.draggable_todo.pixmap())
        drag.setHotSpot(self.draggable_todo.rect().center())
        drag.exec_(QtCore.Qt.MoveAction)


