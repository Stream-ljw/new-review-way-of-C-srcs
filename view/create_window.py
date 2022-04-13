import sys

from PyQt5.QtWidgets import QWidget, QMainWindow, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QAction, QMenu, QApplication
from PyQt5.QtCore import Qt, QObject, QDir, QFileInfo, QFile, QTextStream

class Window(QMainWindow):

    def __init__(self):
        super(Window,self).__init__()
        self.editor = QPlainTextEdit()        
        self.filename = ""
        self.create_Actions()
        self.create_MenuBar()
        
        #1. layout control
        layoutV = QVBoxLayout()
        layoutV.addWidget(self.menubar_field)
        layoutV.addWidget(self.editor)
        
        #2.  add layout into QWidget module to show
        mainQWiget = QWidget(self)
        mainQWiget.setLayout(layoutV)
       
        #3. QMainWindow.setCentralWidget takes ownership of the widget pointer
        #and deletes it at the approparite time. 
        self.setCentralWidget(mainQWiget)

    # create submenu and add action like open file
    def create_MenuBar(self):
        
        # first level menu : file
        self.menubar_field = self.menuBar()
        self.fileMenu = self.menubar_field.addMenu('&file')
        self.fileMenu.addAction(self.newAcion)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.exitAction)

       
    def create_Actions(self):

        #sencond level menu operation : open exit
        self.newAcion = QAction('&new', self)
        self.openAction = QAction('&open', self)
        self.exitAction = QAction('&exit', self)
        self.saveAction = QAction('&save', self)
        #define open file operation to openAction
        self.newAcion.triggered.connect(self.New_file_event)
        self.openAction.triggered.connect(self.Open_file_event)
        self.saveAction.triggered.connect(self.Save_file_event)
        self.exitAction.triggered.connect(self.close)

    #Implement create new plain text file to newAcion
    def New_file_event(self):
        
        self.filename = ''
        self.editor.clear()
        self.editor.setPlainText('')
        
        # reserved operation 
        #self.editor.moveCursor(self.cursor.End)        

    #Implement open file operation to openAction
    def Open_file_event(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath() + '/Document/' \
                'Text Files (*.txt *.c *.py);; All Files (*.*)')

        if path:
            inFile = QFile(path)
            
            if inFile.open(QFile.ReadWrite | QFile.Text):
                text = inFile.readAll()
                
                try:
                    text = str(text, encoding = 'utf-8')
                except TypeError:
                    text = str(text)
                
                self.editor.setPlainText(text)
                self.filename = path
                self.fname = QFileInfo(path).fileName()
                
                # sync fname to WindowTitile
                self.setWindowTitle(self.fname + '[*]')
    
    #Implement save file operation to saveAction
    def Save_file_event(self):
        # print('stream is saving file !!')

        #if filename isn't null, save action write modified content to origin path
        if self.filename != "":
            outfile = QFile(self.filename)

            #open file 
            if not outfile.open( QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self, "Error", "Cannot write file")
                return 

            # write file
            # QTextStream construct a QTextStream, must assign a device or a string before use it
            outContent = QTextStream(outfile)

            # set a wait period until write file successfully
            QApplication.setOverrideCursor(Qt.WaitCursor)
            outContent << self.editor.toPlainText()
            QApplication.restoreOverrideCursor()
            
            #update window title
            self.setWindowTitle(self.fname + '[*]')
        else:

            #save file that newly created
            self.Save_new_file()
    
    def Save_new_file(self):
        
        # new file means that need to choose a path to save 
        # QFileDialog.getSaveFileName method satisfy this need
        
        new_file_path, _ = QFileDialog.getSaveFileName(self, 'Save as..', self.filename, 'Python files (*.py)')

        if not new_file_path :
            QMessageBox.warning(self, 'Error', 'save file failed')
            return

        self.filename = new_file_path
        self.fname = QFileInfo(new_file_path).fileName()
        print('new_file_path is : %s' %(self.filename))

        return self.Save_file_event()





'''
if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = Window()
    ex.show()

    sys.exit(app.exec_())
'''
