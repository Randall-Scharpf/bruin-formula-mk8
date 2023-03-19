# constants
# raspberry pi's OS has different-looking fonts than MacOS or Windows
# a scalar applied to the font size of every non-dial widget
SCALE = 1.0  # 0.8 on RP
# a scalar applied to the font size of every dial widget
DIAL_SCALE = 1.0

# helper constants to prevent typos
FONT_CSS = "font-family: Ubuntu;"  # ben's favorite font
WHITE_CSS = "color: rgba(255, 255, 255, 255);"
TRANSPARENT_CSS = "background-color : rgba(0, 0, 0, 0);"


def scaled_css_size(px):
    return "font-size:" + str(int(px * SCALE)) + "px;"


def scaled_dial_size(size):
    return size * DIAL_SCALE


def scale_size_for_all(main_win):
    main_win.CANStatusLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(25))
    main_win.CANConnectionLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(25))
    main_win.TimeLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(25))
    main_win.LogLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(25))
    main_win.AFRLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(35))
    main_win.RPMLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(40))
    main_win.VelocityLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(35))
    main_win.FPSLabel.setStyleSheet(FONT_CSS + WHITE_CSS + TRANSPARENT_CSS + scaled_css_size(25))
