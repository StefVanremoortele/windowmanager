import pygetwindow as gw
import pyautogui
import keyboard
import time


from helpers import click_window
from constants import (
    PRECHECK_FOLD_POSITION_X,
    PRECHECK_FOLD_POSITION_Y,
    TABLE_KEYWORD,
    RELATIVE_POS_BUTTON_CHECK_OR_CALL,
    RELATIVE_POS_BUTTON_RAISE,
    RELATIVE_POS_CHECKBOX_FOLD,
    INPUT_BET_SIZE_AMOUNT,
    HK_call,
    HK_RELANCE,
    HK_check_or_fold,
    HK_fold_all,
    HK_cycle_next,
    HK_cycle_prev,
    HK_toggle,
)

pyautogui.FAILSAFE = False


class Manager:
    tables = []
    windows = []
    current_index = 0
    enabled = True

    def __init__(self):
        self.refresh()
        self.configure_hotkeys()

    def refresh(self):
        self.tables = [w for w in gw.getAllTitles() if TABLE_KEYWORD in w]

        for win in gw.getAllWindows():
            if TABLE_KEYWORD in win.title:
                self.windows.append(win)

        sorted_items = sorted(self.windows, key=lambda item: item.left + item.top)
        self.windows = sorted_items

        self.order_tables()

    def order_tables(self):
        temp_tables = {}
        for title in self.tables:
            window = gw.getWindowsWithTitle(title)[0]
            temp_tables[title] = {
                "left": window.left,
                "top": window.top,
            }

        sorted_items = sorted(
            temp_tables.items(), key=lambda item: item[1]["left"] + item[1]["top"]
        )
        sorted_dict_by_values = dict(sorted_items)
        self.tables = list(sorted_dict_by_values.keys())

    def click_button(self, x, y):
        pyautogui.click(x, y)
        # window = gw.get(title)[0]

    def activate_table(self, index):
        print("Should activate")
        if not self.windows:
            return

        window = self.windows[index]
        window.activate()

        pyautogui.moveTo(
            window.left + (window.width / 2), window.top + (window.height / 2)
        )

    def select_amount(self):
        click_window(
            self.windows[self.current_index],
            INPUT_BET_SIZE_AMOUNT,
            self.click_button,
            True
        )

        pyautogui.moveTo(
            self.windows[self.current_index].left + (self.windows[self.current_index].width / 2), self.windows[self.current_index].top + (self.windows[self.current_index].height / 2)
        )

    def activate_window(self, index):
        window = self.windows[index]
        window.activate()

        pos = (window.width / 100) * INPUT_BET_SIZE_AMOUNT[0], (
            window.height / 100
        ) * INPUT_BET_SIZE_AMOUNT[1]

        pyautogui.moveTo(
            window.left + (window.width / 2), window.top + (window.height / 2)
        )

    def cycle_table(self, direction):
        # refresh_tables()
        if not self.windows:
            return
        self.current_index = (self.current_index + direction) % len(self.windows)
        self.activate_window(self.current_index)

    def test(self):
        # window = gw.getWindowsWithTitle(self.tables[self.current_index])[0]
        # pyautogui.moveTo(
        #     window.left + (window.width / 2), window.top + (window.height / 2)
        # )
        # keyboard.wait()
        pass

    def call(self):
        click_window(
            self.windows[self.current_index],
            RELATIVE_POS_BUTTON_CHECK_OR_CALL,
            self.click_button,
        )

    def fold(self):
        window = gw.getWindowsWithTitle(self.tables[self.current_index])[0]
        window.activate()
        base_x, base_y = window.left, window.top
        pos = (window.width / 100) * INPUT_BET_SIZE_AMOUNT[0], (
            window.width / 100
        ) * INPUT_BET_SIZE_AMOUNT[1]

        self.click_button(base_x + pos[0], base_y + pos[1])

    def check_or_fold(self):
        click_window(
            self.windows[self.current_index],
            RELATIVE_POS_CHECKBOX_FOLD,
            self.click_button,
        )

    def relance(self):
        click_window(
            self.windows[self.current_index],
            RELATIVE_POS_BUTTON_RAISE,
            self.click_button,
        )

    def check_fold(self):
        click_window(
            self.windows[self.current_index],
            RELATIVE_POS_CHECKBOX_FOLD,
            self.click_button,
        )

    def fold_all(self):
        for window in self.windows:
            window.activate()
            base_x, base_y = window.left, window.top
            pos = (window.width / 100) * RELATIVE_POS_CHECKBOX_FOLD[0], (
                window.width / 100
            ) * RELATIVE_POS_CHECKBOX_FOLD[1]
            self.click_button(
                base_x + pos[0],
                base_y + pos[1],
            )

    def toggle(self):
        self.enabled = not self.enabled
        if not self.enabled:
            keyboard.clear_all_hotkeys()
            keyboard.add_hotkey("shift+p", lambda: self.toggle())
        else:
            keyboard.clear_hotkey("shift+p")
            self.configure_hotkeys()

        print(f"Hotkeys {'enabled' if self.enabled else 'disabled'}")

    def configure_hotkeys(self):
        keyboard.add_hotkey(HK_toggle, lambda: self.toggle())
        keyboard.add_hotkey(HK_cycle_next, lambda: self.cycle_table(1))
        keyboard.add_hotkey(HK_cycle_prev, lambda: self.cycle_table(-1))
        keyboard.add_hotkey(HK_call, lambda: self.call())
        keyboard.add_hotkey(HK_check_or_fold, lambda: self.check_or_fold())
        keyboard.add_hotkey(HK_fold_all, lambda: self.fold_all())
        keyboard.add_hotkey('s', lambda: self.select_amount())
        keyboard.add_hotkey(HK_RELANCE, lambda: self.relance())
        keyboard.add_hotkey("t", lambda: self.test())
        # keyboard.add_hotkey('t', on_hotkey, suppress=False, trigger_on_release=False)
