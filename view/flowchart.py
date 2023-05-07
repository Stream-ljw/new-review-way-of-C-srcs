import sys

from pyqtgraph.flowchart import Flowchart
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget

app = QApplication(sys.argv)

fc = Flowchart(terminals={
    'nameOfInputTerminal' : {'io': 'in'},
    'nameOfOutputTerminal' : {'io': 'out'}
})

ctrl = fc.widget()


window = QMainWindow()
window.setCentralWidget(ctrl)
window.show()

sys.exit(app.exec_())




