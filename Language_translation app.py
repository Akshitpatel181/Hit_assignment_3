import tkinter as tk
import googletrans
import textblob
from tkinter import ttk, messagebox
from tkinter import *
import pyttsx3

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Language Translation App')
        self.root.geometry('900x300')

        def translate_it():
            # Delete any previous translations
            translated_text.delete(1.0, END)
            try:
                # Get languages from Dictionary keys

                # Get the From language key
                for key, value in languages.items():
                    if (value == original_combo.get()):
                        from_language_key = key

                # Get the To language key
                for key, value in languages.items():
                    if (value == translated_combo.get()):
                        to_language_key = key

                # Turn original text into a text blob
                words = textblob.TextBlob(original_text.get(1.0,END))

                # Translate text
                words = words.translate(from_lang=from_language_key, to=to_language_key)

                # Display translated text
                translated_text.insert(1.0, words)

                # Initializing the speech engine
                engine= pyttsx3.init()

                # Pass text to the speech engine
                engine.say(words)

                # Run the engine
                engine.runAndWait()

            except Exception as e:
                messagebox.showerror('Translator', e)

# Clearing text Function
        
        def clear():
            original_text.delete(1.0,END)
            translated_text.delete(1.0,END)

# Take language list from Google trans and put it in the list
        languages= googletrans.LANGUAGES
        language_list = list(languages.values())
        

# Text Boxes and Buttons
        
        original_text = Text(self.root, height =10, width = 40)
        original_text.grid(row = 0, column = 0, pady=20, padx =10)

        translate_button = Button(self.root, text='Translate it!', font=("Helvetica", 24), command=translate_it)
        translate_button.grid(row=0, column= 1, padx=10)
   
        translated_text = Text(self.root, height =10, width = 40)
        translated_text.grid(row = 0, column = 2, pady=20, padx =10)

        clear_button= Button(self.root, text='Clear', font=("Helvetica", 10), command=clear)
        clear_button.grid(row=2, column=1)

# Combo Boxes
        
        original_combo = ttk.Combobox(self.root, width=50, value=language_list)
        original_combo.current(21)  # Show a default language as english
        original_combo.grid(row=1, column=0)

        translated_combo = ttk.Combobox(self.root, width=50, value=language_list)
        translated_combo.current(26)  # Show a default language as english
        translated_combo.grid(row=1, column=2)


        self.root.mainloop()
        return

if __name__ == "__main__":
    App()

