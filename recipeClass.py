# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:22:58 2019

@author: Admin
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import cm
#import math
import xlwt
import string

#from inputEditors import martinEditor, oliverEditor
from utilities import isTimeFormat, get_sec,martinEditor, oliverEditor

#from martinInputEditor import martinEditor
#from oliverInputEditor import oliverEditor
#from isTimeFormat import isTimeFormat
#from getSec import get_sec


class Recipe:
    
    def __init__(self,recipe_name,recipe_path=False):
        self.recipe_name = recipe_name # Recipe name, file name with .epi
        
        if recipe_path == False:
            recipe_path = os.path.join(os.getcwd(),'recipes',self.recipe_name)
        
        self.recipe_path = recipe_path # File location
        self.recipe_edited = None
        
        if self.recipe_name[0] != 'T':
            self.recipe_edited = martinEditor(self.recipe_path)
        else:
            self.recipe_edited = oliverEditor(self.recipe_path)
            
        with open(self.recipe_edited) as f:
            self.contents = f.read()
#            for ch in [',',';']: #,'<<','>>','>'
#                clear_text = contents.replace(ch,'')
            self.clear_text = self.contents.replace(',','').replace(';','')
            self.words = self.clear_text.split()# List of text
          
        # Gases, Valves, Initial values of the flows, Reactor dictionary, List of variables in the reactor: ReactorTemp, ReactorPres etc., The times where the system makes changes, 00:30 etc.
        self.gas_flows, self.valves, self.initial_flows, self.reactor_variables, self.change_times = [[] for i in range(5)]
        self.init_vars_dict = {}
        self.updateVariable()
#        print(len(self.gas_flows),len(self.valves))
        self.cum_time = np.cumsum(self.change_times)
        
        self.gas_dic = {gas: [0]*(max(self.cum_time)+1) for gas in self.gas_flows}   # 
        self.valve_dic = {valve: [0]*(max(self.cum_time)+1) for valve in self.valves}
        self.reactor_variables_dic = {var: [0]*(max(self.cum_time)+1) for var in self.reactor_variables}

        self.variableTimeChanges()
        self.gasProcessor()
        self.valveProcessor()
        self.reactorProcessor()
#        print(len(list(self.gas_dic.keys())),len(list(self.valve_dic.keys())))
        
        self.all_gases ={key: [0]*(max(self.cum_time)+1) for key in self.gas_dic.keys()}
        self.allGasesProcessor()
        self.reactor_gases = {k: v for k,v in self.all_gases.items() if v != [0] * len(v)}
        self.reactorGases()
        self.semiconductor_layers = {}
        self.semiconductorLayers()
        self.semiconductor_draw = pd.DataFrame()
#        print(len(list(self.reactor_gases.keys())),len(list(self.semiconductor_layers.keys())),'\n')
        
        os.remove(os.path.abspath(self.recipe_edited))
        plt.show()
        f.close()
    def updateVariable(self):
        for i,word in enumerate(self.words[:-1]):
            if word == 'variable':  #Find the reactor variables, tempanpassung and rotation
                self.init_vars_dict[self.words[i+1]] = self.words[i+3]
                
            elif word[-1] == ':':     #Find the initial variables, TMGa_1 etc.
                if word[0] == 'T' or word[0:2] == 'Cp':
                    word = word.replace(':','')
                    var = word
                    self.initial_flows.append(var)
            # After that point, time and changing variables on that time are found
            elif isTimeFormat(word):
                self.change_times.append(get_sec(word))
            elif word == 'to' and self.words[i+1].isdigit():
                var = self.words[i-1]
                self.gas_flows.append(var)
            elif word == '=':
                '''When iterating valves, since the Martins input files give some weird valves (e.g. for, Prepare)
                if '.' structure is added.'''
                if self.words[i + 1] == 'open' or self.words[i + 1] == 'close':
                    if '.' in self.words[i-1]:
                        var = self.words[i-1]
                        self.valves.append(var)
                elif self.words[i-1].startswith('Reactor'):
                    self.reactor_variables.append(self.words[i-1])
            elif word == 'ReactorTemp' or word == 'ReactorPress':
                self.reactor_variables.append(word)
        self.reactor_variables = self.reactor_variables + [gas for gas in set(self.gas_flows) if not('.' in gas or 'Run' in gas or 'Push' in gas)]
        self.gas_flows = list(sorted(set(self.gas_flows)-set(self.reactor_variables)))
        self.valves = list(sorted(set(self.valves)))
        self.initial_flows = list(sorted(set(self.initial_flows)))
        self.reactor_variables = list(sorted(set(self.reactor_variables)))
        try:
            del self.reactor_variables['up']
        except:
            KeyError
#        for gas in gas_temp:
#        #Create reactor variables list
#        if '.' in gas or 'Run' in gas:
#            continue
#        else:
#            reactor_variables_temp.add(gas)
        
        self.change_times.insert(0,0)
#        print(len(set(gas_flows)-set(reactor_variables)))

        #Subtract common elements from gas lists
        return self.gas_flows, self.valves, self.initial_flows, self.reactor_variables, \
    self.valves, self.initial_flows, self.change_times, self.init_vars_dict
    
    def variableTimeChanges(self):
        
        count = 0
        for i,word in enumerate(self.words):
            try:
                if isTimeFormat(word):
                    count += 1
                elif word in self.gas_flows:
                    self.gas_dic[word][self.cum_time[count]] = float(self.words[i+2])
                elif word in self.valves:
                    if self.words[i+2] == 'open':
                        self.valve_dic[word][self.cum_time[count-1]] = 1
                    elif self.words[i+2] == 'close':
                        self.valve_dic[word][self.cum_time[count-1]] = -1
        #        elif word == 'in' and words[i-3] in gas_flows:
        #            index_with_in = cum_time[count-1]+int(words[i+1])
        #            gas_dic[words[i-3]][index_with_in] = float(words[i-1])
        #            if cum_time[count-1]+int(words[i+1]) not in cum_time:
        #                cum_time.insert(count,cum_time[count-1]+int(words[i+1]))
                elif word in self.reactor_variables and (self.words[i+1]=='to' or self.words[i+1]=='='):
                    if '+' in self.words[i+2]:
                        value = float(self.words[i+2][:self.words[i+2].index('+')])
                        init_var = self.words[i+2][self.words[i+2].index('+')+1:]
                        self.reactor_variables_dic[word][self.cum_time[count]] = value+float(self.init_vars_dict[init_var])#1100+TempAnpassung
                    elif '*' in self.words[i+2]:
                        value = float(self.words[i+2][:self.words[i+2].index('*')])
                        init_var = self.words[i+2][self.words[i+2].index('*')+1:]
                        
                        self.reactor_variables_dic[word][self.cum_time[count]] = value*float(self.init_vars_dict[init_var])#90*RotationAnpassFaktor
                    else:
                        self.reactor_variables_dic[word][self.cum_time[count]] = float(self.words[i + 2])
                    
            except:
                ValueError
        #        if self.recipe_name[0] == 'T':
        #            for i,time in enumerate(self.cum_time[:-1]):
        #                if self.cum_time[i+1]<time:
        #                    del self.cum_time[i]       
        return self.gas_dic, self.valve_dic, self.reactor_variables_dic
    
    def gasProcessor(self):
        
        for gas, list_values in self.gas_dic.items():
            for i,time in enumerate(self.cum_time[:-1]):
                next_step_value = list_values[self.cum_time[i + 1]]
                current_step_value = list_values[self.cum_time[i]]
                if next_step_value == 0:
                    list_values[self.cum_time[i+1]] = current_step_value

        
        for gas_name, value_list in self.gas_dic.items():
            for i, current_time in enumerate(self.cum_time[:-1]):

                next_step_value = value_list[self.cum_time[i + 1]]
                current_step_value = value_list[self.cum_time[i]]
    
                if next_step_value == current_step_value:
                    value_list[current_time+1 : self.cum_time[i + 1]] = \
                        [next_step_value for x in range(len(value_list[current_time+1:self.cum_time[i+1]]))]
    
                elif next_step_value != current_step_value:
                    if all(a == 0 for a in value_list[current_time+1:self.cum_time[i+1]]):
                        value_list[current_time+1:self.cum_time[i + 1]] = [current_step_value + \
                        round((next_step_value-current_step_value)/(len(value_list[current_time+1:self.cum_time[i+1]])+1)*(count+1),1) \
                        for count in range(len(value_list[current_time+1:self.cum_time[i+1]]))]
                    else:

                        for index, x in enumerate(value_list[current_time:self.cum_time[i + 1]]):
                            if x != 0:
                                in_index, in_value = index, x

                        value_list[current_time+1:(current_time+in_index)] = [current_step_value + round((in_value - \
                        current_step_value)/(len(value_list[current_time+1:(current_time+in_index)])+2)*(count+1),1) \
                        for count in range(len(value_list[current_time+1:(current_time+in_index)]))]
    
                        value_list[(current_time+in_index+1):self.cum_time[i+1]] = \
                        [in_value for x in range(len(value_list[(current_time+in_index+1):self.cum_time[i+1]]))]

        return self.gas_dic
    
    def valveProcessor(self):
        
        for valve_name, value_list in self.valve_dic.items():
            for i, step_time in enumerate(self.cum_time[:-1]):

                next_step_value = value_list[self.cum_time[i + 1]]
                current_step_value = value_list[self.cum_time[i]]
                if next_step_value == 0:
                    value_list[self.cum_time[i]:self.cum_time[i + 1]] = \
                        [current_step_value for x in value_list[self.cum_time[i]:self.cum_time[i + 1]]]
                    value_list[self.cum_time[i + 1]] = current_step_value
                else:
                    value_list[self.cum_time[i]:self.cum_time[i + 1]] = \
                        [current_step_value for x in value_list[self.cum_time[i]:self.cum_time[i + 1]]]

        
        for valve_name, value_list in self.valve_dic.items():
            for i, x in enumerate(value_list):
                if x == -1:
                    value_list[i] = 0
                    
        return self.valve_dic

    def reactorProcessor(self):
        
        for var, list_values in self.reactor_variables_dic.items():
            for i,time in enumerate(self.cum_time[:-1]):
                next_step_value = list_values[self.cum_time[i + 1]]
                current_step_value = list_values[self.cum_time[i]]
                if next_step_value == 0:
                    list_values[self.cum_time[i+1]] = current_step_value

        for var, value_list in self.reactor_variables_dic.items():
            for i, current_time in enumerate(self.cum_time[:-1]):
        
                next_step_value = value_list[self.cum_time[i + 1]]
                current_step_value = value_list[self.cum_time[i]]
        
                if next_step_value == current_step_value:
                    value_list[current_time+1 : self.cum_time[i + 1]] = \
                        [next_step_value for x in range(len(value_list[current_time+1:self.cum_time[i+1]]))]
        
                elif next_step_value != current_step_value:
                    if all(a == 0 for a in value_list[current_time+1:self.cum_time[i+1]]):
                        # print(value_list[current_time:cum_time[i+1]])
                        value_list[current_time+1:self.cum_time[i + 1]] = [current_step_value + \
                        round((next_step_value-current_step_value)/(len(value_list[current_time+1:self.cum_time[i+1]])+1)*(count+1),1) \
                        for count in range(len(value_list[current_time+1:self.cum_time[i+1]]))]
                    else:
                        for index, x in enumerate(value_list[current_time:self.cum_time[i + 1]]):
                            if x != 0:
                                in_index, in_value = index, x

                        value_list[current_time+1:(current_time+in_index)] = [current_step_value + round((in_value - \
                        current_step_value)/(len(value_list[current_time+1:(current_time+in_index)])+2)*(count+1),1) \
                        for count in range(len(value_list[current_time+1:(current_time+in_index)]))]
        
                        value_list[(current_time+in_index+1):self.cum_time[i+1]] = \
                        [in_value for x in range(len(value_list[(current_time+in_index+1):self.cum_time[i+1]]))]
        return self.reactor_variables_dic
            
    def allGasesProcessor(self):
        for gas_key, gas_value in self.gas_dic.items():
            gas_name = gas_key.replace('.source', '')
            #.replace('.push','').replace('.inject','')
            if gas_name + '.run' in self.valve_dic.keys():
                # print(gas_name)
                for index, step in enumerate(self.valve_dic[gas_name + '.run']):
                    if step == 1:
                        self.all_gases[gas_name + '.source'][index] = self.gas_dic[gas_name+'.source'][index]
                        try:
                            self.all_gases[gas_name + '.push'][index] = self.gas_dic[gas_name + '.push'][index]
                            self.all_gases[gas_name + '.inject'][index] = self.gas_dic[gas_name + '.inject'][index]
                        except:
                            KeyError
            elif gas_name.startswith('Run') or gas_name.startswith('Push'):
                self.all_gases[gas_name] = gas_value
        return self.all_gases

    def reactorGases(self):
        
        try:
            del self.reactor_gases['SiH4_1.source']
        except:
            KeyError
        
        reactor_gases_total = []
        
        for i in range(max(self.cum_time)+1):
            temp = 0
            for gas in self.reactor_gases.keys():
                temp += self.reactor_gases[gas][i]
            reactor_gases_total.append(temp)

        self.reactor_gases['Total'] = reactor_gases_total
        
        return self.reactor_gases
    
    def semiconductorLayers(self):

        for valve, valve_list in self.valve_dic.items():
            valve_name = valve.replace('.line','')
            run_valve = '{}.run'.format(valve_name)
            line_valve = '{}.line'.format(valve_name)
            gas_name = valve_name
            gas_source_name = '{}.source'.format(gas_name)
            if run_valve in self.valve_dic.keys() and line_valve in self.valve_dic.keys():
                if gas_name == 'SiH4_1':
                    self.semiconductor_layers['SiH4_1'] = len(valve_list)*[0]
                    for i,(src,inj,dil) in enumerate(zip(self.gas_dic[gas_source_name],self.gas_dic[gas_name + '.inject'],self.gas_dic[gas_name + '.dilute'])):
                        if (self.valve_dic[run_valve][i],self.valve_dic[line_valve][i]) == (1,1):
                            if (src+dil != 0):
                                self.semiconductor_layers[gas_name][i] = src*inj/(src+dil)
                            else:
                                self.semiconductor_layers[gas_name][i] = 0
                elif any(self.valve_dic[run_valve]) and any(self.valve_dic[line_valve]):
                    try:
                        self.gas_dic[gas_source_name]
                        self.semiconductor_layers[gas_source_name] = len(valve_list)*[0]
                        for index, step in enumerate(zip(self.valve_dic[run_valve],self.valve_dic[line_valve])):
                            if step == (1,1):
                                self.semiconductor_layers[gas_source_name][index] = self.gas_dic[gas_source_name][index]
                        
                    except:
                        KeyError
        
        return self.semiconductor_layers

    
    def draw_semiconductor(self):
        '''Draw the semiconductor using semiconductor_layers gases'''
        TMGa_1_constant = 1/30
        TEGa_constant = 1/2880*3
        TMAl_1_constant = 1/360
        TMIn_2_constant = 1/5000
#        constants_dict = {'TMGa_1':1/30,}
        

        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax = plt.gca()
        fig.canvas.set_window_title('Semiconductor: {}'.format(self.recipe_name))
        
        def layers_with_flows():
            my_dict = {key.split('_')[0]:value for key,value in self.semiconductor_layers.items()}
            df = self.semiconductor_draw
            df =  pd.DataFrame.from_dict(my_dict, orient='index')
            layer_thickness = 0 
            thickness_flows = []
            for i_data in range(len(df.iloc[0,])-1):
                # Iterate every second for every flow in semiconductor_layers dictionary
                data = df.iloc[:,i_data]
    
                if any(data):
                    # Check if any gas flow is greater than zero
    #                flow_indices = np.transpose(np.nonzero(data))
                    flow_indices= np.nonzero(data)
                    next_flow_indices = np.nonzero(df.iloc[:,i_data+1])
        
    #                if not np.array_equal(flow_indices,next_flow_indices):
    #                    print(semiconductor_layer)
    #                    semiconductor_layer = 0
                    
                    for flow_index in flow_indices:
                        for index in flow_index:
                            # Iterate nonzero gas flows by index
                            if df.index[index] == 'TMGa':
                                layer_thickness += TMGa_1_constant * data[index]
                            elif df.index[index] == 'TEGa':
                                layer_thickness += TEGa_constant * data[index]
                            elif df.index[index] == 'TMAl':
                                layer_thickness += TMAl_1_constant * data[index]
                            elif df.index[index] == 'TMIn':
                                layer_thickness += TMIn_2_constant * data[index]
    
    
                    if not np.array_equal(flow_indices,next_flow_indices):
                        thickness_flows.append(([df.index[index] for flow_index in flow_indices for index in flow_index],layer_thickness))
                        layer_thickness = 0
#            print(thickness_flows)
            return thickness_flows
#        print(layers_with_flows())
        def semiconductor():
            
            layers = layers_with_flows()
#            scale_factor = 10**-2
            previous_layer_thickness = 0
            key_list_layer = [gas_list[0] for gas_list in layers]
            key_list_set = []
            for key_list in key_list_layer:
                if key_list not in key_list_set:
                    key_list_set.append(key_list)

            color_bar = cm.get_cmap('tab10')
            colors = color_bar(np.linspace(0, 1, len(key_list_set)))
            color_labels = [letter for letter in string.ascii_lowercase[0:len(key_list_set)]]
            previous_colors = []
            semiconductor_layers = []
#            ax.legend([color for color in colors],[key_list for key_list in key_list_set])
#            print(layers)
            for i_layer,layer in enumerate(layers):
                gases = layer[0]
                thickness = layer[1] * 10**-3
                
                micrometer_check = False
#                if len(str(thickness/10**-3).split('.')[0]) >= 3:
#                    thickness_label = thickness * 10**-3
#                    micrometer_check = True
#                    thickness = thickness / 10
#                else:
#                    thickness = thickness * 10
                
                color = colors[key_list_set.index(gases)]
                color_label = color_labels[key_list_set.index(gases)]
                semiconductor_layer = Rectangle((0,previous_layer_thickness),4,thickness,color=color,label=gases)#=['{}-'.format(gas) for gas in gases[:-1]]
                previous_layer_thickness += thickness
                ax.add_patch(semiconductor_layer)
                if thickness and micrometer_check:
                    ax.text(4.01,previous_layer_thickness-thickness/2,'{} $\mu$'.format(str(thickness)[0:4]))
                elif thickness:
                    ax.text(4.001,previous_layer_thickness-thickness/2,'{} nm'.format(str(thickness/10**-3)[0:4]))
                
                if not color_label in previous_colors:
                    previous_colors.append(color_label)
                    semiconductor_layers.append(semiconductor_layer)


            ax.legend(handles=semiconductor_layers,loc='lower right')
            
            ax.set_xlim([-0.1,10])
            ax.set_ylim([-0.1,previous_layer_thickness+1.5])
            plt.show()
            return ax
        return semiconductor()
#    
    def plot_dict(self,my_dict,my_dict_title):
#        window_titles = ['Reactor gases: ', 'Semiconductor layers: ', 'Gas flows: ','Lines and Runs: ','Reactor properties: ']
        
        color_bar = cm.get_cmap('tab20')
        colors = color_bar(np.linspace(0, 1, len(my_dict)))
        
        df =  pd.DataFrame.from_dict(my_dict, orient='index')
        fig,axes = plt.subplots(nrows=int(len(my_dict)),ncols=1,sharex=True)
        fig.canvas.set_window_title(my_dict_title+str(self.recipe_name))
#        fig.canvas.set_window_title(window_titles[dict_index].format(self.recipe_name))
        if len(my_dict) ==1:
            axes.plot(df.values[0],color=colors[0], label=df.index[0])
            axes.set_ylim(0,max(df.values[0])*1.2)
            axes.legend()
        else:
            for i in range(1,len(my_dict)+1):
                axes[i-1].plot(df.values[i-1],color=colors[i-1], label=df.index[i-1])
                axes[i-1].set_ylim(0,max(df.values[i-1])*1.2)
                axes[i-1].legend()
        fig.tight_layout()
        plt.show()
        return fig
        
    def write_excel(self):
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet(self.recipe_name)
        count = 1
        index = 1
        for keys, values in self.reactor_gases.items():
            # Add gas names to first row
            sheet1.write(0, count, keys)
            for i, value in enumerate(values):
                # Insert values
                sheet1.write(i + 1, count, value)
                if index == 1:
                    # Add time in seconds
                    sheet1.write(i + 1, 0, i)
            count += 1
            index = 0
    
        # Add time title
        sheet1.write(0, 0, 'Time(sec)')
    
        book.save(self.recipe_name.replace('.epi','').replace('.EPI','') + "_data.xls")
        return book


#all_recipes = ['GaN_1.EPI', 'InGaN_QW.EPI', 'T2118GQTs.epi', 'T3025GSa.epi', 'T3039Ga.epi', 'T3130GnSa.epi', 'Y1129.EPI', 'Y1914GQT.EPI', 'Y2041GA.EPI', 'Y2075GQA.EPI', 'Y2096GPA.EPI', 'Y2131GQA.EPI']
#my_recipe = Recipe('Y1914GQT.EPI')
#my_recipe.draw_semiconductor()
#my_recipe = Recipe('T2118GQTs.epi')
#my_recipe.draw_semiconductor()
#my_recipe = Recipe('T3025GSa.epi')
#my_recipe.plot_dict(my_recipe.semiconductor_layers,'semiconductor')
#my_recipe = Recipe('T9173GLSa_edit.epi')
#my_recipe.draw_semiconductor()
#my_recipe.plot_dict(my_recipe.semiconductor_layers,'Semiconductor layers: ')
#plt.show()


