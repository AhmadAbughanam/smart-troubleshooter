import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import datetime
import threading
from chatbot.engine import ChatbotEngine

class ModernChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.engine = ChatbotEngine()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_bindings()
        self.add_welcome_message()
        self.update_time()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🤖 Smart Troubleshooting Assistant")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        self.root.configure(bg='#2C3E50')
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
        
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'chat_bg': '#FFFFFF',
            'input_bg': '#ECF0F1',
            'button_primary': '#3498DB',
            'button_success': '#27AE60',
            'button_warning': '#F39C12',
            'button_danger': '#E74C3C',
            'accent': '#9B59B6'
        }
        
        # Configure button styles with map for hover effects
        style.configure('Primary.TButton',
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', '#2980B9'), ('!active', self.colors['button_primary'])],
                 foreground=[('active', 'white'), ('!active', 'white')])
        
        style.configure('Success.TButton',
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        style.map('Success.TButton',
                 background=[('active', '#219A52'), ('!active', self.colors['button_success'])],
                 foreground=[('active', 'white'), ('!active', 'white')])
        
        style.configure('Warning.TButton',
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        style.map('Warning.TButton',
                 background=[('active', '#E67E22'), ('!active', self.colors['button_warning'])],
                 foreground=[('active', 'white'), ('!active', 'white')])
        
        style.configure('Danger.TButton',
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        style.map('Danger.TButton',
                 background=[('active', '#C0392B'), ('!active', self.colors['button_danger'])],
                 foreground=[('active', 'white'), ('!active', 'white')])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['bg'],
                       relief='solid',
                       borderwidth=1)
        
    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Chat area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Button area
        self.create_button_area(main_frame)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'], height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🤖 Smart Troubleshooting Assistant",
                              font=('Helvetica', 20, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['fg'])
        title_label.pack(expand=True)
        
        # Separator
        separator = tk.Frame(parent, height=2, bg=self.colors['accent'])
        separator.pack(fill='x', pady=(0, 10))
        
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg'])
        status_frame.pack(fill='x', pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(status_frame,
                                    text="Status: Ready",
                                    font=('Helvetica', 10),
                                    bg=self.colors['bg'],
                                    fg='#2ECC71')
        self.status_label.pack(side='left')
        
        # Time label
        self.time_label = tk.Label(status_frame,
                                  text="",
                                  font=('Helvetica', 10),
                                  bg=self.colors['bg'],
                                  fg='#BDC3C7')
        self.time_label.pack(side='right')
        
    def create_chat_area(self, parent):
        """Create the chat display area"""
        # Chat frame
        chat_frame = tk.LabelFrame(parent,
                                  text="  💬 Conversation  ",
                                  font=('Helvetica', 12, 'bold'),
                                  bg=self.colors['bg'],
                                  fg=self.colors['fg'],
                                  bd=2,
                                  relief='solid')
        chat_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(chat_frame,
                                                     wrap=tk.WORD,
                                                     font=('Consolas', 11),
                                                     bg=self.colors['chat_bg'],
                                                     fg='#2C3E50',
                                                     state='disabled',
                                                     borderwidth=0,
                                                     highlightthickness=0)
        self.chat_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure text tags for different message types
        self.chat_display.tag_configure('user', foreground='#2980B9', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_configure('bot', foreground='#E74C3C', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_configure('timestamp', foreground='#7F8C8D', font=('Consolas', 9))
        
    def create_input_area(self, parent):
        """Create the input area"""
        input_frame = tk.LabelFrame(parent,
                                   text="  ✍️ Your Message  ",
                                   font=('Helvetica', 12, 'bold'),
                                   bg=self.colors['bg'],
                                   fg=self.colors['fg'],
                                   bd=2,
                                   relief='solid')
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Input text area
        self.input_text = tk.Text(input_frame,
                                 height=3,
                                 font=('Helvetica', 11),
                                 bg=self.colors['input_bg'],
                                 fg='#2C3E50',
                                 wrap=tk.WORD,
                                 borderwidth=0,
                                 highlightthickness=1,
                                 highlightcolor=self.colors['button_primary'])
        self.input_text.pack(fill='x', padx=5, pady=5)
        
        # Tip label
        tip_label = tk.Label(input_frame,
                            text="💡 Tip: Press Enter to send, Shift+Enter for new line",
                            font=('Helvetica', 9, 'italic'),
                            bg=self.colors['bg'],
                            fg='#7F8C8D')
        tip_label.pack(anchor='w', padx=5, pady=(0, 5))
        
    def create_button_area(self, parent):
        """Create the button area"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill='x')
        
        # Send button
        self.send_button = ttk.Button(button_frame,
                                     text="📤 Send Message",
                                     style='Primary.TButton',
                                     command=self.send_message)
        self.send_button.pack(side='left', padx=(0, 10))
        
        # Clear button
        self.clear_button = ttk.Button(button_frame,
                                      text="🗑️ Clear Chat",
                                      style='Warning.TButton',
                                      command=self.clear_chat)
        self.clear_button.pack(side='left', padx=(0, 10))
        
        # Export button
        self.export_button = ttk.Button(button_frame,
                                       text="💾 Export Chat",
                                       style='Success.TButton',
                                       command=self.export_chat)
        self.export_button.pack(side='left', padx=(0, 10))
        
        # Exit button
        self.exit_button = ttk.Button(button_frame,
                                     text="❌ Exit",
                                     style='Danger.TButton',
                                     command=self.exit_application)
        self.exit_button.pack(side='right')
        
    def setup_bindings(self):
        """Setup keyboard bindings"""
        # Bind Enter key to send message
        self.input_text.bind('<Return>', self.on_enter_key)
        self.input_text.bind('<Control-Return>', self.on_ctrl_enter)
        
        # Other shortcuts
        self.root.bind('<Control-l>', lambda e: self.clear_chat())
        self.root.bind('<Control-q>', lambda e: self.exit_application())
        
        # Focus on input when window is clicked
        self.root.bind('<Button-1>', lambda e: self.input_text.focus_set())
        
    def on_enter_key(self, event):
        """Handle Enter key press"""
        # Check if Shift is held (for new line)
        if event.state & 0x1:  # Shift key
            return  # Allow normal newline
        else:
            # Send message
            self.send_message()
            return 'break'  # Prevent default newline
            
    def on_ctrl_enter(self, event):
        """Handle Ctrl+Enter key press"""
        self.send_message()
        return 'break'
        
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_msg = "Hello! I'm your Smart Troubleshooting Assistant. How can I help you today?"
        self.add_message("Bot", welcome_msg)
        
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Add sender and message
        if sender == "You":
            self.chat_display.insert(tk.END, f"👤 You: ", 'user')
        else:
            self.chat_display.insert(tk.END, f"🤖 Bot: ", 'bot')
            
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        
    def send_message(self):
        """Send message and get response"""
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return
            
        # Add user message
        self.add_message("You", message)
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Update status
        self.update_status("Processing...", '#F39C12')
        
        # Disable send button
        self.send_button.config(state='disabled')
        
        # Process in separate thread to avoid blocking GUI
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        """Process message in separate thread"""
        try:
            response = self.engine.respond(message)
            self.root.after(0, self.handle_response, response)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, self.handle_response, error_msg)
            
    def handle_response(self, response):
        """Handle bot response in main thread"""
        self.add_message("Bot", response)
        self.update_status("Ready", '#2ECC71')
        self.send_button.config(state='normal')
        self.input_text.focus_set()
        
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state='normal')
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state='disabled')
        self.add_welcome_message()
        
    def export_chat(self):
        """Export chat to text file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                chat_content = self.chat_display.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(chat_content)
                messagebox.showinfo("Success", f"Chat exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export chat: {str(e)}")
            
    def update_status(self, message, color):
        """Update status message"""
        self.status_label.config(text=f"Status: {message}", fg=color)
        
    def update_time(self):
        """Update time display"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Time: {current_time}")
        self.root.after(1000, self.update_time)  # Update every second
        
    def exit_application(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
            
    def run(self):
        """Run the application"""
        self.input_text.focus_set()  # Focus on input field
        self.root.mainloop()

def main():
    app = ModernChatbotGUI()
    app.run()

if __name__ == '__main__':
    main()