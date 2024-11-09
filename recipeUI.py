import tkinter
from tkinter import *
import os
import zmq


LARGE_FONT = ("Verdana", 16)
recipeFolder = os.listdir("C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipes")


class RecipeCatalog(tkinter.Tk):

    def __init__(self, *args, **kwargs):

        tkinter.Tk.__init__(self, *args, **kwargs)
        container = tkinter.Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=TRUE)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (RecipeStartPage, CatalogPage, AddPage, EditPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=NSEW)
        self.show_frame(RecipeStartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def getRecipes(self):
        list_of_recipes = []
        for files in recipeFolder:
            fileName = os.path.splitext(files)[0]
            list_of_recipes.append(fileName)
        return list_of_recipes


class RecipeStartPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="Recipes For You", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        introLabel = Label(self, text="A place to view and store your favorite recipes "
                                      "and their respective ingredients and measurements!")
        introLabel.pack(pady=10, padx=10)

        button1 = Button(self, text="Catalog", command=lambda: controller.show_frame(CatalogPage))
        button1.pack()


class CatalogPage(tkinter.Frame):

    def getRecipe(self):
        i = 1
        listbox = Listbox(self, width=40, height=10)

        for files in os.listdir("C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipes"):
            fileName = os.path.splitext(files)[0]
            listbox.insert(str(i), fileName)
            i += 1
        listbox.pack()

        def deletePrompt():
            top = Toplevel()
            top.geometry("800x200")
            top.title("WARNING")
            warningLabel = Label(top, text="Are you sure you wish to delete this recipe? " 
                                           "Doing so will result in the loss of all data "
                                           "associated with that recipe. Please confirm. ")
            warningLabel.pack()

            def on_cancel():
                listbox.destroy()
                recipeSelect.destroy()
                deleteRecipe.destroy()
                top.destroy()

            def deleteItem():
                for item in listbox.curselection():
                    save_path = 'C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipes/'
                    save_path = save_path + listbox.get(item) + ".txt"
                    os.remove(save_path)
                    listbox.delete(item)
                    listbox.destroy()
                    recipeSelect.destroy()
                    deleteRecipe.destroy()
                    top.destroy()
            deleteButton = Button(top, text="Delete Recipe", command=deleteItem)
            cancelButton = Button(top, text="Cancel", command=on_cancel)
            deleteButton.pack()
            cancelButton.pack()

        def selectedItem():
            top = Toplevel()
            top.geometry("600x400")
            top.title("Recipe App")
            doubleButton = Button(top, text="Double Ingredients", command=lambda: doubler())
            doubleButton.pack(side=TOP)
            notesButton = Button(top, text="Add Notes", command=lambda: notes())
            notesButton.pack(side=TOP)
            timerButton = Button(top, text="Add Timer", command=lambda: timer())
            timerButton.pack(side=TOP)
            text_box = Text(top, height=175, width=125)
            text_box.pack()

            for item in listbox.curselection():
                save_path = 'C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipes/'
                save_path = save_path + listbox.get(item) + ".txt"
                f = open(save_path, "r")
                content = f.read()
                text_box.insert(END, listbox.get(item))
                text_box.insert(END, "\n")
                text_box.insert(END, "\n")
                text_box.insert(END, content)
            recipeTitle = listbox.get(item)
            listbox.delete(0, END)
            listbox.destroy()
            recipeSelect.destroy()
            deleteRecipe.destroy()
            def doubler():
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect("tcp://localhost:1234")

                save_path = 'C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipe Ingredients/'
                save_path = save_path + recipeTitle + ' ingredients.txt'
                socket.send_string(save_path)

                doubledIngredientsFile = socket.recv()
                top = Toplevel()
                top.geometry("600x400")
                top.title("Recipe App")
                doubleButton = Button(top, text="Double Ingredients", command=lambda: doubler())
                doubleButton.pack(side=TOP)
                notesButton = Button(top, text="Add Notes", command=lambda: notes())
                notesButton.pack(side=TOP)
                text_box = Text(top, height=175, width=125)
                text_box.pack()
                f = open(doubledIngredientsFile, "r")
                content = f.read()
                text_box.insert(END, recipeTitle)
                text_box.insert(END, "\n")
                text_box.insert(END, "\n")
                text_box.insert(END, content)

            def notes():
                top.destroy()
                frame = Toplevel()
                frame.title("Recipe Notes")
                frame.geometry("400x200")
                inputNote = Text(frame, height=5, width=20)
                inputNote.pack()

                saveButton = Button(frame, text="Save Note", command=lambda: saveNote())
                saveButton.pack()

                def saveNote():
                    context = zmq.Context()
                    socket = context.socket(zmq.REQ)
                    socketTwo = context.socket(zmq.REQ)
                    socket.connect("tcp://localhost:5678")
                    socketTwo.connect("tcp://localhost:8765")
                    save_path = 'C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipes/'
                    save_path = save_path + recipeTitle
                    socket.send_string(save_path)
                    socketTwo.send_string(inputNote.get(1.0, END))

                    frame.destroy()

            def timer():
                minute = StringVar()
                minute.set("00")

                frame = Toplevel()
                frame.title("Add Time")
                frame.geometry("350x200")
                timeLabel = Label(frame, font=("Arial",18,""), text="Please enter a time in minutes")
                timeLabel.pack(side=TOP)
                timeEntry = Entry(frame, width=3, font=("Arial",18,""), textvariable=minute)
                timeEntry.pack()
                submit = Button(frame, font=("Arial",12,""), text="Submit", command=lambda: submitTime())
                submit.pack()

                def submitTime():
                    context = zmq.Context()
                    socket = context.socket(zmq.REQ)
                    socket.connect("tcp://localhost:1138")
                    socket.send_string(timeEntry.get())
                    frame.destroy()

        recipeSelect = Button(self, text="View Recipe", command=selectedItem)
        deleteRecipe = Button(self, text="Delete Recipe", command=deletePrompt)
        recipeSelect.pack()
        deleteRecipe.pack()

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = Label(self, text="Recipe Home Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        introLabel = Label(self, text="Welcome! To get started, either click on the "
                                      "'Add Recipe' button to add and save a "
                                      "new recipe to the catalog, or click on "
                                      "the 'Get Recipes' button to view the "
                                      "recipes currently available.")
        introLabel.pack(pady=5, padx=5)

        button1 = Button(self, text="Add Recipe", command=lambda: controller.show_frame(AddPage))
        button1.pack()

        button2 = Button(self, text="Get Recipes", command=self.getRecipe)
        button2.pack()


class AddPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="Add a new Recipe", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky=N)
        self.ingList = []
        self.rowTrack = 3
        self.requiredTitle = ""

        requiredTitleText = Label(self, text="Recipe Title")
        requiredTitleText.grid(row=1, column=0)
        self.requiredTitle = Entry(self)
        self.requiredTitle.grid(row=1, column=1)

        addButton = Button(self, text="Add ingredient", command=lambda: self.addIngredient())
        addButton.grid(row=2, column=1)

        saveButton = Button(self, text="Save Recipe", command=lambda: self.saveRecipe())
        saveButton.grid(sticky=S)

        addFromWebsite = Button(self, text="Add from Website", command=lambda: self.addFromWebsite())
        addFromWebsite.grid(row=3, column=1)

    def addIngredient(self):

        self.ingList.append(Entry(self))
        self.ingList[-1].grid(row=self.rowTrack, column=1, pady=5, padx=20)
        self.rowTrack += 1

    def saveRecipe(self):

        save_path = 'C:/Users/sport/PycharmProjects/Recipe-Catalog/Recipes'
        recipeTitle = self.requiredTitle.get()
        directory = os.path.join(save_path, recipeTitle + '.txt')
        f = open(directory, "w")
        j = 0
        while j < len(self.ingList):
            f.write(self.ingList[j].get() + '\n')
            j += 1
        f.close()
        self.destroy()

    def addFromWebsite(self):
        top = Toplevel()
        top.geometry("400x75")
        top.title("Recipe App")

        urlLabel = Label(top, text="Paste URL")
        urlLabel.grid(row=1, column=0)
        url = Entry(top)
        url.grid(row=1, column=1)

        submit = Button(top, text="Submit", command=lambda: submit(url.get(), top))
        submit.grid(row=1, column=2)

        def submit(url, top):
            self.destroy()
            top.destroy()
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5555")
            socket.send_string(url)
            top = Toplevel()
            top.title("Saved!")
            message = socket.recv()
            message = message.decode("utf-8")
            saveLabel = Label(top, text=message)
            saveLabel.grid(row=0, column=1)


class EditPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="Recipe", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Catalog", command=lambda: controller.show_frame(RecipeStartPage))
        button1.pack()


app = RecipeCatalog()
app.mainloop()
