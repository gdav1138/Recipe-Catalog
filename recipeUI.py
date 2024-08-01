import tkinter
from tkinter import *
import os

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
            warningLabel = Label(top, text="Are you sure you wish to delete this recipe?" 
                            " Doing so will result in the loss of all data "
                            "associated with that recipe. Please confirm.")
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
            top.geometry("500x300")
            top.title("Recipe App")
            text_box = Text(top, height=100, width=50)
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
                f.close()
            listbox.delete(0, END)
            listbox.destroy()
            recipeSelect.destroy()
            deleteRecipe.destroy()

        recipeSelect = Button(self, text="View Recipe", command=selectedItem)
        deleteRecipe = Button(self, text="Delete Recipe", command=deletePrompt)
        recipeSelect.pack()
        deleteRecipe.pack()

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = Label(self, text="Recipe Home Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

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

    def addIngredient(self):

        self.ingList.append(Entry(self))
        self.ingList[-1].grid(row=self.rowTrack, column=1, pady=10, padx=10)
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

class EditPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="Edit Recipe", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Catalog", command=lambda: controller.show_frame(RecipeStartPage))
        button1.pack()

app = RecipeCatalog()
app.mainloop()