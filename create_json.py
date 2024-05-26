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
        start = words.index("ESTUDIO") + 2
        end = words.index("HALLAZGOS:")
        
        # Extract the study name between the words "ESTUDIO" y "HALLAZGOS:" 
        study_name = ""
        for study_words in range(start, end):
            study_name += f"{words[study_words]} "
        
        return (words[id_type_index + 1], words[id_type_index], study_name)  # id 
        # number, type id, study name.
    
def create_json(sorted_file_paths):  
    data = []

    for file_path in sorted_file_paths:
        id, id_type, study_name = get_result_info(file_path)
        data.append({
             "id" : id,
             "id_type" : id_type,
             "study_name" : study_name,
             "file_path": file_path
        })  
        
    return data

# File directory.
dir_path = r"D:\Users\User\Documents\BACKUP 04-03-2024\David\Salud.SIS\SUBIR\ARCHIVOS"

sorted_file_paths = sort_dir_ascending(dir_path)
data = create_json(sorted_file_paths)
