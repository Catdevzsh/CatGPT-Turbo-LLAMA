import tkinter as tk
from tkinter import ttk, simpledialog
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CatGPT 1.0 [Beta] - Local Server 1.0 [C] Flames Labs 20XX")
        self.geometry("600x400")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background="#343541", foreground="white")
        style.configure("TEntry", fieldbackground="#808080")  # Gray color for input box
        style.configure("TButton", background="#444654", foreground="white")
        style.map("TButton", background=[("active", "#565869")])

        self.chat_history = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, bg="#D2B48C", fg="#008000")  # Green color for chat text
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_input = ttk.Entry(input_frame, style="TEntry")
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.LEFT, padx=(10, 0))

        self.bind("<Return>", lambda event: self.send_message())

        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "Assistant: Hello! I'm an intelligent assistant. How may I assist you today?\n\n")
        self.chat_history.configure(state=tk.DISABLED)

    def send_message(self):
        user_message = self.user_input.get()
        self.user_input.delete(0, tk.END)

        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"You: {user_message}\n\n")
        self.chat_history.configure(state=tk.DISABLED)

        history = [
            {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
            {"role": "user", "content": user_message},
        ]
        
        completion = client.chat.completions.create(
            model="LM Studio Community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
        )
        
        assistant_response = completion.choices[0].message.content
        
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"Assistant: {assistant_response}\n\n")
        self.chat_history.configure(state=tk.DISABLED)

        self.chat_history.see(tk.END)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
