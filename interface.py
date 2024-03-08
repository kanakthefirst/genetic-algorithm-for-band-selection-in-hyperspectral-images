import tkinter as tk
from tkinter import filedialog
import genetic_algo


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_file1 = tk.Button(self, text="Hyperspectral Image Data File", command=self.browse_file1)
        self.select_file1.pack()

        self.select_file2 = tk.Button(self, text="Target file to train", command=self.browse_file2)

        self.select_file2.pack()

        l1 = tk.Label(self,text="no. of bands to select:")
        l1.pack()
        self.num_bands = tk.Text(self,height=1)
        self.num_bands.pack()

        l2 = tk.Label(self,text="no. of individuals to initialize:")
        l2.pack()
        self.num_inds = tk.Text(self,height=1)
        self.num_inds.pack()

        l3 = tk.Label(self, text="no. of generations to before stopping:")
        l3.pack()
        self.num_gens = tk.Text(self,height=1)
        self.num_gens.pack()

        self.run_button = tk.Button(self, text="Run", command=self.run_program)
        self.run_button.pack()

        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit.pack()


    def browse_file1(self):
        self.file1 = filedialog.askopenfilename()

    def browse_file2(self):
        self.file2 = filedialog.askopenfilename()
    
    def run_program(self):
        num_bands = int(self.num_bands.get(1.0, "end-1c"))
        num_inds = int(self.num_inds.get(1.0, "end-1c"))
        num_gens = int(self.num_gens.get(1.0, "end-1c"))

        output, score0, score1 = genetic_algo.run(self.file1, self.file2, num_bands, num_inds, num_gens)
        
        mylist = tk.Listbox(root ,width=100)

        mylist.insert(tk.END, 'The selected bands are :')
        mylist.insert(tk.END, str(', '.join([str(i) for i in sorted(output)])))
        mylist.insert(tk.END, 'The accuracy obtained is :')
        mylist.insert(tk.END, str(score0[0]))
        # mylist.insert(tk.END, str(score1))
        mylist.pack( side = tk.LEFT, fill = tk.BOTH )

root = tk.Tk()
app = Application(master=root)
app.mainloop()
