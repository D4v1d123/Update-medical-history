import os 
import json
import PyPDF2

# Get file id via file name. 
def get_file_id(file_path):
    file_name = file_path.split("\\")[-1]
    return int(file_name.split()[0])

# Sort file paths in a directory in ascending order.
def sort_dir_ascending(dir_path):
    files = os.listdir(dir_path)
    sorted_files = sorted(files, key=get_file_id)
    paths_sorted_files = [os.path.join(dir_path, file) for file in sorted_files]
    
    return paths_sorted_files

# Extract the id number, type id and study name of the patient result. 
def get_result_info(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        content = reader.pages[0]
        text = content.extract_text()
        words = text.split()

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
    
def create_json(sorted_file_paths):  
    data = []

    for file_path in sorted_file_paths:
        id, id_type, study_name, patients_name, age = get_result_info(file_path)

        if(age == "NO"):
            print(f"Document \"{file_path}\" has no age.")
            break

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
dir_path = r"C:\Users\RADIOLOGIA\Documents\David\Salud.SIS\SUBIR ARCHIVOS"

sorted_file_paths = sort_dir_ascending(dir_path)
data = create_json(sorted_file_paths)