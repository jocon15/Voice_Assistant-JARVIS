###############################################################################
#   Copyright (c) 2022 Jason O'Connell.  All rights reserved.
#
#   This code is licensed under the MIT License.  See the FindCUDA.cmake script
#   for the text of the license.

# The MIT License
#
# License for the specific language governing rights and limitations under
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
###############################################################################

import time
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from jarvis.jarvis_coms import *
from sort_commands.SortComands import *


def greeting(needs_greeting):
    # good morning or good afternoon
    if needs_greeting:
        hour = int(datetime.now().strftime('%H'))
        if hour >= 20:
            speak("Good evening sir, if you need anything, I'll be listening")
        elif 11 < hour < 20:
            speak("Good afternoon sir, if you need anything, I'll be listening.")
        else:
            speak("Good morning sir, if you need anything, I'll be listening.")
        # we just greeted so we don't need to greet anymore
        return False
    else:
        speak('Refresh complete.')
        return False


def main():
    #   -refresh data, exit, sell positions
    # for now, just display account information
    MasterConfig.cwd = os.getcwd()
    main_flag = True
    listen_flag = True
    needs_greeting = True
    # we have to wait for the
    needs_greeting = greeting(needs_greeting)
    while listen_flag:
        # jarvis will now listen infinitely for instructions
        command = listen().lower()
        if command != 'Exception':
            # user said something audible
            returned = sort_verbal_command(command)
            # if a value was returned from the sort, break
            if returned:
                break


if __name__ == '__main__':
    main()
