import sys
from PyQt5.QtWidgets import QListWidgetItem,QGridLayout,QAbstractItemView,QListWidget,QFileDialog,QDialog, QApplication, QPushButton, QLabel, QTextEdit
from PyQt5 import QtGui
from PyQt5 import QtCore

import os
from recipeClass import Recipe

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
#        self.showMaximized()
#        self.setupUi(self)
        self.setWindowFlags(
        QtCore.Qt.Window |
        QtCore.Qt.CustomizeWindowHint |
        QtCore.Qt.WindowTitleHint |
        QtCore.Qt.WindowCloseButtonHint |
#        QtCore.Qt.WindowStaysOnTopHint |
        QtCore.Qt.WindowMinimizeButtonHint |
        QtCore.Qt.WindowMaximizeButtonHint
        )
        
        # Buttons connected to `plot` method
        self.recipe = 'T2118GQTs.epi'
        self.recipe_class = Recipe(self.recipe)
        
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
        
        self.b_excel = QPushButton('Write reactor gases to excel')
        self.b_excel.clicked.connect(self.write_excel)
        
        self.b_draw_sc = QPushButton('Draw semiconductor')
        self.b_draw_sc.clicked.connect(self.draw_semiconductor)
        
        self.text_recipe = QTextEdit(self)
        self.b_takeFromQtextedit = QPushButton('Load changes')
        self.b_takeFromQtextedit.clicked.connect(self.editor_input)
        
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

#        for listwidget in self.qlistwidgets:
#            listwidget.setMinimumWidth(listwidget.sizeHintForColumn(0))
        
        # set the layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.recipe_button,0,0,1,5)
        layout.addWidget(self.file_notify,1,2,1,3)

        layout.addWidget(self.b_reactor,2,0)
        layout.addWidget(self.qlistwidget_reactor_gas,3,0)
        layout.addWidget(self.b_excel,4,0)

        layout.addWidget(self.b_sc_layers,2,1)
        layout.addWidget(self.qlistwidget_sc_gas,3,1)
        layout.addWidget(self.b_draw_sc,4,1)
        
        layout.addWidget(self.b_gas,2,2)
        layout.addWidget(self.qlistwidget_gas,3,2)
        
        layout.addWidget(self.b_valves,2,3)
        layout.addWidget(self.qlistwidget_valve,3,3)
        
        layout.addWidget(self.b_reactor_pro,2,4)
        layout.addWidget(self.qlistwidget_reactor_prop,3,4)
        
        layout.addWidget(self.b_takeFromQtextedit,5,0,6,5)
        layout.addWidget(self.text_recipe,11,0,12,5)
        

    def get_input(self):
        # Clear all variables
        self.text_recipe.clear()

        for qlistwidget in self.qlistwidgets:
            qlistwidget.clear()
        
        # Open the input recipe
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_line,_ = QFileDialog.getOpenFileName(self,'Open file', 
            os.path.join(os.getcwd(),'recipes'),'(*.epi)', options=options)
        
        file_path = os.path.abspath(file_line)

        # Write the recipe to the app text editor
        self.recipe = os.path.basename(file_path)
        fo = open(file_path,'r')
        with fo:
            text = fo.read()
            self.text_recipe.setText(text)
        
        self.recipe_class = Recipe(self.recipe,file_path)
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
        
    def editor_input(self):
        recipe_text = self.text_recipe.toPlainText()
        
        with open('editor_recipe.epi','w+') as f:
            f.write(recipe_text)
        f.close()
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
    
    def write_excel(self):
        return self.recipe_class.write_excel()
    
    def draw_semiconductor(self):
        return self.recipe_class.draw_semiconductor()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.setWindowTitle('MOVPE Recipe')
    main.setWindowIcon(QtGui.QIcon('icon.png'))
    main.show()
    app.exec_()
    
       
