import os
import pyautogui
import pyperclip
from re import findall
from time import sleep
from create_json import data 

# Move the mouse pointer and click.
def moveMouse(y, x):
    pyautogui.click(y, x, interval=0.2)

# Search for an element on the screen by means of an image and return it's position
# in X and Y.  
def search_element(img_path):
    try:
        position = pyautogui.locateOnScreen(img_path, confidence=0.8) 
        return (position.left, position.top)  # y, x.
    except pyautogui.ImageNotFoundException:
        return None

# Wait for an element to be in screen.
def wait_for_element_load(img_path):
    while True:
        if (coordinates := search_element(img_path)) != None:
            sleep(0.2)
            return int(coordinates[0]), int(coordinates[1]) # y, x.
        
        sleep(0.5)

# Check if patient information in PDFs is correct. 
def check_patients_data(name, data):
    age = data[0]["age"]
    id_type = data[0]["id_type"]
    name_in_website = set(findall(r"\w+", name))
    name_in_pdf = set(findall(r"\w+", data[0]["patients_name"]))

    # Check name.
    if len(name_in_pdf.difference(name_in_website)) != 0:
        print("Incorrect name.")
        exit()

    # Check id type with respect to age.
    if (id_type == "RC") and (age >= 0) and (age <= 6):
        pass
    elif (id_type == "TI") and (age >= 7) and (age <= 17):
        pass
    elif (id_type == "CC") and (age >= 18): 
        pass
    else:
        print("Age does not correspond to the id type.")
        exit()
        
sleep(2) 
while data is not None:
    # Wait until the patient consultation website has loaded.  
    wait_for_element_load(r"img\Search window.png")
    sleep(0.3)
 
    # Select the search type.
    moveMouse(445, 295)
    moveMouse(445, 350)

    # Select the id type.
    type_id = data[0]["id_type"]
    moveMouse(445, 360)
    if type_id == "CC":
        moveMouse(445, 410)
    elif type_id == "TI":
        moveMouse(445, 430)
    elif type_id == "RC":
        moveMouse(445, 470)

    # Write patient id.
    moveMouse(1200, 360)
    pyautogui.write(data[0]["id"])

    # Click the search button.
    moveMouse(1505, 405) 
    sleep(1)

    # Check if type id is correct.
    element = search_element(r"img\Data not found.PNG")
    
    i = 0
    while not(element is None):
        moveMouse(920, 530)
        moveMouse(445, 350)

        # Select RC.
        if i == 0:
            moveMouse(445, 470)
            sleep(0.5)
        # Select CC.
        elif i == 1:
            moveMouse(445, 410)
            sleep(0.5) 
        # Select TI.
        elif i == 2:
            moveMouse(445, 430)
            sleep(0.5)
        else:
            exit()
        
        moveMouse(1505, 405) 
        sleep(0.5)
        element =search_element(r"img\Data not found.PNG")
        i += 1
        
    # Click the select patient button.
    wait_for_element_load(r"img\Select patient.PNG") 
    pyautogui.click(1415, 580)

    # Wait until the patient clinic history website has loaded.
    wait_for_element_load(r"img\Document upload window.png")

    # Copy and get patient´s name
    start_x, start_y = 370, 260
    end_x, end_y = 1500, 260

    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.dragTo(end_x, end_y, duration=0.4)
    pyautogui.mouseUp()

    pyautogui.hotkey('ctrl', 'c')
    sleep(0.5)
    patients_name = pyperclip.paste()

    check_patients_data(patients_name, data)

    pyautogui.scroll(-300)
    
    # Click the select file button.
    sleep(0.5)
    y, x = wait_for_element_load(r"img\Select file.PNG")
    moveMouse(y + 55, x + 45)
    pyautogui.click()
    sleep(0.8)

    # Select file in the window.
    moveMouse(750, 130)
    sleep(0.4) 
    pyautogui.doubleClick()
    sleep(1.5)

    # Fill patient information.
    moveMouse(y + 745, x + 170) 
    sleep(0.5)

    pyautogui.typewrite("Diag")
    sleep(0.5)
    pyautogui.press("tab")
    pyautogui.press("tab")

    pyperclip.copy(f"RESULTADO : {data[0]["study_name"]}")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("tab")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("tab")
    pyautogui.hotkey("ctrl", "v")
    
    # Click the register button.
    y, x = search_element(r"img\Register patient.PNG")
    moveMouse(y, x)
    
    # Check if the patient's result has been successfully recorded.
    sleep(1)
    pop_up = search_element(r"img\Successful.PNG")
    
    if pop_up is None:
        exit()
    else:
        # Delete patient's result.
        os.remove(data[0]["file_path"])
        data.pop(0)
        
        # Go to patient consultation website.
        pyautogui.click(50, 90)
        sleep(1.5)