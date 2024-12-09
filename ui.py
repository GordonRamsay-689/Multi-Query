

import sys
import termios
import subprocess

def main():
    c_out("hi, my name is michael", isolate=True, color=5)
    c_out("I like veggies", isolate=True, bottom_margin=False)
    c_out("and sake", isolate=False, indent=1, highlight=False, color=34, bottom_margin=True, endline=False)
    c_out("Error!", error=True, separator=True)
    
    c_out("Input: ")
    x = c_in()
    c_out(x)

def c_in():
    ''' (None) -> str

    Gets multiline input from the user. When three newline chars
    or empty lines are detected in sucession the function stops 
    reading input. Will remove the three final empty rows from the 
    string before returning it.

    Note:
    Maximum input size for pasted content ~1000 WITHOUT a newline. (this
    is a terminal limitation and may vary between consoles.) If there is a 
    newline every 1000 chars it will handle at least 9200 pasted chars).
    '''

    string = ''
    c = 0 
    line = ''
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    while True:
        line = sys.stdin.readline()
        string += line

        if line == '\n' or line == '':
            c += 1
            if c > 3:
                break   
        else:
            c = 0

    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    # Adjust for whitespace at end of input, remove it.    
    return string[:-5]

def c_out(text, *, bottom_margin=False, top_margin=False, color=None, endline=True, error=False, focus=False,
          highlight=None, indent=0, isolate=False, separator=False):
    """ (str, *) -> None
    
    Handles console output with various formatting options.
    
    Args:
        (* or /)
        text:           str
        
        (*)
        bottom_margin:  bool
        color:          str (RGB color value) | "0;0;0"
        endline:        bool
        error:          bool
        focus:          bool
        highlight:      str (RGB color value)
        indent:         int (> 0)
        isolate:        bool
        separator:      bool 
        top_margin:     bool
    """

    # SET dependent variables
    if error:
        highlight = 52
    if bottom_margin:
        endline = True
    endchar = '\n' if endline == True else ''

    # MANIPULATE text (ansi escape codes)
    if color:
        text = f"\033[38;5;{color}m{text}" 
    if highlight:
        text = f"\033[48;5;{highlight}m {text}"

    text = f"{text}\033[0m" 

    # POSITION text
    text = ('\t' * indent) + text
    if isolate:
        text = f"\n{text}\n"
    if bottom_margin:
        text = f"{text}\n"
    if top_margin:
        text = f"\n{text}"

    # PRINT text
    print(text, end=endchar)
    if separator:
        print('-' * 50, '\n')
    
    if focus:
        bring_terminal_to_front()


def bring_terminal_to_front():
    ''' AppleScript command, focus terminal window '''
    script = 'tell application "Terminal" to activate'
    subprocess.run(['osascript', '-e', script])

if __name__ == '__main__':
    main()