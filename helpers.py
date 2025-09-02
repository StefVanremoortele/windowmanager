import pygetwindow as gw

def click_window(window, position, cb, double_click=False):
    window.activate()
    base_x, base_y = window.left, window.top
    pos = (window.width / 100) * position[0], (window.width / 100) * position[1]
    cb(base_x + pos[0], base_y + pos[1])
    if double_click:
        cb(base_x + pos[0], base_y + pos[1])