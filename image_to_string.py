import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import easyocr

class ImageTextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Text Extractor")

        # Create a button to select an image
        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=10)

        # Create a label to display the selected image
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Create a button to extract text from the selected image
        self.extract_button = tk.Button(root, text="Extract Text", command=self.extract_text)
        self.extract_button.pack(pady=10)

        # Create a label to display the extracted text
        self.text_label = tk.Label(root, wraplength=400, justify="left")
        self.text_label.pack()

        # Variable to store the selected image path
        self.image_path = None

        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(['en'])

    def select_image(self):
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("PDF files", "*.pdf"), ("all files", "*.*")))

        if file_path:
            self.image_path = file_path

            # Display the selected image
            image = Image.open(file_path)
            image = image.resize((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Clear the previous text when a new image is selected
            self.text_label.config(text="")

    def extract_text(self):
        if self.image_path:
            # Use EasyOCR to extract text from the image
            image = Image.open(self.image_path)
            result = self.reader.readtext(image)

            # Extracted text may contain multiple lines, join them
            text = '\n'.join([item[1] for item in result])

            # Display the extracted text
            self.text_label.config(text=text)
        else:
            # Display an error message if no image is selected
            self.text_label.config(text="Please select an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTextExtractorApp(root)
    root.mainloop()
