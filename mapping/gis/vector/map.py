import mapnik
import cv2


map = mapnik.Map(800, 600)
map.background = mapnik.Color('white')
style = mapnik.Style()
rule = mapnik.Rule()
polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('white'))
symbolizer = mapnik.PointSymbolizer()
rule.symbols.append(polygon_symbolizer)
rule.symbols.append(symbolizer)
line_symbolizer = mapnik.LineSymbolizer(
mapnik.Color('rgb(50%,50%,50%)'), 0.1)
rule.symbols.append(line_symbolizer)
style.rules.append(rule)
map.append_style('My Style', style)
reply="yes"
while reply=="yes":
    filePath = str(input("file path"))
    print "Entered File Path is %s" % filePath
    data = mapnik.Shapefile(file=filePath)
    layerName=str(input("Enter Name of Layer"))
    layer = mapnik.Layer(layerName)
    layer.datasource = data
    layer.styles.append('My Style')
    map.layers.append(layer)
    reply = str(input("Add More Layer"))
map.zoom_all()
output_filePath = str(input("Enter path to save map"))
print "Entered File Path is %s" % output_filePath
mapnik.render_to_file(map,output_filePath,'png')
image = cv2.imread(output_filePath)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

def display_map(image_file):
    image = cv2.imread(image_file)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def create_map(style_file, output_image, size=(800, 600)):
    map = mapnik.Map(*size)
    mapnik.load_map(map, style_file)
    map.zoom_all()
    mapnik.render_to_file(map, output_image)