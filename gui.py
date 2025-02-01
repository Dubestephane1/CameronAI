from PIL import Image, ImageTk
from tkinter import scrolledtext, messagebox, simpledialog, Toplevel
import datetime
import os
import tkinter as tk

class GUI:
    def __init__(self, root, ai_name, chat_app):
        self.root = root
        self.ai_name = ai_name
        self.chat_app = chat_app
        # Theme colors
        self.themes = {
            "Light": {
                "bg": "white",
                "fg": "black",
                "text_bg": "white",
                "text_fg": "black",
                "button_bg": "lightblue",
                "button_fg": "black",
                "frame_bg": "SystemButtonFace"
            },
            "Dark": {
                "bg": "#1E1E1E",  # Dark charcoal
                "fg": "white",
                "text_bg": "#2C2C2C",  # Slightly lighter dark background
                "text_fg": "white",
                "button_bg": "#4A4A4A",  # Dark gray
                "button_fg": "white",
                "frame_bg": "#3A3A3A"  # Darker gray for dark mode frame
            }
        }
        # Current theme
        self.current_theme = "Light"
        # Rest of the initialization remains the same
        self.root.title(f"Chat with {self.ai_name}")
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculate 99% of screen width and height
        window_width = int(screen_width * 1)
        window_height = int(screen_height * 0.99)
        # Center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        # Set the window geometry
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        # Apply initial theme
        self.apply_theme(self.current_theme)
        self.load_image("C:/Users/dubes/Documents/www/chatbot/Cameron_chat/cameron_profile.jpg")
        self.setup_text_area()
        self.setup_input_field()
        self.text_area.tag_configure("listening", foreground="green")  # Define the tag for green text
        # Add text display speed control
        self.text_display_speed = 1  # milliseconds between characters - DISPLAY SPEED (1 = fast, 10 = slower)
        # Ensure q_a directory exists
        os.makedirs("chat_log", exist_ok=True)
        # Set up window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_text_area(self):
        """ Setup the text area for conversation history."""
        # Calculate text area width as 90% of screen width
        screen_width = self.root.winfo_screenwidth()
        text_area_width = int(screen_width * 0.9 / 10)  # Tkinter's width is in characters, not pixels
        # Create text area with calculated width and theme colors
        self.text_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            width=text_area_width, 
            height=20, 
            font=("Verdana", 13),
            bg=self.themes[self.current_theme]["text_bg"],
            fg=self.themes[self.current_theme]["text_fg"]
        )
        self.text_area.tag_configure("left", justify='left')  # Ensure this is configured
        # Center the text area using pack with padx
        screen_width = self.root.winfo_screenwidth()
        text_area_width_pixels = text_area_width * 10  # Convert character width to pixels
        side_padding = (screen_width - text_area_width_pixels) // 2
        self.text_area.pack(padx=side_padding, pady=10)
        # Create a tag for orange text
        self.text_area.tag_configure("loading_message", foreground="orange", font=("bold"))

    def setup_input_field(self):
        """ Setup the input field for user messages. """
        # Calculate screen and input field dimensions
        screen_width = self.root.winfo_screenwidth()
        input_width = int(screen_width * 0.9)  # 80% of screen width
        # Create main input frame with theme background
        input_frame = tk.Frame(
            self.root, 
            bg=self.themes[self.current_theme]["bg"]
        )
        input_frame.pack(padx=0, pady=10)
        # Calculate side padding to center the entire input area
        side_padding = (screen_width - input_width) // 2
        # Create a frame for buttons with theme background
        button_frame = tk.Frame(
            input_frame, 
            bg=self.themes[self.current_theme]["bg"]
        )
        button_frame.pack(side=tk.LEFT, padx=(0, 10))
        # Voice input button
        self.voice_input_button = tk.Button(
            button_frame, 
            text="Voice Input", 
            command=self.chat_app.handle_voice_input, 
            bg=self.themes[self.current_theme]["button_bg"],
            fg=self.themes[self.current_theme]["button_fg"],
            width=10
        )
        self.voice_input_button.pack(side=tk.TOP, pady=5)
        # Read Aloud button
        self.tts_button = tk.Button(
            button_frame, 
            text="Read Aloud", 
            command=self.read_aloud, 
            bg=self.themes[self.current_theme]["button_bg"],
            fg=self.themes[self.current_theme]["button_fg"],
            width=10
        )
        self.tts_button.pack(side=tk.TOP, pady=5)
        # Calculate remaining width for input field
        button_width = 10  # Matches the button width we set
        text_width = int((input_width - (button_width * 10)) / 10)  # Convert to Tkinter character width
        # Create the input field
        self.input_field = tk.Text(
            input_frame, 
            height=4, 
            wrap=tk.WORD, 
            width=text_width,  # Dynamically calculated width
            font=("Arial", 13),
            bg=self.themes[self.current_theme]["text_bg"],
            fg=self.themes[self.current_theme]["text_fg"]
        )
        self.input_field.pack(side=tk.LEFT)
        # Create a tag for blue text
        self.input_field.tag_configure("user_input", foreground="blue")
        # Chat log button
        self.chat_log_button = tk.Button(
            input_frame, 
            text="View\nChat\nLog", 
            command=self.view_chat_log, 
            bg=self.themes[self.current_theme]["button_bg"], 
            fg=self.themes[self.current_theme]["button_fg"],
            font=("Arial", 12),
            width=10
        )
        self.chat_log_button.pack(side=tk.LEFT, padx=(10, 0))
        # Apply overall side padding to the input frame
        input_frame.pack(padx=side_padding)

    def apply_theme(self, theme):
        # Update current theme
        self.current_theme = theme
        theme_colors = self.themes[theme]
        
        # Centralized method to configure widget colors
        def configure_widget_colors(widget, bg_key='frame_bg', fg_key='fg'):
            """
            Configure widget colors based on theme colors.
            
            :param widget: Tkinter widget to configure
            :param bg_key: Key for background color in theme_colors
            :param fg_key: Key for foreground color in theme_colors
            """
            if widget:
                widget.configure(
                    bg=theme_colors[bg_key], 
                    fg=theme_colors[fg_key]
                )
        
        # Recursively update colors for all widgets
        def update_widget_colors(widget):
            # Update frame colors
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme_colors["frame_bg"])
            
            # Update label colors
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme_colors["frame_bg"])
            
            # Update button colors
            if isinstance(widget, tk.Button):
                widget.configure(
                    bg=theme_colors["button_bg"], 
                    fg=theme_colors["button_fg"]
                )
            
            # Update text widgets and input fields
            if isinstance(widget, (tk.Text, tk.Entry)):
                configure_widget_colors(
                    widget, 
                    bg_key='text_bg', 
                    fg_key='text_fg'
                )
            
            # Recursively update child widgets
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    update_widget_colors(child)
        
        # Apply theme to root window and all its children
        update_widget_colors(self.root)
        
        # Update root window background
        self.root.configure(bg=theme_colors["bg"])
        
        # Text area and input field theming (if they exist)
        configure_widget_colors(
            getattr(self, 'text_area', None), 
            bg_key='text_bg', 
            fg_key='text_fg'
        )
        configure_widget_colors(
            getattr(self, 'input_field', None), 
            bg_key='text_bg', 
            fg_key='text_fg'
        )

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = "Dark" if self.current_theme == "Light" else "Light"
        self.apply_theme(new_theme)

    def insert_loading_message(self):
        """ Insert a loading message while the AI is processing. """
        self.text_area.delete('1.0', tk.END)  # Clear previous messages
        self.insert_text("The AI is loading, please wait ...\n", "loading_message")  # Apply the orange tag

    def activate_voice_input(self):
        """ Activate voice input and insert the recognized text into the input field. """
        self.chat_app.handle_voice_input()  # Ensure this is correctly referencing the ChatApp instance

    def get_last_ai_response(self):
        """ Retrieve the last AI response from the conversation history. """
        for entry in reversed(self.conversation_history):
            if entry['role'] == 'assistant':
                return entry['content']
        return None
        
    def read_aloud(self):
        """ Read only the last AI response aloud. """
        # Get the last line or last AI response from the text area
        text_to_read = self.text_area.get('1.0', tk.END).strip().split('\n')[-1]
        # If no text, show a message
        if not text_to_read:
            messagebox.showinfo("Read Aloud", "No text available to read.")
            return
        # Check if text-to-speech engine is available
        try:
            if not hasattr(self, 'engine'):
                import pyttsx3
                self.engine = pyttsx3.init()
            # Get available voices
            voices = self.engine.getProperty('voices')
            # Prioritize finding a female voice
            female_voices = [
                voice for voice in voices 
                if 'female' in voice.name.lower() or 'microsoft zira' in voice.name.lower()
            ]
            # Set voice preference
            if female_voices:
                # Use the first female voice found
                self.engine.setProperty('voice', female_voices[0].id)
            elif len(voices) > 1:
                # If no female voice, use the second voice (typically female on many systems)
                self.engine.setProperty('voice', voices[1].id)
            self.engine.setProperty('rate', 185)  # Adjust the speech rate
            self.engine.say(text_to_read)
            self.engine.runAndWait()
        except ImportError:
            messagebox.showerror("Error", "Text-to-speech library (pyttsx3) not installed.")
        except Exception as e:
            messagebox.showerror("Read Aloud Error", f"Could not read text aloud: {str(e)}")

    def get_text_since_last_user_question(self):
        """ Retrieve the last AI response :return: Text to be read aloud """
        # Check if conversation_history exists and is not empty
        if not hasattr(self, 'conversation_history') or not self.conversation_history:
            return None
        # Find the last AI response
        for entry in reversed(self.conversation_history):
            if entry['role'] == 'assistant':
                return entry['content']
        return None

    def view_chat_log(self):
        """ Open a previous chat log file in the default text editor. """
        log_directory = r"C:\Users\dubes\Documents\www\chatbot\Cameron_chat\chat_log"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        chat_logs = [f for f in os.listdir(log_directory) if f.endswith('.txt')]
        if not chat_logs:
            messagebox.showinfo("Info", "No chat log files found.")
            return
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Chat Log")
        # Get screen width and height
        screen_width = selection_window.winfo_screenwidth()
        screen_height = selection_window.winfo_screenheight()
        # Set window size
        window_width = 200
        window_height = 350
        # Calculate position to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        # Set window size and position
        selection_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        listbox = tk.Listbox(
            selection_window, 
            width=50, 
            height=15, 
            font=("Arial", 12)  # Increase font size
        )
        listbox.pack(padx=10, pady=10)
        for log in chat_logs:
            listbox.insert(tk.END, log)
        def open_selected_log():
            selected_index = listbox.curselection()
            if selected_index:
                chat_log_file = chat_logs[selected_index[0]]
                chat_log_path = os.path.join(log_directory, chat_log_file)
                os.startfile(chat_log_path)
                selection_window.destroy()
            else:
                messagebox.showinfo("Info", "Please select a chat log file.")
        select_button = tk.Button(selection_window, text="Open Selected Log", command=open_selected_log)
        select_button.pack(pady=10)

    def load_image(self, image_path):
        """ Load and display an image. """
        try:
            # Open the original image
            original_image = Image.open(image_path)
            # Calculate the width based on the text area
            screen_width = self.root.winfo_screenwidth()
            text_area_width = int(screen_width * 0.9)  # 90% of screen width in pixels
            # Calculate the height while maintaining aspect ratio
            width_ratio = text_area_width / original_image.width
            new_height = int(original_image.height * (width_ratio*0.667)) # Prevent the image to be too high (can play with it, like 0.5 to 0.9)
            # Resize the image
            resized_image = original_image.resize((text_area_width, new_height), Image.LANCZOS)
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized_image)
            # Create a frame to center the image
            image_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["frame_bg"])
            image_frame.pack(pady=(10, 10))
            # Calculate side padding to center the image
            side_padding = (screen_width - text_area_width) // 2
            # Create label with the image
            label = tk.Label(image_frame, image=photo, bg=self.themes[self.current_theme]["frame_bg"])
            label.image = photo  # Keep a reference to avoid garbage collection
            label.pack(padx=side_padding)
        except Exception as e:
            print(f"Error loading image: {e}")

    def auto_scroll_text_area(self):
        """ Automatically scroll to the end of the text area. """
        self.text_area.see(tk.END)

    def insert_text(self, text, tag=None):
        """ Insert text into the text area and auto-scroll. """
        if tag:
            self.text_area.insert(tk.END, text, tag)
        else:
            self.text_area.insert(tk.END, text)
        self.auto_scroll_text_area()

    def insert_with_typing_effect(self, text, tag=None, speed=1):
        if speed is None:
            speed = self.text_display_speed
        self.text_area.delete('1.0', tk.END)
        def type_text(index=0):
            if index < len(text):
                current_text = text[:index+1]
                self.text_area.delete('1.0', tk.END)
                if tag:
                    self.text_area.insert(tk.END, current_text, tag)
                else:
                    self.text_area.insert(tk.END, current_text)
                self.text_area.see(tk.END)
                self.root.after(speed, type_text, index + 1)
            else:
                # Ensure final scroll after typing is complete
                self.auto_scroll_text_area()
        type_text()

    def on_closing(self):
        """ Handle the window closing event and save the chat log. """
        chat_log = self.text_area.get("1.0", tk.END)
        log_dir = r"C:\Users\dubes\Documents\www\chatbot\Cameron_chat\chat_log"
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y_%b_%d')}.txt"), "a", encoding='utf-8') as f:
            f.write(chat_log + "\n\n")
        self.root.destroy()
