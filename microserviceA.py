import time
import os
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:1234")

file_path = socket.recv()
file_path = file_path.decode("utf-8")
check_interval = .2
last_modified_time = None

def read_list_from_file(file_path):
    ingredientDict = {}
    ingredientKey = ''
    measurement = ''
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line.strip()
            for chars in line:
                if chars == '\n':
                    pass
                elif chars.isdigit():
                    ingredientKey = chars
                else:
                    measurement = measurement + chars
            ingredientDict[ingredientKey] = measurement
            measurement = ''
            ingredientKey = ''
        return ingredientDict

def write_list_to_file(file_path, data_list):
    file_name = "Doubled " + os.path.basename(os.path.normpath(file_path))
    save_path = 'C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipe Ingredients'
    directory = os.path.join(save_path, file_name)
    with open(directory, 'w') as file:
        for item in data_list:
            file.write(f"{item}" + f" {data_list[item]}\n")
    socket.send_string(directory)

def process_list_in_place(file_path):
    # Read the list from the file
    data_list = read_list_from_file(file_path)
    new_data_list = {}

    # Compute sums
    for keys in data_list.keys():
        newKey = int(keys) + int(keys)
        new_data_list[str(newKey)] = data_list[keys]

    # Overwrite the file with the processed list
    write_list_to_file(file_path, new_data_list)

while True:
    try:
        # Get the last modified time of the file
        current_modified_time = os.path.getmtime(file_path)

        # Check if the file has been modified since the last check
        if last_modified_time is None or current_modified_time != last_modified_time:
            print(f"Processing file: {file_path}")
            process_list_in_place(file_path)
            last_modified_time = os.path.getmtime(file_path)

        # Wait for the next check
        time.sleep(check_interval)

    except FileNotFoundError:
        print(f"File {file_path} not found. Waiting for the file to be created.")
        time.sleep(check_interval)