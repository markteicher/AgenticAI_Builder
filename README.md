# AgenticAI Builder

AgenticAI Builder is a graphical application for creating intelligent agents step-by-step. It provides a user-friendly interface to define agent roles, skills, impact metrics, and preview the resulting agent card.

---

## 🧠 Overview

This application allows you to:
- Define a new agent's name, purpose, and description
- Select core skills from a predefined list
- Add custom impact metrics (e.g. "30% Increase in Monitoring")
- Instantly generate a formatted agent summary card

---

## 🖥️ Interface

The graphical interface includes:
- Input fields for name, role, and description
- Checkboxes for core skills
- Customizable metric/impact entries
- A real-time preview panel for the agent card

---

## 🚀 Running the App

To start the application:

```bash
python main.py
```

This will launch the GUI window where you can build agents visually.

---

## 📦 Requirements

Install the required libraries with:

```bash
pip install -r requirements.txt
```

### `requirements.txt` includes:

```text
tk
```

_Tkinter comes pre-installed with standard Python distributions. No additional GUI frameworks are required._

---

## 📤 Output

When you click “Generate Agent Card”, a live preview appears in the right panel. You can copy the output for documentation, dashboards, or communication purposes.

