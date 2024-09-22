# Update of medical history 🩻
This program automates the process of validating information contained in PDF files by comparing it with the data from the Salud.SIS platform, then updates the patient clinical history by uploading documents with the correct data.

## 🔬 How does it work?
1. Sort PDF file paths for processing.
2. Extract information from the PDFs, such as the user's identification number and type, the name of the study, and patient data (name and age), storing it in a JSON file.
3. Using image recognition techniques and predefined coordinates, the program verifies the data with the web platform, if the information matches, it uploads the corresponding file to the platform.

## 💻 Installation
1. Installs version 3.12 of Python.
2. Run the following command in the terminal (CMD) to clone the project:
~~~
git clone https://github.com/D4v1d123/Update-medical-history.git
~~~
3. Run the following command in the terminal (CMD) to install the project dependencies:
~~~
python3 -m pip install -r requirements.txt
~~~
4. Configure your favorite code editor to run Python, or use an IDE such as PyCharm or Spyder.

## 🔗 Dependencies
- Python 3.12+
- opencv-python 4.10.0.84 
- PyAutoGUI 0.9.54   
- pyperclip 1.9.0  
- keyboard 0.13.5
- PyPDF2 3.0.1
