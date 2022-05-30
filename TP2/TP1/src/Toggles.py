# Toggles H(s) data input showing state.
def toggle_transfer_data(widg):
    # widg.clear()
    if widg.showing_Hs:
        widg.transfer_data.hide()
        widg.clear_transfer()
        widg.signal_response_frame.hide()
        widg.signal_response_showing = False
    else:
        widg.transfer_data.show()
        if widg.showing_LT: widg.toggle_spice_data()
        if widg.showing_CSV: widg.toggle_csv_data()
    widg.showing_Hs = not widg.showing_Hs


# Toggles LTSpice data input showing state.
def toggle_spice_data(widg):
    if widg.showing_LT:
        widg.InputSpice.hide()
        widg.clear_spice()
    else:
        if widg.showing_Hs: widg.toggle_transfer_data()
        if widg.showing_CSV: widg.toggle_csv_data()
        widg.InputSpice.show()
    widg.showing_LT = not widg.showing_LT


# toggles CSV data input showing state.
def toggle_csv_data(widg):
    if widg.showing_CSV:
        widg.CSV_input.hide()
        widg.clear_csv()
    else:
        widg.CSV_input.show()
        if widg.showing_Hs: widg.toggle_transfer_data()
        if widg.showing_LT: widg.toggle_spice_data()
    widg.showing_CSV = not widg.showing_CSV

def newPlot(widg):
    if widg.new_plot_button.text() == "New Plot":
        widg.new_plot_button.setText("Close")
        widg.data_input_frame.show()
    else:
        widg.new_plot_button.setText("New Plot")
        widg.data_input_frame.hide()
        widg.signal_response_frame.hide()
        widg.signal_response_showing = False


def toggle_signal_resp(widg):
    if widg.signal_response_showing:
        widg.signal_response_frame.hide()
        widg.clear()
    else:
        widg.signal_response_frame.show()
    widg.signal_response_showing = not widg.signal_response_showing

def toggle_freq_duty(widg):
    if widg.signal_type_box.currentText() in ('Sine','Square'): widg.fr_frame.show()
    else: widg.fr_frame.hide()

    if widg.signal_type_box.currentText() == 'Square': widg.duty_cycle.show()
    else: widg.duty_cycle.hide()