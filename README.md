# Password-Manager
A password manager made in python which generates one-time emails for you along with an efficient search function, all made using CTk. 

## Features:
- An email generator using DuckDuckGo Private Emails
- Password generator
- Easy search functionality
- Place to view all the stored password
- A catppuccin color scheme, with a light and dark mode

## Email generator set-up

To use the email generation capabilities of the password manager, you first need to have a duckduckgo private email address.
Log into your duckduckgo email account and open up your console to the network tab. Then, clikc the generate email button, where you should see two requests load up on your network tab.      ![image](https://github.com/user-attachments/assets/d5f613d7-7a5d-4a7c-ad26-a349df3c4b10)

Then, click on the first request and copy the authorization key, along with the word Bearer.
![image](https://github.com/user-attachments/assets/c1baef3b-bb2f-4470-a591-38893c72064a)

Paste it into the variable Auth_key in the main.py like this:
![image](https://github.com/user-attachments/assets/1c3d7c79-0cbd-4bdd-920a-a0462435bc64)
The auth key should look something like this: `Bearer xysdyhdosfhkfhsgiuybdfiniuvgydfiuvhiuoghdfviouh`
Once the auth key is pasted, the setup for the email generator is done. Please let me know in the issues if there is a way to simplify this process or if something is unclear.

## Using the program
Simply clone this into the folder you want using: `git clone https://github.com/Anonymous-ABC-XYZ/Password-Manager.git`
Then, run `pip -r requirements.txt`. You can then use the password manager. Enjoy!

## Images
![image](https://github.com/user-attachments/assets/0e7bb136-08bb-45cc-9722-6761681946a2)
![image](https://github.com/user-attachments/assets/4897b30a-129b-4cc1-af68-e41c4230920e)
![image](https://github.com/user-attachments/assets/ddc13bd2-377e-4cdb-b1ac-2a7afef09b0d)
![image](https://github.com/user-attachments/assets/fd26ab42-d085-4fc7-a3ef-31a4d6f5766d)



## To-do
- [ ] Shift to Electron

## Features
Please raise an issue if you want additional features like encryption for the passwords, which I use on my personal version, but it might complicate some users lives.
