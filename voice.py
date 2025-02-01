import speech_recognition as sr
import tkinter as tk

class VoiceHandler:
    def __init__(self, gui):
        self.recognizer = sr.Recognizer()  # Initialize the recognizer
        self.gui = gui  # Store the GUI reference

    def _activate_voice_input(self):
        """Internal method to handle voice input in a separate thread."""
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)  # Listen for audio input
        try:
            voice_input = self.recognizer.recognize_google(audio)  # Recognize speech using Google API
            # Insert the recognized text into the input field
            self.gui.input_field.insert(tk.END, voice_input, "user_input")  # Insert the recognized text with the blue tag
            self.send_user_message()  # Optionally send the message after recognition
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def start_listening(self, callback):
        # Implement the logic to start listening for voice input
        # Once the input is recognized, call the callback function
        recognized_text = "Sample recognized text"  # Replace with actual recognition logic
        callback(recognized_text)

    def listen_for_voice(self, callback):
        """Start listening for voice input and call the callback with the recognized text."""
        self.gui.gui.text_area.insert(tk.END, "Listening...\n", "user_input")  # Access text_area through gui
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            try:
                recognized_text = self.recognizer.recognize_google(audio)
                self.gui.gui.text_area.insert(tk.END, f"Recognized: {recognized_text}\n", "user_input")  # Show recognized text
                callback(recognized_text)  # Call the callback with the recognized text
            except sr.UnknownValueError:
                self.gui.gui.text_area.insert(tk.END, "Could not understand audio\n", "user_input")
            except sr.RequestError as e:
                self.gui.gui.text_area.insert(tk.END, f"Could not request results from Google Speech Recognition service; {e}\n", "user_input")
