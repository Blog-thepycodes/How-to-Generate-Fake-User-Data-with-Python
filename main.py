import os
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, IntVar, Checkbutton, filedialog, Text, OptionMenu, \
   Radiobutton
from faker import Faker
from faker.providers import internet
import csv
 
 
 
 
# Function to create a standard set of fake user information
def create_standard_user(fake, gender):
   if gender == 'male':
       name = fake.name_male()
   elif gender == 'female':
       name = fake.name_female()
   else:
       name = fake.name()
 
 
   return {
       'Full Name': name,
       'Email Address': fake.email(),
       'Phone': fake.phone_number(),
       'Street Address': fake.address(),
       'City Name': fake.city(),
       'Country Name': fake.country(),
   }
 
 
 
 
# Function to create a detailed set of fake user information
def create_detailed_user(fake, gender):
   if gender == 'male':
       name = fake.name_male()
   elif gender == 'female':
       name = fake.name_female()
   else:
       name = fake.name()
 
 
   return {
       'Full Name': name,
       'Email Address': fake.email(),
       'Phone': fake.phone_number(),
       'Birth Date': fake.date_of_birth(),
       'Street Address': fake.address(),
       'City Name': fake.city(),
       'Country Name': fake.country(),
       'Postal Code': fake.zipcode(),
       'Occupation': fake.job(),
       'Company Name': fake.company(),
       'Private IP': fake.ipv4_private(),
       'Card Number': fake.credit_card_number(),
       'User ID': fake.user_name(),
       'Website URL': fake.url(),
       'Social Security Number': fake.ssn()
   }
 
 
 
 
# Function to generate user data
def generate_user_data(count, detailed=False, gender=None):
   fake = Faker()
   fake.add_provider(internet)
   user_list = []
   for _ in range(count):
       if detailed:
           user_list.append(create_detailed_user(fake, gender))
       else:
           user_list.append(create_standard_user(fake, gender))
   return user_list
 
 
 
 
# Function to save data to CSV
def save_to_csv(data, filename):
   keys = data[0].keys()
   if os.path.exists(filename):
       overwrite = messagebox.askyesno("Overwrite?", f"{filename} already exists. Overwrite?")
       if not overwrite:
           return
   with open(filename, 'w', newline='') as file:
       writer = csv.DictWriter(file, fieldnames=keys)
       writer.writeheader()
       writer.writerows(data)
   messagebox.showinfo("Success", f"Data successfully saved to {filename}")
 
 
 
 
# Function to save data to text file
def save_to_text(data, filename):
   if os.path.exists(filename):
       overwrite = messagebox.askyesno("Overwrite?", f"{filename} already exists. Overwrite?")
       if not overwrite:
           return
   with open(filename, 'w') as file:
       for entry in data:
           for key, value in entry.items():
               file.write(f"{key}: {value}\n")
           file.write("\n")
   messagebox.showinfo("Success", f"Data successfully saved to {filename}")
 
 
 
 
# Function to display data on the console
def display_data(data):
   result_window = Tk()
   result_window.title("Generated Data - The Pycodes")
   result_window.geometry("600x400")
   text_widget = Text(result_window)
   text_widget.pack(expand=True, fill='both')
   for entry in data:
       for key, value in entry.items():
           text_widget.insert('end', f"{key}: {value}\n")
       text_widget.insert('end', "\n")
   result_window.mainloop()
 
 
 
 
# Function to handle generation and saving of user data
def handle_generate():
   try:
       count = int(user_count_var.get())
       if count <= 0:
           raise ValueError("Number of users must be a positive integer.")
   except ValueError as e:
       messagebox.showerror("Error", str(e))
       return
 
 
   detailed = detailed_var.get()
   gender = gender_var.get()
   users = generate_user_data(count, detailed, gender)
 
 
   if save_var.get():
       file_type = file_type_var.get()
       if file_type in ['csv', 'csv and txt']:
           csv_filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
           if csv_filename:
               save_to_csv(users, csv_filename)
 
 
       if file_type in ['txt', 'csv and txt']:
           txt_filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
           if txt_filename:
               save_to_text(users, txt_filename)
 
 
       if file_type not in ['csv', 'txt', 'csv and txt']:
           messagebox.showerror("Error", "Invalid file type. Data not saved.")
   else:
       display_data(users)
 
 
 
 
# Set up the Tkinter window
root = Tk()
root.title("User Data Generator - The Pycodes")
root.geometry("400x450")
 
 
# User count entry
Label(root, text="Number of users:").pack(pady=5)
user_count_var = StringVar()
Entry(root, textvariable=user_count_var).pack(pady=5)
 
 
# Detailed information checkbox
detailed_var = IntVar()
Checkbutton(root, text="Generate detailed information", variable=detailed_var).pack(pady=5)
 
 
# Gender selection radio buttons
gender_var = StringVar(value="both")
Label(root, text="Gender:").pack(pady=5)
Radiobutton(root, text="Both", variable=gender_var, value="both").pack(pady=5)
Radiobutton(root, text="Male", variable=gender_var, value="male").pack(pady=5)
Radiobutton(root, text="Female", variable=gender_var, value="female").pack(pady=5)
 
 
# Save to file checkbox
save_var = IntVar()
Checkbutton(root, text="Save to file", variable=save_var).pack(pady=5)
 
 
# File type selection using drop-down menu
Label(root, text="File type (if saving):").pack(pady=5)
file_type_var = StringVar(value="csv")
file_type_menu = OptionMenu(root, file_type_var, "csv", "txt", "csv and txt")
file_type_menu.pack(pady=5)
 
 
# Generate button
Button(root, text="Generate", command=handle_generate).pack(pady=20)
 
 
# Start the Tkinter event loop
root.mainloop()
