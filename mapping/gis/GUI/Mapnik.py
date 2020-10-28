import mapnik


def polygon_map():
    m = mapnik.Map(600, 300)  # create a map with a given width and height in pixels
    # note: m.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    # the 'map.srs' is the target projection of the map and can be whatever you wish
    m.background = mapnik.Color('steelblue')  # set background colour to 'steelblue'.
    s = mapnik.Style()  # style object to hold rules
    r = mapnik.Rule()  # rule object to hold symbolizers
    # to fill a polygon we create a PolygonSymbolizer
    polygon_symbolizer = mapnik.PolygonSymbolizer()
    polygon_symbolizer.fill = mapnik.Color('#f2eff9')
    r.symbols.append(polygon_symbolizer)  # add the symbolizer to the rule object
    # to add outlines to a polygon we create a LineSymbolizer
    sym = mapnik.PointSymbolizer()
    # args are file, type, height, width
    sym.allow_overlap = True
    sym.opacity = .5
    r.symbols.append(sym)
    '''line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
    line_symbolizer.stroke_width = 0.1
    r.symbols.append(line_symbolizer)'''# add the symbolizer to the rule object
    s.rules.append(r)  # now add the rule to the style and we're done
    m.append_style('My Style', s)  # Styles are given names only as they are applied to the map
    ds = mapnik.Shapefile(file='I:\Data\shashankdata\LSMDATASET\INVENTORY\INVENTORY.shp')
    layer = mapnik.Layer('Petrolling Party')  # new layer called 'world' (we could name it anything)
    # note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    layer.datasource = ds
    layer.styles.append('My Style')
    m.layers.append(layer)
    # Write the data to a png image called world.png in the current directory
    mapnik.render_to_file(m, 'C:\Users\Hp\Desktop\pol\sha.png', 'png')

    # Exit the Python interpreter
    exit()  # or ctrl-d
    

polygon_map()