# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 23:39:10 2019

@author: Admin
"""
from datetime import datetime

def isTimeFormat(input):
    try:
        minute, second = input.split(':')
        if minute.isdigit() and second.isdigit():
            return True
    except ValueError:
        pass
    try:
        hour, minute, second = input.split(':')
        if hour.isdigit() and minute.isdigit() and second.isdigit():
            return True
    except ValueError:
        return False

def get_sec(time_str):
    try:
        m, s = time_str.split(':')
        return int(m) * 60 + int(s)
    except ValueError:
        pass
    try:
        h, m, s = time_str.split(':')
        return int(h)*3600 + int(m) * 60 + int(s)
    except ValueError:
        return False

def oliverEditor(file):
    
    edited_file = file.replace('.EPI','').replace('.epi','') + '_edited.epi'
    with open(file, 'r') as f:
        lines = f.readlines()
        with open(edited_file, 'w') as fw:
            with open("oliverSubfunction", 'r') as subfunction:
                for sub_line in subfunction:
                    fw.write(sub_line)
                subfunction.close()
                
            for line_index, line in enumerate(lines):
                
                if 'loop' in line:
                    words = line.strip().split()
                    for i,word in enumerate(words):
    #                    print(word)
                        loop_counter = 0
                        if word == 'loop' and words[i+2] == '{':
                            
                            loop_time = words[i+1]          
                            loop_start = line_index
                            for loop_index,item in enumerate(lines[line_index+1:]):
                                loop_words = item.strip().split()
                                for i,loop_word in enumerate(loop_words):
                                    if loop_word == '}' and loop_counter==0:
                                        loop_finish = line_index + loop_index+1
                                        loop = [lines[loop_start:loop_finish+1]* (int(loop_time))]
                                        loop_counter += 1
                                        fw.write(''.join(loop[0]))
                                        break
                                    break
                else:
                    fw.write(line)
    return fw.name

def martinEditor(input_file):
    '''Create the "_edited" files for Martin input files'''
    with open(input_file, 'r') as f:
        lines = []
        for line in f:
            split_line = line.split()
            for i,word in enumerate(split_line):
                first_word = split_line[0]
                if ',' or ';' in word:
                    split_line[i] = word.replace(',','').replace(';','')
                if first_word.isdigit():
                    m = int(int(first_word) / 60)
                    s = int(first_word) - m * 60
                    split_line[0] = word.replace(first_word,str(m)+':'+str(s))
                if split_line[i] == 'open' or split_line[i] == 'close':
                    split_line[i] = split_line[i].replace('open','= open').replace('close','= close')
                if 'ReactorTemp' in split_line[i]:
                    split_line[i] = word.replace(',','').replace(';','').replace('=', ' = ')
                if word == '>' or word =='>>':
                    del split_line[i]

            lines.append(' '.join(split_line) + '\n')
        del lines[-1]

    edited_file = input_file.replace('.EPI','').replace('.epi','') + '_edited.epi'
    with open(edited_file, 'w') as fw:
        for line in lines:
            if 'loop' in open(input_file).read():
                if 'loop' in line:
                    fw_split_line = line.split()
                    loop_time = fw_split_line[1]
                    loop_start = lines.index(line)
                elif '}' in line:
                    loop_finish = lines.index(line)
                    loop = [''.join(lines[loop_start:loop_finish+1]* (int(loop_time)-1))]
                    fw.write(loop[0])
                    continue

            fw.write(line)
    f.close()
    fw.close()
    return fw.name

def compound_writer(compounds):
    group_3 = set()
    group_5 = set()
    doping = set()
    # Access elements from compounds e.g. NH3 >> N
    for compound in compounds:
        if compound.startswith('T'):
            group_3.add(compound[2:4])
        elif compound.startswith('N'):
            group_5.add(compound[0])
        elif compound.startswith('Si'):
            doping.add(compound[0:3])
        elif compound.startswith('MCp'):
            doping.add('Mg')
            
    # Name compounds e.g. N Al Ga >> AlGaN

    my_compounds = set().union(group_3,group_5,doping)
#    return my_compounds
    if group_3 and group_5 and doping:
        if all(i in my_compounds for i in ['Ga','N','Al','Si']):
            return 'InGaN (Si)'
        elif all(i in my_compounds for i in ['Ga','N','Al','Mg']):
            return 'InGaN (Mg)'
        elif all(i in my_compounds for i in ['Ga','N','Mg']):
            return 'GaN (Mg)'
        elif all(i in my_compounds for i in ['Ga','N','Si']):
            return 'GaN (Si)'
        elif all(i in my_compounds for i in ['N','Al','Si']):
            return 'AlN (Si)'
        elif all(i in my_compounds for i in ['N','Al','Mg']):
            return 'AlN (Mg)'
    elif group_3 and group_5:
        if all(i in my_compounds for i in ['Al','Ga','N']):
            return 'AlGaN'
        elif all(i in my_compounds for i in ['In','Ga','N']):
            return 'InGaN'
        elif all(i in my_compounds for i in ['Ga','N']):
            return 'GaN'
        elif all(i in my_compounds for i in ['Al','N']):
            return 'AlN' 
        elif all(i in my_compounds for i in ['In','N']):
            return 'InN'
    elif group_5:
       return 0
    else:
        print("{} is missing, please consider adding the necessary compound".format(compounds))
        
        