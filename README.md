# AgenticAI Builder

AgenticAI Builder is a graphical application for creating intelligent agents step-by-step. It provides a user-friendly interface to define agent roles, skills, impact metrics, and preview the resulting agent card.

---

## 🧠 Overview

This application allows you to:
- Define a new agent's name, purpose, and description
- Enter core skills using freeform input (add/remove as needed)
- Add custom impact metrics (e.g. "30% Increase in Monitoring")
- Instantly generate a formatted agent summary card

---

## 🖥️ Interface

The graphical interface includes:
- Input fields for name, role, and description
- Freeform skill entry with "Add" and "Remove" controls
- Customizable metric/impact entries
- A real-time preview panel for the agent card

---

## 🚀 Launching the Application

To open AgenticAI Builder, run the following from your terminal:

```bash
python agentic_ai_builder.py
```

This launches the graphical interface. No command-line interaction is required.

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

When you click “Generate Agent Card,” a live preview appears in the panel. You can copy the output for documentation, dashboards, or communication purposes.
