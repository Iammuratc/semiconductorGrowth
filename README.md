# Project name: MOVPE input analyzer

# What is metal organic vapor phase epitaxy (MOVPE)?
Semiconductors form the basis of modern electronic devices such as transistors, diodes and lasers. For example, nitride semiconductors (e.g. GaN/AlGaN, InN) are widely used in optoelectronic devices such as LEDs and detectors. The production of nitride semiconductors with desired properties (resistance, sensitivity to light etc.) requires a complex and diligent process. One of the production methods for nitride semiconductors is metal organic vapor phase epitaxy (MOVPE), where epitaxy describes an ordered crystalline growth. This method employs each element (Ga, N, In etc.) in the gas form to build the semiconductor structure. However, the production of group III elements (Ga, In, Al) as gases is a difficult task due to physical reasons, that's why, these elements are bound to metal organic compounds (e.g. Trimethyl-gallium, TMGa). Eventually, the MOVPE method produces the desired nitride semiconductor structure by the reaction of such compounds at various amounts and time intervals. (See https://en.wikipedia.org/wiki/Metalorganic_vapour-phase_epitaxy for details.)

# What is MOVPE input analyzer?
The MOVPE method consists of various gas sources, valves to control the flow of these gases and a reactor where the gases react to build the semiconductor. In that manner, input of the MOVPE method simply gives the recipe of the semiconductor, which describes the amount of each gas at certain time intervals. The MOVPE input analyzer provides an user friendly handling for these input files, see an example input file under the folder 'inputs'. 
## Usage
You may see a screenshot from the application below. The 3rd and 4rd columns show the gases and valves used in the recipe, and you can plot the flows of each gas and valve over time by using the buttons above. There are two different valves for each gas, called run and line valves. Depending on the position of these valves (0 close, 1 open), the semiconductor growth occurs in the reactor. The 1st column shows the flow of gas if the corresponding run valve is open. If both valves (line and run) are open, the semiconductor growth occurs, where these gases are listed under the 2nd column. Finally, the reactor properties (temperature, pressure etc.) are listed under the 5th column. You can plot each gas flow under every column, where the y-axis is flow rate (ccpm) and the x-axis is time (sec).

![Preview of the application](https://github.com/Iammuratc/semiconductorGrowth/blob/master/ss0.png)

![Flow of TMGa](https://github.com/Iammuratc/semiconductorGrowth/blob/master/ss2.png)

Also, you can plot the final semiconductor structure under 'Tools'. The last figure above shows the semiconductor structure, which is a p-type AlN/GaN semiconductor. Besides that, it is possible to export data to excel under 'Excel'.

![Preview of the semiconductor](https://github.com/Iammuratc/semiconductorGrowth/blob/master/ss1.png)

# Installation
I used Python3 for this project.

You could clone the repository as follows:
$ git clone git@github.com:Iammuratc/semiconductorGrowth.git

Run the app by typing
$ python app.py
