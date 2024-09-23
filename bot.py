import pyautogui
import time
import keyboard


def buy_stocks(stock, short, amountOfShares):
    time.sleep(3)
    keyboard.press_and_release('alt + tab')
    time.sleep(3)
    pyautogui.moveTo( 226,450)
    pyautogui.click(226,450)
    time.sleep(0.5)
    keyboard.write(stock)
    time.sleep(0.5)
    keyboard.press_and_release('enter')
    time.sleep(0.5)
    pyautogui.moveTo( 226,550)
    pyautogui.click(226,550)
    time.sleep(0.5)
    pyautogui.moveTo( 500,850)
    pyautogui.click(500,850)
    if(short == True):
        time.sleep(0.5)
        pyautogui.moveTo( 550,340)
        pyautogui.click(550,340)
    if(short == False):
        time.sleep(0.5)
        pyautogui.moveTo(405,340)
        pyautogui.click(405,340)
    
    time.sleep(0.5)
    pyautogui.moveTo(771,500)
    pyautogui.click(771,500)
    time.sleep(0.5)
    keyboard.press_and_release('delete')
    time.sleep(0.5)
    keyboard.write(amountOfShares)
    time.sleep(0.5)
    pyautogui.moveTo(771,500)
    pyautogui.click(862,840)


def clear():
    time.sleep(0.5)
    pyautogui.moveTo( 913,231)
    pyautogui.click(913,231)
    time.sleep(1)
    pyautogui.moveTo( 767,460)
    pyautogui.click(767,460)

    





#buy_stocks("TSLA", True, "1")
#clear()