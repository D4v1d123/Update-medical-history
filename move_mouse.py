import os
import pyautogui
import pyperclip
from PIL import Image
from time import sleep
from create_json import data 

# Move the mouse pointer and click.
def moveMouse(y, x):
    pyautogui.click(y, x)
    sleep(0.2)

# Search for an element on the screen by means of an image and return it's position
# in X and Y.  
def search_element(img_path):
    try:
        position = pyautogui.locateOnScreen(img_path) 
        return (position.left, position.top)  # y, x.
    except pyautogui.ImageNotFoundException:
        return None

# Wait for an element to be in screen. 
def wait_for_element_load(img_path):
    while search_element(img_path) == None:
        sleep(0.4)

sleep(3) 
while data is not None:
    # Wait until the patient consultation website has loaded.  
    wait_for_element_load(r"img\Search window.png")
        
    # Select the search type.
    moveMouse(880, 333)
    moveMouse(880, 390)

    # Write patient id.
    moveMouse(1170, 400)
    pyautogui.write(data[0]["id"])

    # Select the id type.
    type_id = data[0]["id_type"]
    moveMouse(880, 400)
    if type_id == "CC":
        moveMouse(880, 455)
    elif type_id == "TI":
        moveMouse(880, 475)
    elif type_id == "RC":
        moveMouse(880, 530)

    # Click the search button.
    moveMouse(1815, 450) 
    sleep(1)

    # Check if type id is correct.
    element = search_element(r"img\Data not found.PNG")
    i = 0

    while not(element is None):
        moveMouse(1095, 655)
        moveMouse(880, 400)

        # Select RC.
        if i == 0:
            moveMouse(880, 525)
            sleep(0.5)
        # Select CC.
        elif i == 1:
            moveMouse(880, 445)
            sleep(0.5) 
        # Select TI.
        elif i == 2:
            moveMouse(880, 470)
            sleep(0.5)
        else:
            exit()
        
        moveMouse(1815, 450)
        sleep(0.5)
        element =search_element(r"img\Data not found.PNG")
        i += 1
        
    # Click the select patient button.
    wait_for_element_load(r"img\Select patient.PNG") 
    pyautogui.click(r"img\Select patient.PNG")

    # Wait until the patient clinic history website has loaded.
    wait_for_element_load(r"img\History patient.PNG")
    pyautogui.click(r"img\Select file.PNG")
    sleep(0.5)

    # Select file in the window.
    moveMouse(955, 140)
    pyautogui.click()
    pyautogui.click()
    sleep(2)
    
    pyautogui.scroll(-200)

    # Fill patient information.
    y, x = search_element("img/Annex type.PNG")
    moveMouse((y + 359), (x + 15)) 
    sleep(0.5)
    
    pyautogui.typewrite("Diag")
    sleep(0.5)
    pyautogui.press("tab")
    pyautogui.press("tab")

    pyperclip.copy(f"RESULTADO : {data[0]["study_name"]}")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("tab")

    pyautogui.hotkey("ctrl", "v")
    
    # Click the register button.
    sleep(3)
    y, x = search_element(r"img\Register patient.PNG")
    moveMouse(y, x - 25)
    
    # Check if the patient's result has been successfully recorded.
    sleep(1)
    pop_up = search_element(r"img\Successful.PNG")
    
    print(pop_up)
    if pop_up is None:
        exit()
    else:
        # Delete patient's result.
        os.remove(data[0]["file_path"])
        data.pop(0)
        
        # Go to patient consultation website.
        pyautogui.click(80, 90)
