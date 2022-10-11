from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QHBoxLayout

class TextElement(QWidget):

   def __init__(self,parent,text,effect):
      super().__init__(parent)
      self.data={"text":text,"effect":effect}
      horizontal_box_lo=QHBoxLayout()
      horizontal_box_lo.addStretch(1)
      line_edit=QLineEdit(self)
      line_edit.setText(text)
      line_edit.textChanged.connect( self._update)
      self.line_edit=line_edit
      horizontal_box_lo.addWidget(line_edit)
      combo=QComboBox(self)
      combo.addItems(["verticalScroll","horizontalScroll","blink"])
      combo.setCurrentText(effect)
      combo.currentTextChanged.connect(self._update)
      self.combo=combo
      horizontal_box_lo.addWidget(combo)
      self.setLayout(horizontal_box_lo)



   def _update(self):
      self.data["text"]=self.line_edit.text()
      self.data["effect"]=self.combo.currentText()

   def get_data(self):
      return self.data