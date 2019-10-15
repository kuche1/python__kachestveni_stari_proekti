import pygame
import time
import os
import random
from threading import Thread

pygame.mixer.init()

class music():
    volume = 1
    autoPlay = False
    reloadingSongs = False
    playedSongs = []
    allSongs = []
    
    def changeVolume(self, sKolko):
        self.volume += sKolko
        if self.volume < 0:
            self.volume = 0
        elif self.volume > 1:
            self.volume = 1
        self.currentSong.set_volume(self.volume)
        print('volume = %s' %(self.volume))
    def changeAutoPlay(self):
        if self.autoPlay:
            self.autoPlay = False
        else:
            self.autoPlay = True
        print('autoPlay = %s' %(self.autoPlay))
    
    def reloadSongs(self):
        self.reloadingSongs = True
        print('=====RELOADING_SONGS=====')
        self.allSongs = []
        self.playedSongs = []
        for (folderName, nz, files) in os.walk('songs'):
            for file in files:
                self.addSong(file)
            break
        print('%s songs loaded' %(len(self.allSongs)))
        print('=====DONE=====')
        self.reloadingSongs = False
    def addSong(self, fileName):
        try:
            self.allSongs.append(pygame.mixer.Sound(os.path.join('songs', fileName)))
        except pygame.error:
            print('unable to load song: %s' %(fileName))
    def playRandomSong(self):
        while True:
            choosenSong = random.randrange(0, len(self.allSongs))
            if choosenSong not in self.playedSongs:
                break
        self.playedSongs.append(choosenSong)
        self.playSong(self.allSongs[choosenSong])
        if len(self.playedSongs) == len(self.allSongs):
            self.changeAutoPlay()
            self.reloadSongs()
    def playSong(self, song):
        if self.reloadingSongs:
            print('You cant play new song while the song list is refreshing')
        else:
            print('Playing song')
            pygame.mixer.stop()
            self.currentSong = song
            self.currentSong.set_volume(self.volume)
            self.currentSong.play()
        
music = music()

music.reloadSongs()

def mainThread():
    while True:
        if music.autoPlay:
            if not pygame.mixer.get_busy():
                music.playRandomSong()
        time.sleep(5)
Thread(target=mainThread).start()



from pyHook import HookManager
from win32gui import PumpMessages, PostQuitMessage
import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))



class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()


    def on_keyboard_event(self, event):
        try:
            key = event.KeyID
            #print(key)
            if key == 103:#7
                print('Playing new random song')
                music.playRandomSong()
            elif key==104:#8
                music.changeAutoPlay()
            elif key == 105:#9
                print("Replaying current song...")
                music.playSong(music.currentSong)
            elif key == 97:#1
                print('Paused')
                pygame.mixer.pause()
            elif key == 98:#2
                print('Unpaused')
                pygame.mixer.unpause()
            elif key == 109: #-
                music.changeVolume(-0.1)
            elif key == 107: #+
                music.changeVolume(0.1)
            elif key == 110:#.
                music.reloadSongs()
        except:
            raise
        #finally:
        #    return True
        return True

    def shutdown(self):
        PostQuitMessage(0)
        self.hm.UnhookKeyboard()


watcher = Keystroke_Watcher()
PumpMessages()


