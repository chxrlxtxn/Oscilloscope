In order to run this program please make sure you have Python < 3.10. Once that is installed run the following commands in your command line.
1. pip install PyQt5
2. pip install numpy
3. pip install pyserial
4. pip install pyqtgraph

After installing the necessary libraries please program your Arduino to run the given firmware. Then please run main.py located in the public folder.

ADDITIONALLY - If you would like auto scaling for the Y axis please right click on the graph and click Y-axis and click Auto scaling.

!!! IF YOU FACE ERRORS !!!
If your program doesn't run properly stating that it can't find certain files check your terminal run path to ensure its running from outside the public filepath.
If that doesn't work please go to "main.py", "rolling/settings.py", "triggering/settings.py", and "xy mode/settings.py" and scroll down to the filepaths that include "public/" and remove just the "public/" from each filepath.

