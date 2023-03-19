# Bruin Formula Racing Dashboard
Written by Guo (Jason) Liu 2022-2023<br>
Email liug22@hotmail.com for suggestions
 
### How to set up on Raspberry Pi
1. Connect Raspberry Pi and a screen with resolution around 1280x720 pixels to power supply.
2. Package resource files (if you made any changes to them) with command: pyrcc5 resources.qrc -o resources.py
3. Upload non-resource files (excluding gui/resources, gui/main.ui and resources.qrc) to Raspberry Pi
4. Configure the resolution of Raspberry Pi to be 1280x720
5. Cd to main.py's directory, and run command: python main.py. The dashboard should display.
6. You may have to update constant scalers in globalfonts.py since fonts in Raspberry Pi's OS look different.
7. Set in Raspberry Pi to launch main.py upon booting.
