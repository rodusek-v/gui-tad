def translate_children(widget, value_x, value_y):
    for child in widget.children():
        geometry = child.geometry()
        geometry.translate(value_x, value_y)
        child.setGeometry(geometry)