def clear_spice(widg):
    widg.X_axis_input_spice.clear()
    widg.Y_axis_input_spice.clear()


def clear_csv(widg):
    widg.X_axis_input_csv.clear()
    widg.Y_axis_input_csv.clear()


def clear_transfer(widg):
    widg.numerator_text.clear()
    widg.denom_text.clear()


# Clears plot.
def clear(widg):
    widg.figure.clear()
    widg.axes = widg.figure.add_subplot()
    widg.canvas.draw()
    widg.x_axis.clear()
    widg.y_axis.clear()
    widg.y_phase.clear()