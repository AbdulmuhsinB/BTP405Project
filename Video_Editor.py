from tkinter import *
from tkinter import filedialog
from moviepy.editor import *
import threading
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['BTP425']
collection = db['user']

def signup_user(name, username, email, password):
    # Check if the username already exists
    if collection.find_one({"username": username}):
        return False, "Username already exists"
    else:
        # Insert new user into the database
        collection.insert_one({"name": name, "username": username, "email": email, "password": password})
        return True, "Signup successful"

def authenticate_user(username, password):
    # Check if the username and password are correct
    user = collection.find_one({"username": username, "password": password})
    return user

def toggle_signup():
    if signup_frame.winfo_ismapped():
        signup_frame.pack_forget()
    else:
        signup_frame.pack()

def signup():
    name = name_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        signup_status.config(text="Passwords do not match")
        return

    signup_success, message = signup_user(name, username, email, password)
    signup_status.config(text=message)
    
    if signup_success:
        # Automatically attempt to login after successful signup
        signup_status.config(text="Sign-up Complete")

def destroy_login_signup_frames():
    login_frame.destroy()
    signup_frame.destroy()
    
def login():
    # Retrieve username and password from entry fields
    username = username_entry.get()
    password = password_entry.get()

    # Authenticate user with MongoDB
    user = authenticate_user(username, password)

    if user:
        # If authentication is successful, initialize the editor
        initialize_editor(user)
        destroy_login_signup_frames()
    else:
        # If authentication fails, show an error message
        login_status.config(text="Invalid username or password")
   

def initialize_editor(user):
    # Main screen
    root.title("Video Editor")
    root.geometry("450x250")
    root.minsize(400, 150)
    root.maxsize(550, 300)
    root.config(bg="#232323")

    # Frame for labels
    label_frame.pack()

    # Display user's name
    welcome_label = Label(label_frame, text=f"Welcome, {user['name']}!", bg="#232323", fg="white")
    welcome_label.pack()

    # Processing label
    process_label.pack()

    # Functions for video editing

    def select_file():
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        return filename

    def ask_for_size(clip, file_name_entry):
        size_label = Label(label_frame, text="Enter Your Size:", bg="#232323", fg="white")
        size_label.pack()
        size_entry = Entry(label_frame)
        size_entry.pack()

        def get_size():
            r = float(size_entry.get())
            clip_resize = clip.resize(r)
            try:
                filename = file_name_entry.get()
                if filename.strip() == "":
                    filename = "Final_Render.mp4"
                clip_resize.write_videofile(f"{filename}.mp4")
                process_label.config(text="Processing complete")
            except Exception as e:
                process_label.config(text=f"Error: {e}")
            size_label.destroy()
            size_entry.destroy()
            confirm_button.destroy()

        confirm_button = Button(label_frame, text="Confirm", command=get_size)
        confirm_button.pack()

        process_label.config(text="Processing...")

    def concat(file_name_entry):
        num_videos_label = Label(label_frame, text="How many videos do you want to concatenate (up to 5)?", bg="#232323", fg="white")
        num_videos_label.pack()
        num_videos_entry = Entry(label_frame)
        num_videos_entry.pack()

        def get_num_videos():
            num_videos = int(num_videos_entry.get())
            if num_videos > 5:
                process_label.config(text="You can concatenate up to 5 videos.")
                return
            
            clips = []
            for i in range(num_videos):
                file = select_file()
                clip = VideoFileClip(file)
                clips.append(clip)
            
            final_clip = concatenate_videoclips(clips)
            try:
                filename = file_name_entry.get()
                if filename.strip() == "":
                    filename = "Final_Render.mp4"
                final_clip.write_videofile(f"{filename}.mp4")
                process_label.config(text="Processing complete")
            except Exception as e:
                process_label.config(text=f"Error: {e}")
            num_videos_label.destroy()
            num_videos_entry.destroy()
            confirm_button.destroy()

        confirm_button = Button(label_frame, text="Confirm", command=get_num_videos)
        confirm_button.pack()

        process_label.config(text="Processing...")

    def mirror(file_name_entry):
        file = select_file()
        clip = VideoFileClip(file)
        clip_mirror = clip.fx(vfx.mirror_x)
        try:
            filename = file_name_entry.get()
            if filename.strip() == "":
                filename = "Final_Render.mp4"
            clip_mirror.write_videofile(f"{filename}.mp4")
            process_label.config(text="Processing complete")
        except Exception as e:
            process_label.config(text=f"Error: {e}")

    def trim(file_name_entry):
        file = select_file()
        clip = VideoFileClip(file)
        start_label = Label(label_frame, text="Enter the starting point:", bg="#232323", fg="white")
        start_label.pack()
        start_entry = Entry(label_frame)
        start_entry.pack()

        end_label = Label(label_frame, text="Enter the ending point:", bg="#232323", fg="white")
        end_label.pack()
        end_entry = Entry(label_frame)
        end_entry.pack()

        def get_trim():
            start_point = int(start_entry.get())
            end_point = int(end_entry.get())
            clip_trim = clip.cutout(start_point, end_point)
            try:
                filename = file_name_entry.get()
                if filename.strip() == "":
                    filename = "Final_Render.mp4"
                clip_trim.write_videofile(f"{filename}.mp4")
                process_label.config(text="Processing complete")
            except Exception as e:
                process_label.config(text=f"Error: {e}")
            start_label.destroy()
            start_entry.destroy()
            end_label.destroy()
            end_entry.destroy()
            confirm_button.destroy()

        confirm_button = Button(label_frame, text="Confirm", command=get_trim)
        confirm_button.pack()

        process_label.config(text="Processing...")

    def audio(file_name_entry):
        file_video = select_file()
        clip_video = VideoFileClip(file_video)
        file_audio = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
        clip_audio = AudioFileClip(file_audio)
        clip_final = clip_video.set_audio(clip_audio)
        try:
            filename = file_name_entry.get()
            if filename.strip() == "":
                filename = "Final_Render.mp4"
            clip_final.write_videofile(f"{filename}.mp4")
            process_label.config(text="Processing complete")
        except Exception as e:
            process_label.config(text=f"Error: {e}")

    def start_thread(target, file_name_entry):
        process_label.config(text="Processing...")
        thread = threading.Thread(target=target, args=(file_name_entry,))
        thread.start()

    # Buttons for video editing
    buttons = [
        ("Concat", concat),
        ("Mirror", mirror),
        ("Trim", trim),
        ("Audio", audio)
    ]

    file_name_entry = Entry(root, width=50)
    file_name_entry.pack()
    file_name_entry.insert(0, "Enter name for the file after editing")
    for text, command in buttons:
        b = Button(root, text=text, relief=GROOVE, bg="#232323", fg="white", command=lambda cmd=command, fname=file_name_entry: start_thread(cmd, fname))
        b.pack(side="left", padx=20)
        b.config(width=8, height=3)

def start_thread(target, file_name_entry):
    process_label.config(text="Processing...")
    thread = threading.Thread(target=target, args=(file_name_entry,))
    thread.start()

# GUI setup
root = Tk()
root.title("Signup/Login")

# Login frame
login_frame = Frame(root)
login_frame.pack()

username_label = Label(login_frame, text="Username:")
username_label.pack()
username_entry = Entry(login_frame)
username_entry.pack()

password_label = Label(login_frame, text="Password:")
password_label.pack()
password_entry = Entry(login_frame, show="*")
password_entry.pack()

login_button = Button(login_frame, text="Login", command=login)
login_button.pack()

signup_button = Button(login_frame, text="Signup", command=toggle_signup)
signup_button.pack()

# Create login status label
login_status = Label(login_frame, text="", fg="red")
login_status.pack()

# Signup frame
signup_frame = Frame(root)

name_label = Label(signup_frame, text="Name:")
name_label.pack()
name_entry = Entry(signup_frame)
name_entry.pack()

username_label = Label(signup_frame, text="Username:")
username_label.pack()
username_entry = Entry(signup_frame)
username_entry.pack()

email_label = Label(signup_frame, text="Email:")
email_label.pack()
email_entry = Entry(signup_frame)
email_entry.pack()

password_label = Label(signup_frame, text="Password:")
password_label.pack()
password_entry = Entry(signup_frame, show="*")
password_entry.pack()

confirm_password_label = Label(signup_frame, text="Confirm Password:")
confirm_password_label.pack()
confirm_password_entry = Entry(signup_frame, show="*")
confirm_password_entry.pack()

signup_button = Button(signup_frame, text="Signup", command=signup)
signup_button.pack()

signup_status = Label(signup_frame, text="")
signup_status.pack()

# Hide signup frame by default
signup_frame.pack_forget()

# Frame for labels
label_frame = Frame(root, bg="#232323", pady=10)

# Processing label
process_label = Label(label_frame, text="", bg="#232323", fg="white")

root.mainloop()
