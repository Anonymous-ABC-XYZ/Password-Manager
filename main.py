from tkinter import *
import customtkinter
from CTkMessagebox import CTkMessagebox
import random
import pyperclip
import json
import requests as rq
from fuzzywuzzy import fuzz

FONT = ("Arial", 18, "bold")
FONT_LABEL = ("Arial", 18)
Background_color = "#181825"
Text_color = "white"
Button_color = "#CBA6F7"
Button_text_color = "#FFFFFF"
HOVER_COLOR = "#B4BEFE"
windowtwo_txtclr = "#000000"
CORNER_RADIUS = 30
WINDOWTWO_RADIUS = 15
Auth_key = ""

dark_mode = True
mode = "Light"
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

passwords_json = "./passwords.json"
passwords_text = "./passwords.txt"
logo = "./logo.png"
delete = "./delete-button.png"


# ---------------------------- DARK/LIGHT MODE ------------------------------- #
def callback(event):
    window.after(50, select_all, event.widget)


def select_all(widget):
    widget.select_range(0, 'end')
    widget.icursor('end')


def callback_search(event):
    find_password()


def change():
    global Text_color
    global dark_mode
    global mode
    global Background_color
    if dark_mode:
        Text_color = "white"
        Background_color = "#181825"
        mode = "Light"
        change_button.configure(text=mode)
        website_label.configure(text="Website: ", font=FONT_LABEL,
                                text_color=Text_color, bg_color=Background_color)
        email_label.configure(text="Email/Username: ", font=FONT_LABEL,
                              text_color=Text_color, bg_color=Background_color)
        password_label.configure(text="Password: ", height=35, font=FONT_LABEL,
                                 text_color=Text_color, bg_color=Background_color)
        window.config(bg=Background_color)
        generate_email_button.configure(bg_color=Background_color)
        add_button.configure(bg_color=Background_color)
        search_button.configure(bg_color=Background_color)
        change_button.configure(bg_color=Background_color)
        view_button.configure(bg_color=Background_color)
        generate_password.configure(bg_color=Background_color)

    else:
        Text_color = "black"
        Background_color = "#FFFFFF"
        mode = "Dark"
        change_button.configure(text=mode)
        website_label.configure(text="Website: ", font=FONT_LABEL,
                                text_color=Text_color, bg_color=Background_color)
        email_label.configure(text="Email/Username: ", font=FONT_LABEL,
                              text_color=Text_color, bg_color=Background_color)
        password_label.configure(text="Password: ", height=35, font=FONT_LABEL,
                                 text_color=Text_color, bg_color=Background_color)
        generate_email_button.configure(bg_color=Background_color)
        add_button.configure(bg_color=Background_color)
        search_button.configure(bg_color=Background_color)
        generate_password.configure(bg_color=Background_color)
        change_button.configure(bg_color=Background_color)
        view_button.configure(bg_color=Background_color)
        window.config(bg=Background_color)


def decide_mode():
    global dark_mode
    if dark_mode:
        dark_mode = False
        change()
    elif not dark_mode:
        dark_mode = True
        change()

# Email generation
def generate_email():
    headers = {
        'Accept': '*/*,',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Authorization': Auth_key,
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'DNT': '1',
        'Host': 'quack.duckduckgo.com',
        'Origin': 'https://duckduckgo.com',
        'Referer': 'https://duckduckgo.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'TE': 'trailers',
    }

    response = rq.post(url='https://quack.duckduckgo.com/api/email/addresses', headers=headers)
    duckduckgo_email = str(response.json()['address']) + "@duck.com"
    print(duckduckgo_email)
    pyperclip.copy(duckduckgo_email)
    email_entry.delete(0, "end")
    email_entry.insert(0, duckduckgo_email)


# ---------------------------- VIEW PASSWORDS ------------------------------- #

def view_passwords():
    global delete_button_img
    window1 = customtkinter.CTk()

    window1.config(bg=Background_color, padx=20)

    password_frame = customtkinter.CTkScrollableFrame(window1)
    password_frame.grid(row=0, column=0, padx=50, pady=(10, 0), sticky="nsew")
    password_frame._scrollbar.configure(width=25, corner_radius=3, button_color=Button_color,
                                       button_hover_color=HOVER_COLOR)
    password_frame.bind("<Button-4>", lambda e: password_frame._parent_canvas.yview("scroll", -3, "units"))
    password_frame.bind("<Button-5>", lambda e: password_frame._parent_canvas.yview("scroll", 3, "units"))
    password_frame.configure(height=700, width=1830, fg_color=Background_color)

    def copy(text):
        pyperclip.copy(text)

    def remove_list(number: int):

        with open(passwords_text, "r") as f:
            lines = f.readlines()
            line_to_del = lines[number]
        f.close()
        with open(passwords_text, "w") as fil:
            for line in lines:
                if line != line_to_del:
                    fil.write(line)
        fil.close()

        with open(passwords_json, 'r') as fp:
            data = json.load(fp)
            del data[str(line_to_del.split('|')[0].strip().split(': ')[1])]
            with open(passwords_json, 'w') as new_fp:
                json.dump(data, new_fp)
        fp.close()

        window1.destroy()
        view_passwords()

    def make_the_boxes():
        with open(passwords_text, "r") as file_path:
            password = file_path.readlines()
            password_box = []
            email_box = []
            website_box = []
            remove_box = []
            delete_button_img = PhotoImage(file=delete, master=password_frame)

            for k in range(1, len(password)):
                website_with_label = password[k].split('|')[0].strip()
                website_without_label = website_with_label.split(': ')
                website_box.append(
                    customtkinter.CTkButton(master=password_frame, text=f"Website: {website_without_label[1]}",
                                            command=lambda x=website_without_label[1]: copy(x), height=50,
                                            border_width=0,
                                            border_color="black", corner_radius=WINDOWTWO_RADIUS, fg_color=Button_color,
                                            hover_color=HOVER_COLOR, font=FONT_LABEL, width=30,
                                            text_color=windowtwo_txtclr))
                website_box[k - 1].grid(row=k, column=1, sticky='ew')

            for j in range(1, len(password)):
                email_with_label = password[j].split('|')[1].strip()
                email_without_label = email_with_label.split(': ')
                email_box.append(customtkinter.CTkButton(master=password_frame, text=f"Email: {email_without_label[1]}",
                                                         command=lambda z=email_without_label[1]: copy(z),
                                                         height=50, border_width=0, border_color=Button_color,
                                                         corner_radius=WINDOWTWO_RADIUS, font=FONT_LABEL,
                                                         fg_color=Button_color, hover_color=HOVER_COLOR, width=30,
                                                         text_color=windowtwo_txtclr))
                email_box[j - 1].grid(row=j, column=2, sticky='ew', padx=40, pady=15)

            for i in range(1, len(password)):
                password_with_label = password[i].split('|')[2].strip()
                password_without_label = password_with_label.split(': ')
                password_box.append(
                    customtkinter.CTkButton(master=password_frame, text=f"Password: {password_without_label[1]}",
                                            command=lambda y=password_without_label[1]: copy(y), height=50,
                                            border_width=0, border_color="black", corner_radius=WINDOWTWO_RADIUS,
                                            fg_color=Button_color, font=FONT_LABEL,
                                            hover_color=HOVER_COLOR, border_spacing=0, width=70,
                                            text_color=windowtwo_txtclr))
                password_box[i - 1].grid(row=i, column=3, sticky='ew')

            for m in range(1, len(password)):
                remove_box.append(customtkinter.CTkButton(master=password_frame, text="", image=delete_button_img,
                                                          height=30, border_width=0, border_color=Button_color,
                                                          corner_radius=WINDOWTWO_RADIUS, width=4,
                                                          fg_color="transparent",
                                                          hover_color=HOVER_COLOR,
                                                          command=lambda num=m: remove_list(num)))
                remove_box[m - 1].grid(row=m, column=4, sticky='ew', padx=10, pady=15)
        file_path.close()

    make_the_boxes()
    window1.mainloop()


def search_pass():
    print("hello")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def create_password():
    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(5, 7)
    nr_numbers = random.randint(6, 7)
    password_list = [random.choice(letters) for n in range(nr_letters)]
    password_list += [random.choice(numbers) for n in range(nr_numbers)]
    password_list += [random.choice(symbols) for n in range(nr_symbols)]

    random.shuffle(password_list)

    password = ""
    for character in password_list:
        password += character
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "" or email == "" or password == "":
        CTkMessagebox(title="Error", message="Enter the details!", font=FONT_LABEL)
    else:
        ok = CTkMessagebox(title=website,
                           message=f"These are the details:\n Email: {email}\n Password: {password} \n Do you wish to proceed?",
                           font=FONT_LABEL, button_width=25)
        if ok:
            file = open(passwords_json, "r")
            data = json.load(file)
            data.update(new_data)

            file1 = open(passwords_json, "w")
            json.dump(data, file1, indent=4)

            file = open(passwords_text, "a")
            file.write(f"Website: {website} | Email: {email} | Password: {password}\n")

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- Find Passwords ------------------------------- #
def find_password():
    global website_entry
    website = website_entry.get()
    file = open(passwords_json, "r")
    data = json.load(file)
    counter = 0
    for website_matching in data:
        fuzz_match = fuzz.partial_ratio(f"{website.lower()}", f"{website_matching.lower()}")
        if counter == 0:
            highest = fuzz_match
            matched_website = website_matching
        elif counter > 0:
            if int(fuzz_match) > int(highest):
                highest = fuzz_match
                matched_website = website_matching
        counter += 1

    email = data[matched_website]['email']
    password = data[matched_website]['password']
    msg = CTkMessagebox(title=f"Requested information", width=1000,
                        message=f"The email and password for {matched_website} are as follows:",
                        option_2=f"Email:{email}", option_1=f"Password:{password}", button_color=Button_color,
                        button_hover_color=HOVER_COLOR, bg_color=Background_color, fg_color=Background_color,
                        font=FONT, button_text_color=windowtwo_txtclr)

    if msg.get() == f"Email:{email}":
        pyperclip.copy(email)
    elif msg.get() == f"Password:{password}":
        pyperclip.copy(password)


# ---------------------------- UI SETUP ------------------------------- #
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

window = customtkinter.CTk()
window.config(bg="#181825")
window.config(padx=50)
window.minsize(800, 550)
window.title('Password Manager')
window.attributes('-alpha', 0.5)
# ---------------------------- DARK/LIGHT MODE BUTTON ------------------------------- #

change_button = customtkinter.CTkButton(master=window, text=mode, text_color=Button_text_color, font=FONT,
                                        height=60, command=decide_mode, corner_radius=12, fg_color=Button_color,
                                        hover_color=HOVER_COLOR, border_width=1, bg_color=Background_color)
change_button.grid(row=0, column=1, pady=15, sticky="nsew")

# ---------------------------- CANVAS ------------------------------- #
my_pass_img = PhotoImage(file=logo)
view_button = customtkinter.CTkButton(master=window, text="", text_color="white", font=FONT, width=750,
                                      height=200, command=view_passwords, image=my_pass_img, bg_color=Background_color,
                                      fg_color=Button_color, hover_color=HOVER_COLOR)
view_button.grid(row=1, column=1, pady=15, sticky="nsew")

# ---------------------------- WEBSITE ENTRY ------------------------------- #
website_label = customtkinter.CTkLabel(master=window, text="Website: ", font=FONT_LABEL,
                                       text_color=Text_color, bg_color=Background_color, compound="center")
website_label.grid(row=2, column=0, pady=12, padx=15, sticky="nsew")

website_entry = Entry(width=35, font=("Urbanist", 17))
website_entry.grid(row=2, column=1, pady=12, padx=15, sticky="nsew")
website_entry.bind('<Control-a>', callback)
website_entry.bind('<Return>', func=callback_search)

search_button = customtkinter.CTkButton(master=window, text="Search", text_color=Button_text_color,
                                        font=FONT, width=35, height=40, command=find_password,
                                        corner_radius=CORNER_RADIUS, border_color="#242424", fg_color=Button_color,
                                        hover_color=HOVER_COLOR, bg_color=Background_color)
search_button.grid(row=2, column=2, pady=5, sticky="nsew")

website_entry.focus()
# ---------------------------- EMAIL/USERNAME ENTRY ------------------------------- #

email_label = customtkinter.CTkLabel(master=window, text="Email/Username: ", font=FONT_LABEL,
                                     text_color=Text_color, bg_color=Background_color, anchor="e")
email_label.grid(row=3, column=0, pady=5, sticky="nsew")

email_entry = Entry(width=35, font=("Urbanist", 17))
email_entry.grid(row=3, column=1, columnspan=1, pady=12, padx=15, sticky="nsew")
email_entry.bind('<Control-a>', callback)

generate_email_button = customtkinter.CTkButton(master=window, text="Generate Email", text_color=Button_text_color,
                                                font=FONT, width=20, height=40, command=generate_email,
                                                corner_radius=CORNER_RADIUS, fg_color=Button_color,
                                                hover_color=HOVER_COLOR, bg_color=Background_color)
generate_email_button.grid(row=3, column=2, padx=(2, 0), pady=5, sticky="nsew")

# ---------------------------- PASSWORD ENTRY ------------------------------- #
password_label = customtkinter.CTkLabel(master=window, text="Password: ", height=35, font=FONT_LABEL,
                                        text_color=Text_color, corner_radius=50, bg_color=Background_color, anchor="e")
password_label.grid(row=4, column=0, pady=12, padx=15, sticky="nsew")

password_entry = Entry(width=35, font=("Urbanist", 17))
password_entry.grid(row=4, column=1, columnspan=1, pady=15, padx=15, sticky="nsew")
password_entry.bind('<Control-a>', callback)

generate_password = customtkinter.CTkButton(master=window, text="Generate Password", text_color=Button_text_color,
                                            font=FONT, width=10, height=40, command=create_password,
                                            fg_color=Button_color, hover_color=HOVER_COLOR,
                                            bg_color=Background_color, corner_radius=CORNER_RADIUS)
generate_password.grid(row=4, column=2, padx=(2, 0), pady=5, sticky="nsew")

# ---------------------------- ADD ------------------------------- #
add_button = customtkinter.CTkButton(master=window, text="Add", text_color=Button_text_color, font=FONT, width=10,
                                     height=60, command=add_password, corner_radius=50, fg_color=Button_color,
                                     hover_color=HOVER_COLOR, bg_color=Background_color)
add_button.grid(row=5, column=1, columnspan=2, pady=15, sticky="nsew")

# ---------------------------- SEARCH ------------------------------- #


window.mainloop()
