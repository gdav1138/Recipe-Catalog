import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5678")
socketTwo = context.socket(zmq.REP)
socketTwo.bind("tcp://*:8765")

while True:
    save_path = socket.recv()
    save_path = save_path.decode("utf-8")
    save_path = save_path + ".txt"
    notes = socketTwo.recv()
    notes = notes.decode("utf-8")
    with open(save_path, "a") as recipeFile:
        recipeFile.write('\n' + "Notes:" + '\n' + notes)