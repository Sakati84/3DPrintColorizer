import re #To perform the search and replace.

from ..Script import Script


class PenColorizer(Script):
    """Performs a search-and-replace on all g-code.
    Due to technical limitations, the search can't cross the border between
    layers.
    """

    def getSettingDataString(self):
        return """{
            "name": "PenColorizer",
            "key": "PenColorizer",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "PenXOffset":
                {
                    "label": "Pen X Offset",
                    "description": "Offset of your pen in X direction",
                    "type": "float",
                    "default_value": 36.1
                },
                "PenYOffset":
                {
                    "label": "Pen Y Offset",
                    "description": "Offset of your pen in Y direction",
                    "type": "float",
                    "default_value": 45.8
                },
                "PenZOffset":
                {
                    "label": "Pen Z Offset",
                    "description": "Offset of your pen in Z direction",
                    "type": "float",
                    "default_value": 3.2
                },
                "FirstPenXPosition":
                {
                    "label": "First Pen X Position",
                    "description": "X position for holding the first pen in the pen rack",
                    "type": "float",
                    "default_value": 28.0
                },
                "FirstPenYPosition":
                {
                    "label": "First Pen Z Position",
                    "description": "Z position for holding the first pen in the pen rack",
                    "type": "float",
                    "default_value": 238.0
                }
            }
        }"""

    def getPen(self, pen):    
        penside = pen % 2
        penoffset = float(int(pen / 2)) * 68.0
        
        if penside == 0:
            getlines = [";Get pen " + str(pen),
                        "G0 F5000 ; set speed fast",
                        "G0 X" + str(self.penstartx + penoffset) + "Z" + str(self.penstarty - 152.0) + " ;go under pen",
                        "G0 F2000 ; set speed slow",
                        "G0 X" + str(self.penstartx + penoffset) + " Z" + str(self.penstarty) + " ; lift pen",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty) + " ; move pen right",
                        "G0 F5000 ; set speed fast",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty - 152.0) + " ; lower pen"]
        else:
            getlines = [";Get pen " + str(pen),
                        "G0 F5000 ; set speed fast",
                        "G0 X" + str(self.penstartx + 41.0 + penoffset) + "Z" + str(self.penstarty - 152.0) + " ;go under pen",
                        "G0 F2000 ; set speed slow",
                        "G0 X" + str(self.penstartx + 41.0 + penoffset) + " Z" + str(self.penstarty) + " ; lift pen",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty) + " ; move pen right",
                        "G0 F5000 ; set speed fast",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty - 152.0) + " ; lower pen"]
        return getlines
        
    def putPen(self, pen):
        penside = pen % 2
        penoffset = float(int(pen / 2)) * 68.0
        
        if penside == 0:
            putlines = [";put pen " + str(pen),
                        "G0 F5000 ; set speed fast",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty - 152.0) + " ; go under pen",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty) + " ; lift pen",
                        "G0 F2000 ; set speed slow",
                        "G0 X" + str(self.penstartx + penoffset) + " Z" + str(self.penstarty) + " ; move pen left",
                        "G0 X" + str(self.penstartx + penoffset) + " Z" + str(self.penstarty - 152.0) + " ; lower pen",
                        "G0 F5000 ; set speed fast", ""]
        else:
            putlines = [";put pen " + str(pen),
                        "G0 F5000 ; set speed fast",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty - 152.0) + " ; go under pen",
                        "G0 X" + str(self.penstartx + 20.5 + penoffset) + " Z" + str(self.penstarty) + " ; lift pen",
                        "G0 F2000 ; set speed slow",
                        "G0 X" + str(self.penstartx + 41.0 + penoffset) + " Z" + str(self.penstarty) + " ; move pen left",
                        "G0 X" + str(self.penstartx + 41.0 + penoffset) + " Z" + str(self.penstarty - 152.0) + " ; lower pen",
                        "G0 F5000 ; set speed fast", ""]
        return putlines

    def offset(self, gcode, zoffset):
        coord = re.findall(r'[XYZF].?\d+(?:.\d+)?', gcode)
        newgcode = gcode[:2]
        
        F = next((i for i in coord if i.startswith('F')), None)
        if F != None:
            newgcode += " " + "F3600"#F
            
        X = next((i for i in coord if i.startswith('X')), None)
        if X != None:
            newgcode += " X" + "{:0.3f}".format((float(X[1:]) + self.xoffset))
            
        Y = next((i for i in coord if i.startswith('Y')), None)
        if Y != None:
            newgcode += " Y" + "{:0.3f}".format((float(Y[1:]) + self.yoffset))
            
        Z = next((i for i in coord if i.startswith('Z')), None)
        if Z != None:
            newgcode += " Z" + "{:0.3f}".format((float(Z[1:]) + self.zoffset + zoffset))
        
        return newgcode
        
    def lift(self, gcode, zoffset):
        coord = re.findall(r'[XYZF].?\d+(?:.\d+)?', gcode)
        newgcode = gcode[:2]
        
        F = next((i for i in coord if i.startswith('F')), None)
        if F != None:
            newgcode += " " + F
            
        X = next((i for i in coord if i.startswith('X')), None)
        if X != None:
            newgcode += " X" + "{:0.3f}".format((float(X[1:])))
            
        Y = next((i for i in coord if i.startswith('Y')), None)
        if Y != None:
            newgcode += " Y" + "{:0.3f}".format((float(Y[1:])))
            
        Z = next((i for i in coord if i.startswith('Z')), None)
        if Z != None:
            newgcode += " Z" + "{:0.3f}".format((float(Z[1:]) + zoffset))
        
        return newgcode
        
    def getFirstPos(self, lines):
        for line in lines:
            if "G0" in line or "G1" in line:
                coord = re.findall(r'[XYZ].?\d+(?:.\d+)?', line)
                
                X = next((i for i in coord if i.startswith('X')), None)
                Y = next((i for i in coord if i.startswith('Y')), None)
                Z = next((i for i in coord if i.startswith('Z')), None)
                
                if X != None and Y != None and Z != None:
                    return line
                
        return "; nothing found"
    
    def addExplicitZ(self, lines):
        newlines = []

        for line in lines:
            if "G0" in line or "G1" in line:
                newline = line
            
                coord = re.findall(r'[XYZF].?\d+(?:.\d+)?', line)
                Z = next((i for i in coord if i.startswith('Z')), None)
                if Z != None:
                    self.lastZ = float(Z[1:])
                else:
                    newline += " Z" + "{:0.3f}".format(self.lastZ)
                    
                newlines.append(newline)
            else:
                newlines.append(line)
                    
        return newlines
        
    def execute(self, data):
    
        self.penstartx = self.getSettingValueByKey("FirstPenXPosition")# 28.0
        self.penstarty = self.getSettingValueByKey("FirstPenYPosition")#238.0
    
        self.xoffset = self.getSettingValueByKey("PenXOffset")#36.1
        self.yoffset = self.getSettingValueByKey("PenYOffset")#45.3
        self.zoffset = self.getSettingValueByKey("PenZOffset")#3.2
        self.lastZ = 0.2
        layerheight = 0.2
        
        lastlayerx = 100.0
        lastlayery = 100.0
        lastlayerz = 0.3
        
        drawrectract = 5.5
        
        isRetractMove = True
    
        #iterate layers
        curT = 0
        for layer_number, layer in enumerate(data):
            lines = layer.split("\n")
            lines = self.addExplicitZ(lines)
            
            newlines = []
            isLayer = lines[0].startswith(";LAYER")
            
            #get pen & set height
            zheight = layerheight * (layer_number - 1)
            
            #setup drawbuffers
            drawlines = [None] * 8
            for i in range(8):
                drawlines[i] = ["; Draw Layer " + str(i)]
            
            isPrimeTower = False
            primelines = [";moved prime tower"]
            skirtlines = [";duplicated skirt lines"]

            isSkirt = False
            
            linestoskip = 0
            
            zhopOffset = 3.0
            
            wasG0move = False
            
            #iterate lines
            for line in lines:
                if linestoskip > 0:
                    linestoskip -= 1
                    continue
            
                if ";Layer height:" in line:
                    layerheight = float(line[14:])
                    newlines.append(line)
                #type change
                elif ";TYPE:" in line:
                    if ";TYPE:PRIME-TOWER" in line:
                        isPrimeTower = True
                        isSkirt = False
                    elif ";TYPE:SKIRT" in line or ";TYPE:SUPPORT-INTERFACE" in line or ";TYPE:FILL" in line:
                        isSkirt = True
                        isPrimeTower = False
                    else:
                        isSkirt = False
                        isPrimeTower = False
                    
                    newlines.append(line)
            
                #offset G1 codes & remember curZ
                elif "G0" in line or "G1" in line:
                    coord = re.findall(r'[XYZEF].?\d+(?:.\d+)?', line)
                
                    #should we draw?
                    draw = curT >= 0 and isSkirt == False and isPrimeTower == False and (layer_number + curT) % 2 == 0
                
                    #retract move?
                    E = next((i for i in coord if i.startswith('E')), None)
                    if E != None:
                        if float(E[1:]) < 0.0: 
                            isRetractMove = True
                            zhopOffset = 3.0 
                        else:
                            isRetractMove = False
                            zhopOffset = 0.0
                            
                    '''#G0 Move?
                    if "G0" in line:
                        zhopOffset = 3.0
                        
                        if wasG0move == False and draw == True: #we transition to G0 Move
                            drawlines[curT].append(self.offset(line, 0.0))
                    
                        wasG0move = True
                    else:
                        zhopOffset = 0.0 
                        
                        if wasG0move == True and draw == True: #we transition from G0 Move
                            drawlines[curT].append(self.offset(line, 3.0))
                        
                        wasG0move = False'''
                    
                
                    if  draw == True:
                        drawlines[curT].append(self.offset(line, zhopOffset))
                       
                    if isPrimeTower:
                        primelines.append(line)
                    else:
                        newlines.append(line)
                        
                    #remember last pos
                    
                    X = next((i for i in coord if i.startswith('X')), None)
                    if X != None:
                        lastlayerx = float(X[1:])
                        
                    Y = next((i for i in coord if i.startswith('Y')), None)
                    if Y != None:
                        lastlayery = float(Y[1:])
                        
                    Z = next((i for i in coord if i.startswith('Z')), None)
                    if Z != None:
                        lastlayerz = float(Z[1:])
                                            
                #filter out all dual extruder related gcodes but log which extruder should be active right now
                elif line.startswith("T"):
                    curT = int(line[1:]) - 1
                    newlines.append(";" + line)
                
                #filter out extruder heating commands
                elif "M109" in line and isLayer:
                    print("skip")
                elif "M104" in line and isLayer:
                    print("skip") 
                elif "M105" in line and isLayer:
                    print("skip")  
                    
                else:
                    newlines.append(line)

            #move prime tower to layer startswith
            #primelines.append(";end prime tower")
            #if len(primelines) > 3:
            #    newlines[2:2] = primelines
                
            #add drawlines
            if isLayer:# and layer_number % 2 == 0:
                newlines += ["G1 F1500 E-" + str(drawrectract)] #retract before drawing
                
                for i in range(8):
                    if len(drawlines[i]) <= 1:
                        continue
                        
                    drawlines[i][1:1] = [self.lift(self.getFirstPos(drawlines[i]), 3.0) + ";lower pen from above the first spot"] # lower pen from above the first spot
                    drawlines[i][1:1] = self.getPen(i)
                    drawlines[i] += [self.lift(drawlines[i][-1], 3.0) + "; raise pen from the last spot"] # raise pen from the last spot
                    drawlines[i] += self.putPen(i)

                    newlines += drawlines[i]
                
                #prime after drawing
                newlines += ["G0 X" + str(lastlayerx) + " Y" + str(lastlayery) + " Z" + str(lastlayerz + 2.0), 
                    "G0 X" + str(lastlayerx) + " Y" + str(lastlayery) + " Z" + str(lastlayerz) + " ;return to last pos after drawing"]
                newlines += ["G1 F1500 E" + str(drawrectract), ""]

            result = "\n".join(newlines)
            data[layer_number] = result

        return data
