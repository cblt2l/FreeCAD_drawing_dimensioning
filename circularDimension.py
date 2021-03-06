
from dimensioning import *
from dimensioning import __dir__ # not imported with * directive
import selectionOverlay, previewDimension
from dimensionSvgConstructor import circularDimensionSVG

dimensioning = DimensioningProcessTracker()

def selectFun(  event, referer, elementXML, elementParms, elementViewObject ):
    x,y = elementParms['x'], elementParms['y']
    dimensioning.point1 = x, y
    debugPrint(2, 'center selected at x=%3.1f y=%3.1f' % (x,y))
    dimensioning.radius = elementParms['r']
    dimensioning.dimScale = 1/elementXML.rootNode().scaling()
    dimensioning.stage = 1
    selectionOverlay.hideSelectionGraphicsItems()
    previewDimension.initializePreview( dimensioning.drawingVars, clickFunPreview, hoverFunPreview )

def clickFunPreview( x, y ):
    if dimensioning.stage == 1:
        dimensioning.point2 = x,y
        debugPrint(2, 'dimension radial direction point set to x=%3.1f y=%3.1f' % (x,y))
        dimensioning.stage = 2
        return None, None
    elif dimensioning.stage == 2:
        dimensioning.point3 = x, y
        debugPrint(2, 'radius dimension tail defining point set to x=%3.1f y=%3.1f' % (x,y))
        dimensioning.stage = 3
        return None, None
    else:
        XML = circularDimensionSVG( dimensioning.point1[0], dimensioning.point1[1], dimensioning.radius,
                                    dimensioning.point2[0], dimensioning.point2[1], 
                                    dimensioning.point3[0], dimensioning.point3[1], 
                                    x, y, dimScale=dimensioning.dimScale)
        return findUnusedObjectName('dim'), XML

def hoverFunPreview( x, y):
    if dimensioning.stage == 1:
        return circularDimensionSVG( dimensioning.point1[0], dimensioning.point1[1], dimensioning.radius, x, y, dimScale=dimensioning.dimScale, **dimensioning.svg_preview_KWs )
    elif dimensioning.stage == 2:
        return circularDimensionSVG( dimensioning.point1[0], dimensioning.point1[1], dimensioning.radius, 
                                     dimensioning.point2[0], dimensioning.point2[1], x, y, dimScale=dimensioning.dimScale, **dimensioning.svg_preview_KWs )
    else: 
        return circularDimensionSVG( dimensioning.point1[0], dimensioning.point1[1], dimensioning.radius, 
                                     dimensioning.point2[0], dimensioning.point2[1], 
                                     dimensioning.point3[0], dimensioning.point3[1], 
                                     x, y, dimScale=dimensioning.dimScale,**dimensioning.svg_preview_KWs )
    

maskPen =      QtGui.QPen( QtGui.QColor(0,255,0,100) )
maskPen.setWidth(2.0)
maskHoverPen = QtGui.QPen( QtGui.QColor(0,255,0,255) )
maskHoverPen.setWidth(2.0)

class circularDimension:
    def Activated(self):
        V = getDrawingPageGUIVars()
        dimensioning.activate(V)
        selectionOverlay.generateSelectionGraphicsItems( 
            [obj for obj in V.page.Group  if not obj.Name.startswith('dim')], 
            selectFun ,
            transform = V.transform,
            sceneToAddTo = V.graphicsScene, 
            doCircles=True, doFittedCircles=True, 
            maskPen=maskPen, 
            maskHoverPen=maskHoverPen, 
            maskBrush = QtGui.QBrush() #clear
            )
    def GetResources(self): 
        return {
            'Pixmap' : os.path.join( __dir__ , 'circularDimension.svg' ) , 
            'MenuText': 'Circular Dimension', 
            'ToolTip': 'Creates a circular dimension'
            } 

FreeCADGui.addCommand('circularDimension', circularDimension())
