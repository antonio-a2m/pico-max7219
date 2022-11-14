import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, \
                           QLabel, QPushButton, QVBoxLayout, QHBoxLayout 
from inputData import LocalFile, Pico
from textElement import TextElement
from bitmapElement import BitmapElement, BitmapElementEditor


class ErrorElement(QWidget):

   def __init__(self,parent):
      super().__init__(parent)
      self.vbox_lo=QVBoxLayout()
      label = QLabel("Could not access kangurera device in USB port")
      self.vbox_lo.addWidget(label)
      self.setLayout(self.vbox_lo)

class Contoller(QWidget):

   def __init__(self,parent):
      super().__init__(parent)
      self.hbox_lo=QHBoxLayout()
      self.hbox_lo.addWidget(QLabel("Add new banner:"))
      kind_box=QComboBox(self)
      kind_box.addItems(["Text","Bitmap"])
      self.kind_box=kind_box
      self.hbox_lo.addWidget(kind_box)
      add_button=QPushButton(self)
      add_button.setText("Add")
      add_button.clicked.connect(partial(self.add_element))
      self.hbox_lo.addWidget(add_button)
      save_btn = QPushButton(self)
      save_btn.setText("Save")
      save_btn.clicked.connect(parent.extract_data)
      self.hbox_lo.addWidget(save_btn)

      self.setLayout(self.hbox_lo)

   def add_element(self):
      text=self.kind_box.currentText()
      self.parent().new_element(text)

class MainWindow(QWidget):
   
   def __init__(self, *args):
      super().__init__()
      #self.resize(800,600)
      self.setGeometry(0,0,800,600)
      self.setWindowTitle("Kangurera Config")
      vbox_lo=QVBoxLayout()
      #vbox_lo.addStretch(1)
      self.vbox_lo=vbox_lo
      

      self.setLayout(vbox_lo)
      self.pico=Pico()
      #self.pico = LocalFile("./content.json")
      self.load(self.pico.read())

      
   def load(self,data):
      if "error" in data:
         self.add_element(ErrorElement(self))
      elif "displays" in data:
         contoller=Contoller(self)
         self.add_element(contoller)
         for display in data["displays"]:
            if "bitmap" in display:
               self.add_element(BitmapElement(self,display["bitmap"]))
            elif "text" in display:
               self.add_element(TextElement(self,display["text"],display["effect"]))
         

   def add_element(self,element):
      self.widget = element
      self.vbox_lo.addWidget(element)

   def new_element(self,kind):
      print("creting::"+kind)
      if kind == "Bitmap":
         self.add_element(BitmapElement(self,[[0,0],[1,1],[2,2],[3,3]]))
      elif kind == "Text":
         self.add_element(TextElement(self,"hello","blink"))

   def extract_data(self):
      displays=[]
      for elem in self.children():         
         if isinstance(elem,TextElement) or isinstance(elem,BitmapElement):
            displays.append(elem.get_data())
      print(displays)
      self.pico.write({"displays":displays})


if __name__ == '__main__':
   app = QApplication(sys.argv)
   main_window = MainWindow()
   main_window.show()
   sys.exit(app.exec_())