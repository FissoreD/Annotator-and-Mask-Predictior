import tkinter as tk


class App():

    def __init__(self):

        # fenêtre principale (root)
        self.root = tk.Tk()
        self.root.title('My tk app')
        self.root.geometry('400x300+200+200')

        self.initWidgets()

    def initWidgets(self):

        # canvas (parent = root)
        self.canvas = tk.Canvas(self.root, bg="white", width=400, height=300)
        self.canvas.grid(row=0, column=0)

        # gros bouton (parent = canvas)
        self.bigButton = tk.Button(
            self.canvas, width=12, height=6, bg="#8ccac9")
        self.bigButton.place(relx=0.5, rely=0.5, anchor='center')

        # petit bouton (parent = gros bouton)
        self.smallButton = tk.Button(
            self.bigButton, width=8, height=2, bg="#bbca8c")
        self.smallButton.place(relx=0.5, rely=0.5, anchor='center')


if __name__ == '__main__':

    app = App()
    app.root.mainloop()
