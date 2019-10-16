# Project name: MOVPE input analyzer

# Description
## What is metal organic vapor phase epitaxy (MOVPE)?
Semiconductors form the basis of modern electronic devices such as transistors, diodes and lasers. For example, nitride semiconductors (e.g. GaN/AlGaN, InN) are widely used in optoelectronic devices such as LEDs and detectors. The production of nitride semiconductors with desired properties (resistance, sensitivity to light etc.) requires a complex and diligent process. One of the production methods for nitride semiconductors is metal organic vapor phase epitaxy (MOVPE), where epitaxy describes an ordered crystalline growth. This method employs each element (Ga, N, In etc.) in the gas form to build the semiconductor structure. However, the production of group III elements (Ga, In, Al) as gases is a difficult task due to physical reasons, that's why, these elements are bound to metal organic compounds (e.g. Trimethyl-gallium, TMGa). Eventually, the MOVPE method produces the desired nitride semiconductor structure by the reaction of such compounds at various amounts and time intervals. (See https://en.wikipedia.org/wiki/Metalorganic_vapour-phase_epitaxy for details.)

## What is MOVPE input analyzer?
The MOVPE method consists of various gas sources, valves to control the flow of these gases and a reactor in which the gases react to build the semiconductor. In that manner, the input of the MOVPE method simply gives the recipe of the semiconductor, which describes the amount of each gas at certain time intervals. The MOVPE input analyzer provides a user friendly handling for these input files, see an example input file in the folder 'inputs'.


# Installation
## Prerequisites
```bash
Python3
```

You can clone the repository as follows:
```bash
git clone git@github.com:Iammuratc/semiconductorGrowth.git
```
Run the application by typing
```bash
python app.py
```
## Usage
You can see a screenshot from the application below. The 3rd and 4rd columns show the gases and valves used in the recipe, and you can plot the flows of each gas and valve over time by using the buttons above. There are two different valves for each gas, called *run* and *line* valves. Depending on the position of these valves (0 close, 1 open), the semiconductor growth occurs in the reactor. The 1st column shows the flow of gas when the corresponding *run* valve is open. If both valves (*line* and *run*) are open, the semiconductor grows through the gases listed in the 2nd column. Finally, the reactor properties (temperature, pressure etc.) are listed in the 5th column. You can plot each gas flow in every column, where the y-axis represents the flow rate (ccpm) and the x-axis the time (sec).

![Preview of the application](https://github.com/Iammuratc/semiconductorGrowth/blob/master/ss0.png)

![Flow of TMGa](https://github.com/Iammuratc/semiconductorGrowth/blob/master/ss2.png)

Also, you can plot the final semiconductor structure through the 'Tools' tab. The last figure below shows the semiconductor structure, which is a p-type AlN/GaN semiconductor. Besides that, it is possible to export data to an *Excel* file through the 'Excel' tab.

![Preview of the semiconductor](https://github.com/Iammuratc/semiconductorGrowth/blob/master/ss1.png)
