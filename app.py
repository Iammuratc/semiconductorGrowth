import sys
from PyQt5.QtWidgets import QLabel,QPushButton,QTextEdit,QMainWindow, \
                            QListWidget,QAbstractItemView,QApplication, \
                            QWidget,QGridLayout,QFileDialog,QListWidgetItem, QVBoxLayout
                            
from PyQt5 import QtGui, QtCore
import matplotlib.pyplot as plt

import os
from recipeClass import Recipe

class Window(QMainWindow):

#    got_recipe = QtCore.pyqtSignal(list)
    global_path = None
    
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.recipe = '000.epi'
        self.recipe_class = Recipe(self.recipe)
        self.file_path = os.path.join(os.getcwd(),'recipes',self.recipe)
#        self.got_recipe.emit('ananin ami')
        self.text_editor = TextEditor()
        self.text_editor.got_text.connect(self.editor_input)
        
        
        self.left = 20
        self.top = 20
        self.width = 500
        self.height = 500
        
        self.title ='MOVPE Recipe'
        self.initUI()

        
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        self.file_notify = QLabel(self)
        self.file_notify.setText('Pick a recipe')
        
        self.recipe_button = QPushButton('Recipe folder')
        self.recipe_button.clicked.connect(self.get_input)
        
        self.b_reactor = QPushButton('Reactor gases')
        self.b_reactor.clicked.connect(self.plot_reactor)
        
        self.b_reactor_pro = QPushButton('Reactor properties')
        self.b_reactor_pro.clicked.connect(self.plot_reactor_properties)
        
        self.b_sc_layers = QPushButton('Semiconductor layers')
        self.b_sc_layers.clicked.connect(self.plot_semiconductor)
        
        self.b_gas = QPushButton('Gases')
        self.b_gas.clicked.connect(self.plot_gases)
        
        self.b_valves = QPushButton('Valves')
        self.b_valves.clicked.connect(self.plot_valves)

        
#        self.text_recipe = QTextEdit(self)

        self.b_any = QPushButton('Plot all highlighted items')
        self.b_any.clicked.connect(self.plot_any)
        
        self.qlistwidget_reactor_gas = QListWidget()
        self.qlistwidget_reactor_gas.setSelectionMode(QAbstractItemView.MultiSelection)
        self.qlistwidget_reactor_gas.itemSelectionChanged.connect(self.select_reactor_gas)
        
        self.qlistwidget_sc_gas = QListWidget()
        self.qlistwidget_sc_gas.setSelectionMode(QAbstractItemView.MultiSelection)
        self.qlistwidget_sc_gas.itemSelectionChanged.connect(self.select_sc_gas)
        
        self.qlistwidget_gas = QListWidget()
        self.qlistwidget_gas.setSelectionMode(QAbstractItemView.MultiSelection)
        self.qlistwidget_gas.itemSelectionChanged.connect(self.select_gas)
        
        self.qlistwidget_valve = QListWidget()
        self.qlistwidget_valve.setSelectionMode(QAbstractItemView.MultiSelection)
        self.qlistwidget_valve.itemSelectionChanged.connect(self.select_valve)
        
        self.qlistwidget_reactor_prop = QListWidget()
        self.qlistwidget_reactor_prop.setSelectionMode(QAbstractItemView.MultiSelection)
        self.qlistwidget_reactor_prop.itemSelectionChanged.connect(self.select_reactor_prop)
        
        
        self.qlistwidgets = [self.qlistwidget_reactor_gas,self.qlistwidget_sc_gas,
                             self.qlistwidget_gas,self.qlistwidget_valve,
                             self.qlistwidget_reactor_prop]
#        self.functions = [self.select_reactor_gas,self.select_sc_gas,
#                          self.select_gas,self.select_valve,
#                          self.select_reactor_prop]
        

        
        mainMenu = self.menuBar()
        excel = mainMenu.addMenu('Excel')
        excel_a = excel.addAction('Reactor gases')
        excel_a.triggered.connect(self.excel_reactor)
        excel_b = excel.addAction('Semiconductor layers')
        excel_b.triggered.connect(self.excel_semiconductor)
        excel_c = excel.addAction('All gases')
        excel_c.triggered.connect(self.excel_gases)
        excel_d = excel.addAction('All valves')
        excel_d.triggered.connect(self.excel_valves)
        excel_e = excel.addAction('Reactor properties')
        excel_e.triggered.connect(self.excel_reactor_properties)
        
        tools = mainMenu.addMenu('Tools')
        semiconductor_a = tools.addAction('Draw semiconductor')
        semiconductor_a.triggered.connect(self.draw_semiconductor)
        semiconductor_b = tools.addAction('Draw semiconductor 2')
        semiconductor_b.triggered.connect(self.draw_semiconductor_2)
        editor = tools.addAction('Recipe Editor')
        editor.triggered.connect(self.open_editor)
        
        
        
#        for listwidget in self.qlistwidgets:
#            listwidget.setMinimumWidth(listwidget.sizeHintForColumn(0))
        
        # set the layout
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QGridLayout()
        wid.setLayout(layout)
    
        
        layout.addWidget(self.recipe_button,0,0,1,5)
        layout.addWidget(self.file_notify,1,2,1,3)

        layout.addWidget(self.b_reactor,2,0)
        layout.addWidget(self.qlistwidget_reactor_gas,3,0)


        layout.addWidget(self.b_sc_layers,2,1)
        layout.addWidget(self.qlistwidget_sc_gas,3,1)
        
        layout.addWidget(self.b_gas,2,2)
        layout.addWidget(self.qlistwidget_gas,3,2)
        
        layout.addWidget(self.b_valves,2,3)
        layout.addWidget(self.qlistwidget_valve,3,3)
        
        layout.addWidget(self.b_reactor_pro,2,4)
        layout.addWidget(self.qlistwidget_reactor_prop,3,4)
        
        layout.addWidget(self.b_any,5,0,6,5)
#        layout.addWidget(self.text_recipe,11,0,12,5)
        
#        dialog = TextEditor(self)
#        dialog.show()




    def get_input(self):
        # Clear all variables
#        self.text_recipe.clear()

        for qlistwidget in self.qlistwidgets:
            qlistwidget.clear()
        
        # Open the input recipe
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_line,_ = QFileDialog.getOpenFileName(self,'Open file', 
            os.path.join(os.getcwd(),'recipes'),'(*.epi)', options=options)
        
        self.file_path = os.path.abspath(file_line)

        # Write the recipe to the app text editor
        self.recipe = os.path.basename(self.file_path)


#        with open(self.file_path,'r') as fo:
#            text = fo.read()
        Window.global_path = self.file_path
#            self.got_recipe.emit(text)
#            TextEditor.text_recipe.setText(text)
        
        self.recipe_class = Recipe(self.recipe,self.file_path)
        
        
#        print(self.recipe,file_path)
        self.file_notify.setText('Current recipe: {}'.format(self.recipe))
        

        recipe_dics = [self.recipe_class.reactor_gases,self.recipe_class.semiconductor_layers,
                       self.recipe_class.gas_dic,self.recipe_class.valve_dic,self.recipe_class.reactor_variables_dic]
        
        for dic,dic_list in zip(recipe_dics,self.qlistwidgets):
            for n in dic.keys():
                item = QListWidgetItem(str(n))
                if n in dic.keys():
                    dic_list.addItem(item)
                else:
                    pass
                item.setSelected(False)
        
    def open_editor(self):
#        dialog = TextEditor()
        self.text_editor.show()


    def editor_input(self,text):
#        editor = TextEditor()
#        recipe_text = editor.text_recipe.toPlainText()
#        recipe_text = self.text_recipe.toPlainText()
        
        with open('editor_recipe.epi','w+') as f:
            f.write(text)
        
        f_path = os.path.join(os.getcwd(),'editor_recipe.epi')
#        print(self.recipe,f_path)

        self.recipe_class = Recipe(self.recipe,f_path)
        
        self.file_notify.setText('Current recipe: {} (modified)'.format(self.recipe))
        
        # Add corresponding items to each qlistwidgets  
        for qlistwidget in self.qlistwidgets:
            qlistwidget.clear()

        recipe_dics = [self.recipe_class.reactor_gases,self.recipe_class.semiconductor_layers,
                       self.recipe_class.gas_dic,self.recipe_class.valve_dic,self.recipe_class.reactor_variables_dic]
        
        for dic,dic_list in zip(recipe_dics,self.qlistwidgets):
            for n in dic.keys():
                item = QListWidgetItem(str(n))
                if n in dic.keys():
                    dic_list.addItem(item)
                else:
                    pass
                item.setSelected(False)
            

        os.remove(os.path.abspath(f_path))


    
    def select_sc_gas(self):
        selected_items = self.qlistwidget_sc_gas.selectedItems()
        selected_gases_dict = {item.text(): self.recipe_class.semiconductor_layers[item.text()] for item in selected_items}
        return selected_gases_dict

    def select_reactor_gas(self):
        selected_items = self.qlistwidget_reactor_gas.selectedItems()
        selected_gases_dict = {item.text(): self.recipe_class.reactor_gases[item.text()] for item in selected_items}
        return selected_gases_dict
    
    def select_gas(self):
        selected_items = self.qlistwidget_gas.selectedItems()
        selected_gases_dict = {item.text(): self.recipe_class.gas_dic[item.text()] for item in selected_items}
        return selected_gases_dict
    
    def select_valve(self):
        selected_items = self.qlistwidget_valve.selectedItems()
        selected_gases_dict = {item.text(): self.recipe_class.valve_dic[item.text()] for item in selected_items}
        return selected_gases_dict
    
    def select_reactor_prop(self):
        selected_items = self.qlistwidget_reactor_prop.selectedItems()
        selected_gases_dict = {item.text(): self.recipe_class.reactor_variables_dic[item.text()] for item in selected_items}
        return selected_gases_dict
 
    def plot_reactor(self):
        return self.recipe_class.plot_dict(self.select_reactor_gas(), 'Reactor gases: ')
    
    def plot_semiconductor(self):
        return self.recipe_class.plot_dict(self.select_sc_gas(), 'Semiconductor layers: ')
    
    def plot_reactor_properties(self):
        return self.recipe_class.plot_dict(self.select_reactor_prop(), 'Reactor properties: ')    
    
    def plot_gases(self):
        return self.recipe_class.plot_dict(self.select_gas(), 'Gas flows: ')
    
    def plot_valves(self):
        return self.recipe_class.plot_dict(self.select_valve(), 'Lines and Runs: ')
    
    def plot_any(self):
#        r_dict = self.select_reactor_gas()
        r_dict = {"{}_r".format(key):value for (key,value) in self.select_reactor_gas().items()}
        s_dict = {"{}_s".format(key):value for (key,value) in self.select_sc_gas().items()}
        my_dict = {**self.select_gas(),**self.select_valve(),**r_dict,**s_dict,**self.select_reactor_prop()}
        return self.recipe_class.plot_dict(my_dict, 'Selected flows: ')
    
    def excel_reactor(self):
        return self.recipe_class.write_excel(self.recipe_class.reactor_gases(), 'reactor_gases')
    
    def excel_semiconductor(self):
        return self.recipe_class.write_excel(self.recipe_class.semiconductor_layers(), 'semiconductor_layers') 
    
    def excel_gases(self):
        return self.recipe_class.write_excel(self.recipe_class.gas_dic(), 'gas_flows')
    
    def excel_valves(self):
        return self.recipe_class.write_excel(self.recipe_class.valve_dic(), 'lines_runs')

    def excel_reactor_properties(self):
        return self.recipe_class.write_excel(self.recipe_class.reactor_variables_dic(), 'reactor_properties')   
    
    def draw_semiconductor(self):
        return self.recipe_class.draw_semiconductor(real_semiconductor=True)
    def draw_semiconductor_2(self):
        return self.recipe_class.draw_semiconductor(real_semiconductor=False)

class TextEditor(QWidget):
    
   got_text = QtCore.pyqtSignal(str)
    
   def __init__(self):
        super(TextEditor, self).__init__()
        self.text_recipe = QTextEdit(self)
        
        # Init user interface
        self.initUI()
        
   def initUI(self):
        
        save_b = QPushButton('Save')
        save_b.clicked.connect(self.save_text)
        load_b = QPushButton('Load recipe')
        load_b.clicked.connect(self.load_text)
        
        export_b = QPushButton('Export text')
        export_b.clicked.connect(self.export_text)
        
#        layout = QVBoxLayout()
#        layout.addStretch(1)
#        layout.addWidget(self.text_recipe)
#        self.setLayout(layout)
        
        
        layout = QVBoxLayout()
        layout.addWidget(load_b)
        layout.addWidget(self.text_recipe)
        layout.addWidget(export_b)
        layout.addWidget(save_b)
        self.setLayout(layout)
        self.setMinimumWidth(350)
        
#        layout = QGridLayout()
#        wid.setLayout(layout)
#        layout.addWidget(self.text_recipe,0,1,5,5)
#        layout.addWidget(load_b,0,0)
#        layout.addWidget(save_b,1,6)
#        layout.addWidget(export_b,2,6)
        
        
   def load_text(self):
       with open(Window.global_path,'r') as fo:
           text = fo.read()
           self.text_recipe.setText(text)
           
   def save_text(self):
       options = QFileDialog.Options()
#       options |= QFileDialog.DontUseNativeDialog
       fileName, _ = QFileDialog.getSaveFileName(self,"Save modified recipe","","Text Files (*.epi)", options=options)

       
       plain_text = self.text_recipe.toPlainText()
#        recipe_text = self.text_recipe.toPlainText()
        
       with open(fileName,'w+') as f:
           
           f.write(plain_text)
           
   def export_text(self):
       self.got_text.emit(self.text_recipe.toPlainText())
        
        
if __name__ == '__main__':
    
    try:
        os.mkdir('/recipes')
    except:
        FileExistsError
    
    with open('recipes/000.epi','w+') as f:
        f.write('0')

    app = QApplication(sys.argv)
    main = Window()
    main.setWindowIcon(QtGui.QIcon('icon.png'))
    main.show()
    app.exec_()
#    plt.close('all')
#    sys.exit(app.exec_())
    os.remove(os.path.abspath('recipes/000.epi'))
    
       
    