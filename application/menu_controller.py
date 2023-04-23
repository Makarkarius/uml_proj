from application.util import show_window
from business.db_manager import DBManager
from core.entity import CDEntity, ActsEntity
from core.model import Acts
from business.serializer import deserialize


class MenuController:
    def __init__(self, model=None):
        self.ex = None
        self.model = model
        self.db = DBManager('diagrams.db')

    def show_class_diagram(self):
        from ui import class_diagram
        from application.class_diagram_controller import ClassDiagramController

        classes = []
        links = []
        entity = CDEntity(classes, links)
        self.ex = class_diagram.MainWindow(ClassDiagramController(entity), entity)
        show_window(self.ex, 'диаграмма классов')

    def show_acts_diagram(self):
        from ui import acts_diagram
        from application.acts_diagram_controller import ActsDiagramController

        entity = ActsEntity(Acts())
        self.ex = acts_diagram.MainWindow(ActsDiagramController(entity), entity)
        show_window(self.ex, 'диаграмма прецедентов')

    def load(self, name):
        ans = None
        try:
            ans = self.db.load(name)
        except Exception as e:
            print(str(e))
            return

        entity = deserialize(ans[0])
        if ans[1] == 'cd':
            from ui import class_diagram
            from application.class_diagram_controller import ClassDiagramController

            entity.__class__ = CDEntity
            self.ex = class_diagram.MainWindow(ClassDiagramController(entity), entity)
            show_window(self.ex, 'диаграмма классов')
        elif ans[1] == 'ac':
            from ui import acts_diagram
            from application.acts_diagram_controller import ActsDiagramController

            entity.__class__ = ActsEntity
            self.ex = acts_diagram.MainWindow(ActsDiagramController(entity), entity)
            show_window(self.ex, 'диаграмма прецедентов')

    def delete(self, name):
        try:
            self.db.delete(name)
        except Exception as e:
            print(str(e))

    def read_names(self):
        data = None
        try:
            data = self.db.read_names()
        except Exception as e:
            print(str(e))
        return data
