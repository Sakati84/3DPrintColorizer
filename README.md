
![](Media/Logo.jpg)  

**3D Print Colorizer** is a combination of 3D printed parts and a [Cura](https://ultimaker.com/de/software/ultimaker-cura) plugin which allows anyone with an Ender 3 or BLTouch-compatible printer (no CoreXY for now) to produce multi colored models. Have a look at some results:

![](Media/Models.jpg)  

## Release Notes
- **2021-08-06** Fixed issue with some T-Commands still being in the G-Code as reported by Teaching Tech.
- **2021-08-05** Added big compatibility update. Added parts to mount to nearly any BLTouch-compatible Printer (no CoreXY for now).

## How it works
3D Print Colorizer uses Sharpie or Sharpie-like permanent markers to directly paint on the layers of a 3D print. After a layer is finished printing normally a pen holder, which is mounted to the print head, is used to fetch pens from a special pen rack mounted to the top part of the printer. Normal printing and painting is used alternately to produce a final colored model.

To coordinate the process a special [Cura](https://ultimaker.com/de/software/ultimaker-cura) plugin is used to  add the painting G-Code. After installing the plugin you need to enter some calibration values and afterwards models sliced for an Multi Extrusion printer can be printed on an Ender 3 with full color support.

![](Media/Animation.gif)  
*[YouTube link](https://youtu.be/2vPkmsyEDaQ)*

## Installation
Detailed installation instruction are given in the [Wiki](https://github.com/Sakati84/3DPrintColorizer/wiki/1-Hardware-Setup). Please follow each step to complete the installation and get ready for mutli color printing.

[1. Hardware Setup](https://github.com/Sakati84/3DPrintColorizer/wiki/1-Hardware-Setup)

[2. Materials needed](https://github.com/Sakati84/3DPrintColorizer/wiki/2-Materials)

[3. Calibration](https://github.com/Sakati84/3DPrintColorizer/wiki/3-Calibration)

[4. Software Setup](https://github.com/Sakati84/3DPrintColorizer/wiki/4-Software-Setup)

[5. Printing](https://github.com/Sakati84/3DPrintColorizer/wiki/5-Printing)

---
If you want you can:

<a href="https://www.buymeacoffee.com/sakati" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="150" height="40" ></a>