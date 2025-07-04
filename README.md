# Smart Troubleshooting Chatbot (Local IT Help Assistant)

**Description**  
A Python-based CLI and Tkinter GUI chatbot that helps users diagnose hardware, software, and network issues using CompTIA A+ knowledge. Combines decision trees, keyword detection, and lightweight AI responses to guide troubleshooting workflows.

---

## Features

- Interactive CLI and Tkinter-based GUI
- Pretrained troubleshooting workflows modeled as decision trees
- Node management via admin GUI (add, edit, delete, stats)
- Modular design with Python OOP and JSON workflow storage

---

## Technologies Used

- Python 3.13+
- Tkinter (standard Python GUI library)
- Natural Language Processing & Decision Tree logic
- JSON for workflow data storage

---

## Installation

```bash
git clone https://github.com/yourusername/smart-troubleshooting-chatbot.git
cd smart-troubleshooting-chatbot

python -m venv venv
# Activate virtual environment:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt  # (Empty or minimal file)
```

---

## Usage

- Run CLI chatbot:

  ```bash
  python engine.py
  ```

- Run user GUI chatbot (Tkinter):

  ```bash
  python gui_main.py
  ```

- Run admin GUI for managing workflow nodes:
  ```bash
  python admin_gui_tk.py
  ```

---

## Project Structure

```
.
├── engine.py            # Core chatbot engine & CLI interface
├── gui_main.py          # User chatbot GUI (Tkinter)
├── admin_gui_tk.py      # Admin GUI for workflow management (Tkinter)
├── workflow_manager.py  # Workflow CRUD operations
├── workflows.json       # Troubleshooting workflows data
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies (minimal)
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

---

## License

MIT License
