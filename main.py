from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymupdf
from PIL import Image, ImageTk
from pathlib import Path
import json
import os

root = Tk()
root.title("GENESIS")
root.geometry('1200x750')
root.configure(bg='black')

b_storage_dir = "books"
folder_path = Path(b_storage_dir)
first_book = next(folder_path.iterdir(), None)
doc = pymupdf.open(first_book)

try:
    os.mkdir(b_storage_dir)
    print(f"Directory {b_storage_dir} created successfully")
except FileExistsError:
    print(f"Directory {b_storage_dir} already exists, no need to create it again.")
except PermissionError:
    print(f"Permission denied: Unable to create the directory {b_storage_dir}")
except Exception as e:
    print(f"An error occurred: {e}")

#Inicializacion de pagina de pdfs.
current_page = 0
current_book = ""

page = doc[current_page]         
pix = page.get_pixmap()
mode = "RGBA" if pix.alpha else "RGB"
img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
tkimg = ImageTk.PhotoImage(img)


def change_page(next = True, update_only = False):
    global current_page

    if update_only:
        current_page = 0
    elif next == True:
        current_page += 1
    elif next == False:
        current_page -= 1
    
    if current_page >= len(doc):
        current_page = 0
    elif current_page < 0:
        current_page = doc.page_count - 1

    page = doc[current_page]
    pix = page.get_pixmap()

    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

    tkimg = ImageTk.PhotoImage(img)

    pdf_pages_label.config(image=tkimg)

    pdf_pages_label.image = tkimg
    number_of_pages_counter.configure(text= current_page + 1)


def change_book(book_name):
    global doc, current_page

    doc = pymupdf.open(rf"books/{book_name}")

    current_page = 0

    if os.path.isfile("books_data.json"):
        with open("books_data.json", "r") as file:
            data = json.load(file)

            for book in data["books"]:
                if book["name_of_book"] == book_name:
                    current_page = book["number_of_pages"]
                    break

    page = doc[current_page]
    pix = page.get_pixmap()

    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(
        mode,
        [pix.width, pix.height],
        pix.samples
    )

    tkimg = ImageTk.PhotoImage(img)

    pdf_pages_label.config(image=tkimg)
    pdf_pages_label.image = tkimg

    number_of_pages_counter.configure(text=current_page + 1)


    page = doc[current_page]
    pix = page.get_pixmap()
    
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    
    tkimg = ImageTk.PhotoImage(img)
    
    pdf_pages_label.config(image=tkimg)
    
    pdf_pages_label.image = tkimg
    number_of_pages_counter.configure(text= current_page + 1)
    
   

def save_data_of_books(name_of_book):
    new_book = {
        "name_of_book": name_of_book,
        "number_of_pages": current_page
    }

    if os.path.isfile("books_data.json"):
        with open("books_data.json", "r+") as file:
            data = json.load(file)

            book_found = False

            for book in data["books"]:
                if book["name_of_book"] == name_of_book:
                    book["number_of_pages"] = current_page
                    book_found = True
                    break

            if not book_found:
                data["books"].append(new_book)

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    else:
        starter_data = {
            "books": [new_book]
        }

        with open("books_data.json", "w") as file:
            json.dump(starter_data, file, indent=4)

    messagebox.showinfo("Progress Saved", "Your progress has been saved.")


style = ttk.Style()
style.configure("CustomColor.TFrame", background="#1F1F1F", borderwidth=0)

label_style = ttk.Style()
label_style.configure("CustomStyle.Label",foreground="#FFFFFF", background="#000000")


frame_one = ttk.Frame(root,style="CustomColor.TFrame")
pdf_reader_label = ttk.Label(frame_one, style="CustomStyle.Label", text="GENESIS READER", justify="center", anchor="center")

button_frame = ttk.Frame(frame_one,style="CustomColor.TFrame")
button_frame.grid(row = 1, column = 0, sticky = 'nsew', padx=10, pady=10)
button_frame.columnconfigure(0, weight=1)
button_frame.rowconfigure(0, weight=1)

canvas = Canvas(button_frame, bg='#454545',bd=0,highlightthickness=0, scrollregion=(0, 0, 2000, 5000))
scrollbar = ttk.Scrollbar(button_frame, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

# Frame interno donde van los botones
inner_frame = ttk.Frame(canvas,style="CustomColor.TFrame")
inner_frame.columnconfigure(0, weight=1)
inner_frame.rowconfigure(0, weight=1)
canvas.create_window((10, 10), window=inner_frame, anchor='nw')

for row, i in enumerate(folder_path.iterdir(), start=1):
    book_name = i.name
    new_button = Button(
        inner_frame,
        text=book_name,
        bg="#000000",
        fg="#FFFFFF",
        activebackground="#222222",
        activeforeground="#454545",
        relief="flat",
        borderwidth=1,
        command=lambda book=book_name: change_book(book),
        padx=10,
        pady=10
    )
    new_button.grid(row=row, column=0, sticky="ew", padx=10, pady=10)


frame_two = ttk.Frame(root,style="CustomColor.TFrame")

pdf_pages_label = ttk.Label(frame_two, image=tkimg, anchor="center")

############## FRAME CONFIGURATION RIGHT SIDE ##############################

change_pages_frame = ttk.Frame(frame_two, style="CustomColor.TFrame")
change_pages_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
change_pages_frame.columnconfigure(0, weight=1)
change_pages_frame.rowconfigure(0, weight=1)  # espacio arriba
change_pages_frame.rowconfigure(3, weight=1)

############## FRAME CONFIGURATIONS RIGHT SIDE ##############################

############## RIGHT SIDE BUTTONS AND NUMBER OF PAGES LABEL ##############################

change_page_left_button = Button(change_pages_frame, text="Back",bg="#000000",fg="#FFFFFF",activebackground="#222222",activeforeground="#454545",relief="flat",borderwidth=1,padx=10,pady=10, command=lambda: change_page(False))
change_page_right_button = Button(change_pages_frame, text="Next",bg="#000000",fg="#FFFFFF",activebackground="#222222",activeforeground="#454545",relief="flat",borderwidth=1,padx=10,pady=10, command=lambda: change_page(True))
save_current_location_pages = Button(change_pages_frame, text="Save",bg="#000000",fg="#FFFFFF",activebackground="#222222",activeforeground="#454545",relief="flat",borderwidth=1,padx=10,pady=10, command=lambda: save_data_of_books(Path(doc.name).name))
number_of_pages_counter = ttk.Label(change_pages_frame,text = current_page + 1, style ="CustomStyle.Label", font=("Arial", 20, "bold"), justify="center", anchor="center")

############## RIGHT SIDE BUTTONS AND NUMBER OF PAGES LABEL ##############################


############## RIGHT SIDE BUTTONS AND NUMBER OF PAGES LABEL GRID CONFIGURATION ##############################

change_page_left_button.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
change_page_right_button.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
save_current_location_pages.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
number_of_pages_counter.grid(row = 4, column = 0, ipadx=10, ipady=10)

############## RIGHT SIDE BUTTONS AND NUMBER OF PAGES LABEL GRID CONFIGURATION ##############################


root.columnconfigure(0, weight= 1, uniform='a')
root.columnconfigure(1, weight= 2, uniform='a')
root.rowconfigure(0, weight= 1, uniform='a')


frame_two.grid(row = 0, column = 1, sticky = 'nsew' )
frame_one.grid(row = 0 ,column = 0, sticky='nsew',padx=10,pady=10)
frame_one.columnconfigure(0, weight=1, uniform='a')
frame_one.rowconfigure(0, weight=1, uniform='a')
frame_one.rowconfigure(1, weight=8, uniform='a')


frame_two.columnconfigure(0, weight=2, uniform='a') #Configuracion de columnas panel derecho
frame_two.columnconfigure(1, weight=1, uniform='a') #Configuracion de columnas panel derecho
frame_two.rowconfigure(0, weight=1, uniform='a')

pdf_pages_label.grid(row = 0, column = 0, sticky = 'ns', padx=10, pady=10)


pdf_reader_label.grid(row=0,column=0, sticky="n", padx=10, pady=10 , ipadx=100, ipady=10)

root.mainloop()
