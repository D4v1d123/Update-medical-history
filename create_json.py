import os 
import locale
import shutil
import PyPDF2

# Get file id via file name. 
def get_file_id(file_path):
    file_name = file_path.split("\\")[-1]
    return int(file_name.split()[0])

# Sort file paths in a directory in ascending order.
def sort_dir_ascending(dir_path):
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    files = os.listdir(dir_path)
    sorted_files = sorted(files, key=locale.strxfrm)
    paths_sorted_files = [os.path.join(dir_path, file) for file in sorted_files]
    
    return paths_sorted_files

def move_files(folder, file_path):
    os.makedirs(folder, exist_ok=True)
    shutil.move(file_path, folder)

# Extract the id number, type id and study name of the patient result. 
def get_result_info(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        content = reader.pages[0]
        text = content.extract_text()
        words = text.split()

        try:
            id_type_index = words.index("DOCUMENTO") + 2
            age_index = words.index("EDAD") + 2
            patients_name = ""
            study_name = ""
        
            # Extract the study name between the words "ESTUDIO" y "HALLAZGOS:" 
            start = words.index("ESTUDIO") + 2
            end = words.index("HALLAZGOS:")
    
            for study_words in range(start, end):
                study_name += f"{words[study_words]} "

            # Extract the patients name between the words "NOMBRE" y "DOCUMENTO" 
            start = words.index("NOMBRE") + 2
            end = words.index("DOCUMENTO")
            
            for study_words in range(start, end):
                patients_name += f"{words[study_words]} "

            return (words[id_type_index + 1], words[id_type_index], study_name, patients_name, words[age_index])  # id 
            # number, id type, study name, patients name and age.

        except(ValueError):
            # Move files that can´t extract data
            file.close()
            folder = r"D:\Users\User\Documents\SUBIR MANUEALMENTE"
            move_files(folder, file_path)

            return None

def create_json(sorted_file_paths):  
    data = []

    for file_path in sorted_file_paths:
        patients_info = get_result_info(file_path)
        
        if patients_info == None: 
            continue 
        else: 
            id, id_type, study_name, patients_name, age = patients_info
        
        if(age == "NO"):
            folder = r"D:\Users\User\Documents\Subir manualmente"
            move_files(folder, file_path)

            print(f"Document \"{file_path}\" has no age.")
            continue

        data.append({
             "age" : int(age),
             "id" : id,
             "id_type" : id_type,
             "study_name" : study_name,
             "patients_name" : patients_name,
             "file_path": file_path
        })  
        
    return data

# File directory.
dir_path = r"D:\Users\User\Documents\Archivos PDF"

sorted_file_paths = sort_dir_ascending(dir_path)
data = create_json(sorted_file_paths)