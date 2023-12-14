import os
import tkinter as tk
from tkinter import ttk,Tk,Button, Label, Listbox, filedialog, messagebox, StringVar
from PyPDF2 import PdfMerger
from PIL import Image
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Merger")

        self.file_paths = []

        self.label = Label(master, text="Drag or select files:")
        self.label.pack()

        self.listbox = Listbox(master, selectmode="multiple", height=5, width=40)
        self.listbox.pack()

        self.button_add = Button(master, text="Add Files", command=self.add_file)
        self.button_add.pack()

        self.button_clear = Button(master, text="Clear Files", command=self.clear_files)
        self.button_clear.pack()

        self.button_up = Button(master, text="Move Up", command=self.move_up)
        self.button_up.pack()

        self.button_down = Button(master, text="Move Down", command=self.move_down)
        self.button_down.pack()

        self.button_merge = Button(master, text="Merge to PDF", command=self.merge_to_pdf)
        self.button_merge.pack()

        self.label_resolution = Label(master, text="Image Resolution DPI:")
        self.label_resolution.pack()

        self.resolution_options = [72, 300]
        self.resolution_var = StringVar()
        self.resolution_var.set(self.resolution_options[0])  # default value
        self.combobox_resolution = ttk.Combobox(master, textvariable=self.resolution_var, values=self.resolution_options)
        self.combobox_resolution.pack()

        self.label_status = Label(master, text="")
        self.label_status.pack()

    def merge_to_pdf(self):
        try:
            pdf_merger = PdfMerger()

            for file_path in self.file_paths:
                _, file_extension = os.path.splitext(file_path.lower())

                if file_extension in ['.jpg', '.jpeg', '.png']:
                    img = Image.open(file_path)
                    pdf_path = f"{os.path.splitext(file_path)[0]}.pdf"
                    img.save(pdf_path, 'PDF', resolution=int(self.resolution_var.get()))
                    pdf_merger.append(pdf_path)
                    os.remove(pdf_path)

                elif file_extension == '.pdf':
                    pdf_merger.append(file_path)

            output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            pdf_merger.write(output_pdf_path)
            pdf_merger.close()

            self.label_status.config(text=f"PDF generated at: {output_pdf_path}")
            messagebox.showinfo("Success", "PDF merging completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def add_file(self):
        file_paths = filedialog.askopenfilenames(
            initialdir="/",
            title="Select Files",
            filetypes=(("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"), ("PNG files", "*.png"), ("PDF files", "*.pdf"), ("all files", "*.*")),
        )


        for file_path in file_paths:
            self.listbox.insert("end", os.path.basename(file_path))
            self.file_paths.append(file_path)


    def clear_files(self):
        self.listbox.delete(0, "end")
        self.file_paths = []

    def move_up(self):
        selected_indices = self.listbox.curselection()
        for i in selected_indices:
            if i > 0:
                self.swap_items(i, i - 1)

    def move_down(self):
        selected_indices = self.listbox.curselection()
        for i in reversed(selected_indices):
            if i < self.listbox.size() - 1:
                self.swap_items(i, i + 1)

    def swap_items(self, index1, index2):
        current_text = self.listbox.get(index1)
        target_text = self.listbox.get(index2)

        # Update file_paths using a temporary list
        temp_paths = self.file_paths[:]
        temp_paths[index1], temp_paths[index2] = temp_paths[index2], temp_paths[index1]
        self.file_paths = temp_paths

        self.listbox.delete(index1)
        self.listbox.insert(index1, target_text)
        self.listbox.delete(index2)
        self.listbox.insert(index2, current_text)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()