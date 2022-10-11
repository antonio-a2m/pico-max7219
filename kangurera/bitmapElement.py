from functools import partial
from PyQt5.QtWidgets import QWidget, QCheckBox, QHBoxLayout, QGridLayout, QPushButton, QLabel 
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt



class BitmapElement(QWidget):
   def __init__(self,parent,coords):
      super().__init__()
      horizontal_box_lo=QHBoxLayout()
      horizontal_box_lo.addStretch(1)
      self.setLayout(horizontal_box_lo)
      self.data={"bitmap":coords}
      ed_btn = QPushButton(self)
      ed_btn.setText("Edit Bitmap")
      ed_btn.clicked.connect(self.edit_window)
      horizontal_box_lo.addWidget(ed_btn)
      self.drawn = False

   def changeCoords(self,coords):
      print("change corrds")
      self.data={"bitmap":coords}
      self.drawn = False
      self.update()

   def paintEvent(self, event):
      if not self.drawn:
         painter = QPainter(self)
               
         for row,col in self.data["bitmap"]:
            painter.fillRect(col*6+2,row*6+2,4,4,Qt.red)
         pen = QPen(Qt.gray, 0)
         painter.setPen(pen)
         painter.drawRect(0,0,32*6+2,8*6+2)
         painter.end()
         self.drawn = True

   def get_data(self):
      return self.data

   def edit_window(self):
      self.ed_w = BitmapElementEditor(None,self)
      self.ed_w.show()




class BitmapElementEditor(QWidget):
   def __init__(self,parent,bitmap_element):
      super().__init__(parent)
      self.coords=bitmap_element.data["bitmap"]
      print(self.coords)
      self.bitmap_element = bitmap_element
      self.grid_lo = QGridLayout()
      self.setLayout(self.grid_lo)
      for row in range(8):
         for col in range(32):
            cb=QCheckBox()
            cb.stateChanged.connect(partial(self.changed,[row,col]))
            self.grid_lo.addWidget(cb,row,col)      
      self._load_data()


   def _load_data(self):
      for row,col in self.coords:
        self.grid_lo.itemAtPosition(row,col).widget().setChecked(True)


   def changed(self,newcoords,status):
      if status == Qt.Checked :
         if newcoords not in self.coords:
            self.coords.append(newcoords)
      else:   
         self.coords.remove(newcoords)
      self.bitmap_element.changeCoords(self.coords)
