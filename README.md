# 🤖 **Smart Troubleshooting Chatbot**  
**Local IT Help Assistant — CLI + GUI**

A Python-based chatbot that helps users diagnose hardware, software, and network issues using CompTIA A+ knowledge. Combines decision trees, keyword detection, and lightweight AI responses to guide troubleshooting workflows.

> 🧠 Built for IT support, tech learners, and helpdesk automation — with both CLI and GUI interfaces.

---

## 🚀 Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 💬 **Interactive CLI & GUI**   | Use via terminal or Tkinter-based desktop interface                         |
| 🌳 **Decision Tree Workflows** | Pretrained troubleshooting paths modeled as decision trees                  |
| 🛠️ **Admin GUI**               | Add/edit/delete nodes, view stats, manage workflows                         |
| 🧩 **Modular Design**          | Python OOP architecture with JSON-based workflow storage                    |

---

## 🛠️ Technologies Used

| Component       | Technology                     |
|----------------|---------------------------------|
| **Language**    | Python 3.13+                    |
| **GUI**         | Tkinter (built-in Python GUI)   |
| **Logic**       | Decision Trees, NLP             |
| **Storage**     | JSON for workflow data          |

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/smart-troubleshooting-chatbot.git
cd smart-troubleshooting-chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

> ⚠️ `requirements.txt` is minimal — most dependencies are built-in.

---

## ▶️ Usage

| Mode        | Command                          |
|-------------|----------------------------------|
| 🖥️ CLI Chatbot | `python engine.py`              |
| 🪟 User GUI   | `python gui_main.py`             |
| 🧑‍💼 Admin GUI  | `python admin_gui_tk.py`         |

---

## 📁 Project Structure

```
.
├── engine.py            # Core chatbot engine & CLI interface
├── gui_main.py          # User chatbot GUI (Tkinter)
├── admin_gui_tk.py      # Admin GUI for workflow management
├── workflow_manager.py  # Workflow CRUD operations
├── workflows.json       # Troubleshooting workflows data
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open issues or submit pull requests to improve features, workflows, or UI.

---

## 📃 License

Licensed under the **MIT License** — free to use, modify, and distribute.

---

