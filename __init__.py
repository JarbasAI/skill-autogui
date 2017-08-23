# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from os.path import dirname

import pyautogui
import platform
import cv2
from num2words import num2words
#from mycroft.skills.displayservice import DisplayService

__author__ = 'eClarity'

LOGGER = getLogger(__name__)


class AutoguiSkill(MycroftSkill):
    def __init__(self):
        super(AutoguiSkill, self).__init__(name="AutoguiSkill")
        self.grid = False

    def initialize(self):
        #self.display_service = DisplayService(self.emitter)
        type_intent = IntentBuilder("TypeIntent"). \
            require("TypeKeyword").require("Text").build()
        self.register_intent(type_intent, self.handle_type_intent)

        mouse_absolute_intent = IntentBuilder("MouseAbsoluteIntent"). \
            require("MouseAbsoluteKeyword").require("X").require("Y").build()
        self.register_intent(mouse_absolute_intent,
                             self.handle_mouse_absolute_intent)

        mouse_scroll_down_intent = IntentBuilder("MouseScrollDownIntent"). \
            require("MouseScrollDownKeyword").require("Scroll").build()
        self.register_intent(mouse_scroll_down_intent,
                             self.handle_mouse_scroll_down_intent)

        mouse_scroll_up_intent = IntentBuilder("MouseScrollUpIntent"). \
            require("MouseScrollUpKeyword").require("Scroll").build()
        self.register_intent(mouse_scroll_up_intent,
                             self.handle_mouse_scroll_up_intent)

        mouse_scroll_right_intent = IntentBuilder("MouseScrollRightIntent"). \
            require("MouseScrollRightKeyword").require("Scroll").build()
        self.register_intent(mouse_scroll_right_intent,
                             self.handle_mouse_scroll_right_intent)

        screen_res_intent = IntentBuilder("ScreenResIntent"). \
            require("ScreenResKeyword").build()
        self.register_intent(screen_res_intent, self.handle_screen_res_intent)

        press_key_intent = IntentBuilder("PressKeyIntent"). \
            require("PressKeyKeyword").require("Key").build()
        self.register_intent(press_key_intent, self.handle_press_key_intent)

        hold_key_intent = IntentBuilder("HoldKeyIntent"). \
            require("HoldKeyKeyword").require("Key").build()
        self.register_intent(hold_key_intent, self.handle_hold_key_intent)

        release_key_intent = IntentBuilder("ReleaseKeyIntent"). \
            require("ReleaseKeyKeyword").require("Key").build()
        self.register_intent(release_key_intent, self.handle_release_key_intent)

    def get_grid(self, path=None):
        if path is None:
            path = dirname(__file__) + "/screenshot.jpg"
        pyautogui.screenshot(path)
        img = cv2.imread(path)
        h, w = img.shape[:2]
        x = w / 3
        y = h / 3
        font = cv2.FONT_HERSHEY_SIMPLEX
        # draw vertical lines
        i = 0
        while i < 4:
            cv2.line(img, (x * i, 0), (x * i, h), (0, 0, 255), 5)
            i += 1
        # draw horizontal lines
        i = 0
        while i < 4:
            cv2.line(img, (0, y * i), (w, y * i), (0, 0, 255), 5)
            i += 1

        # draw nums
        i = 0
        o = 0
        for num in range(1, 10):
            cv2.putText(img, str(num), (x / 2 + x * i, y / 2 + y * o), font,
                        1, (0, 0, 255), 2)
            i += 1
            if i % 3 == 0:
                o += 1
                i = 0
        # save num coordinates
        self.boundings = []
        for o in range(0, 3):
            for i in range(0, 3):
                self.boundings.append([x * (i + o * 3), o * y, x, y])
        cv2.imwrite(path, img)
        return img, path

    def handle_activate_grid_intent(self, message):
        self.speak("Grid activated")
        self.grid = True
        img, path = self.get_grid()
        cv2.imshow("grid", img)
        #self.display_service.display([path])

    def handle_deactivate_grid_intent(self, message):
        self.speak("Grid deactivated")
        self.grid = False
        #self.display_service.close()
        cv2.destroyWindow("grid")

    def handle_mouse_position_intent(self, message):
        self.speak("mouse position is TODO")
	
    def handle_mouse_click_intent(self, message):
        self.speak("clicking mouse")
        pyautogui.click()

    def handle_type_intent(self, message):
        self.speak_dialog("typing")
        text = message.data.get('Text')
        pyautogui.typewrite(text, interval=0.05)

    def handle_mouse_absolute_intent(self, message):
        self.speak('moving mouse now')
        X = message.data.get('X')
        Y = message.data.get('Y')
        # pyautogui.moveTo(X, Y)

    def handle_mouse_scroll_down_intent(self, message):
        self.speak('scrolling down now')
        scroll = message.data.get('Scroll')
        scroll_down = int(scroll) * -1
        pyautogui.scroll(scroll_down)

    def handle_mouse_scroll_up_intent(self, message):
        self.speak('scrolling up now')
        scroll = message.data.get('Scroll')
        scroll_up = int(scroll)
        pyautogui.scroll(scroll_up)

    def handle_mouse_scroll_right_intent(self, message):
        if platform.system().lower().startswith('lin'):
            self.speak('scrolling right now')
            scroll = message.data.get('Scroll')
            scroll_right = int(scroll)
            pyautogui.hscroll(scroll_right)
        else:
            self.speak(
                'Sorry, I cannot scroll right on your current operating system')

    def handle_screen_res_intent(self, message):
        screen = pyautogui.size()
        resx = screen[0]
        resy = screen[1]
        responsex = num2words(resx)
        responsey = num2words(resy)
        self.speak(
            "Your screen resolution is %s by %s" % (responsex, responsey))

    def handle_press_key_intent(self, message):
        key = message.data.get('Key')
        self.speak("Pressing %s" % key)
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)

    def handle_hold_key_intent(self, message):
        key = message.data.get('Key')
        self.speak("Holding down %s key" % key)
        pyautogui.keyDown(key)

    def handle_release_key_intent(self, message):
        key = message.data.get('Key')
        self.speak("Releasing %s key" % key)
        pyautogui.keyUp(key)

    def stop(self):
        pass


def create_skill():
    return AutoguiSkill()
