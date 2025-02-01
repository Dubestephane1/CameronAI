import ollama
import re
import threading
import tkinter as tk

class AIHandler:
    def __init__(self, model, text_area):
        self.model = model
        self.text_area = text_area  # Store the text_area for later use

    def stream_response(self, conversation):
        """ Stream the response from the AI model in a separate thread. """
        def stream_task():
            # When stream=True, iterate through response chunks
            full_text = ""
            for chunk in ollama.chat(model=self.model, messages=conversation, stream=True):
                # Accumulate text from each chunk
                if isinstance(chunk, dict):
                    text_chunk = chunk.get('message', {}).get('content', '')
                else:
                    text_chunk = str(chunk)
                full_text += text_chunk
                # Process each chunk (optional: you can comment this out if you want to process only at the end)
                self.process_buffer(text_chunk)
            # Remove <think> tags from the full text
            full_text = re.sub(r'<\s*think\s*>.*?<\s*/\s*think\s*>', '', full_text, flags=re.DOTALL)
        # Start the task in a separate thread
        threading.Thread(target=stream_task, daemon=True).start()

    def process_buffer(self, text):
        """ Process the buffered response text and insert into the GUI text area."""
        # Remove text between <think> and </think> tags
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        # Insert text directly into the GUI text area
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)  # Scroll to the end
        self.text_area.update_idletasks()  # Ensure the GUI updates

    def get_response(self, user_input):
        """ Generate a response based on user input."""
        # This is a placeholder for actual AI response logic
        response = f"AI response to: {user_input}"  # Replace with actual AI logic
        return response
