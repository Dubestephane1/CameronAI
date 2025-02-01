from ai_handler import AIHandler
from constants import AI_MODEL, USER_NAME, AI_NAME, THEMES
from datetime import datetime
from gui import GUI
from voice import VoiceHandler
import os
import pyttsx3
import speech_recognition as sr
import tkinter as tk

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.gui = GUI(root, AI_NAME, self)
        self.ai = AIHandler(AI_MODEL, self.gui.text_area)
        self.voice = VoiceHandler(self)
        self.user_name = USER_NAME
        self.ai_name = AI_NAME
        self.conversation_history = []
        self.engine = pyttsx3.init()  # Initialize TTS engine
        self.setup_buttons()
        self.setup_controls()
        self.welcome_message_printed = False
        self.gui.insert_loading_message()  # Call the method from the GUI
        self.root.after(5000, self.clear_loading_message)  # Adjust this timing as needed
        # Create a tag for blue text in the chat area
        self.gui.text_area.tag_configure("user_input", foreground="blue")

    def setup_buttons(self):
        """ Setup buttons for sending messages, voice input, and reading aloud. """
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)
        # Send button frame
        send_button_frame = tk.Frame(self.root)
        send_button_frame.pack(pady=10)
        self.send_button = tk.Button(send_button_frame, text="Send", command=self.send_user_message, height=2, width=10, bg="green", fg="white", font=("Arial", 12, "bold"))
        self.send_button.pack(side=tk.LEFT, padx=10)

    def setup_controls(self):
        """ Setup controls including theme selection and clear chat button. """
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        self.theme_var = tk.StringVar(value=THEMES[0])
        theme_menu = tk.OptionMenu(control_frame, self.theme_var, *THEMES, command=self.toggle_theme)
        theme_menu.pack(side=tk.LEFT, padx=5)
        clear_button = tk.Button(control_frame, text="Clear", command=self.clear_chat, bg="orange")
        clear_button.pack(side=tk.LEFT, padx=10)

    def clear_loading_message(self):
        """ Clear the loading message and insert the welcome message. """
        self.gui.text_area.delete('1.0', tk.END)  # Clear the loading message
        self.insert_welcome_message()  # Insert the first chat message

    def insert_welcome_message(self):
        """ Insert a welcome message from the AI."""
        if not self.welcome_message_printed:
            welcome_message = f"{self.ai_name}: Hello {self.user_name}!"
            self.gui.text_area.insert(tk.END, welcome_message)
            self.conversation_history.append({"role": "assistant", "content": welcome_message.strip()})
            self.welcome_message_printed = True
            self.gui.text_area.see(tk.END)

    def send_user_message(self, recognized_text=None):
        """ Send the user message to the AI."""
        if recognized_text is not None:
            user_input = recognized_text  # Use the recognized text if provided
        else:
            user_input = self.gui.input_field.get("1.0", tk.END).strip()  # Get input from the GUI
        if user_input:
            self.gui.text_area.insert(tk.END, f"\n\n({self.user_name}) {user_input}\n", "user_input")
            self.conversation_history.append({"role": "user", "content": user_input})
            # Check if the user input is a simple "yes" or "no"
            if user_input.lower() in ["yes", "no"]:
                # Retrieve the last AI question from the conversation history
                last_ai_question = None
                for entry in reversed(self.conversation_history):
                    if entry['role'] == 'assistant':
                        last_ai_question = entry['content']
                        break
                if last_ai_question:
                    # Pass the last AI question along with the user's response
                    self.ai.stream_response([last_ai_question, user_input])
            else:
                # Only pass the last user question to the AI
                if len(self.conversation_history) > 1:
                    last_user_question = self.conversation_history[-1]
                    self.ai.stream_response([last_user_question])
                else:
                    self.ai.stream_response(self.conversation_history)
            # After receiving the AI response, append to the chat log
            self.append_to_chat_log(user_input)
            self.gui.input_field.delete("1.0", tk.END)

    def append_to_chat_log(self, user_input):
        """ Append the user input and AI response to the chat log."""
        # Define the directory for the chat log
        log_directory = os.path.join("Cameron_chat", "chat_log")
        os.makedirs(log_directory, exist_ok=True)  # Create the directory if it doesn't exist
        # Define the log file path
        log_file_path = os.path.join(log_directory, "chat_log.txt")
        # Append the user input and AI response to the log file
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"User: {user_input}\n")
            last_ai_response = self.get_last_ai_response()
            if last_ai_response:
                log_file.write(f"AI: {last_ai_response}\n")

    def handle_voice_input(self):
        """ Handle voice input using the VoiceHandler class."""
        self.voice.listen_for_voice(self.send_user_message)  # Ensure this method exists in VoiceHandler

    def get_last_ai_response(self):
        """ Retrieve the last AI response from the conversation history."""
        for entry in reversed(self.conversation_history):
            if entry['role'] == 'assistant':
                return entry['content']
        return None

    def get_text_since_last_user_question(self):
        """ Retrieve all text from the last user question to the last AI response."""
        conversation_text = ""
        user_found = False
        # Iterate through the conversation history in reverse
        for entry in reversed(self.conversation_history):
            print(f"Checking entry: {entry}")  # Debugging output
            if entry['role'] == 'user':
                user_found = True  # Mark that we found the last user question
                break
            if entry['role'] == 'assistant':
                conversation_text = entry['content'] + "\n" + conversation_text  # Prepend AI response
        # If a user question was found, return only the AI responses
        if user_found:
            print(f"Text to read: {conversation_text.strip()}")  # Debugging output
            return conversation_text.strip()
        return None

    def toggle_theme(self, theme):
        # Update the GUI's current theme and apply it
        self.gui.apply_theme(theme)

    def clear_chat(self):
        self.gui.text_area.delete("1.0", tk.END)
        self.conversation_history.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
