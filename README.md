# AgenticAI Builder

## Overview
**AgenticAI Builder** is a graphical application that allows users to visually define and configure AI agents. Users can specify the agent’s name, description, skills, impact metrics, and optionally toggle display and execute buttons for each agent card.

## Features

- Input **Agent Name** (letters and spaces only, cannot be empty)
- Input **Agent Description** (letters and spaces only, max 60 characters)
- Add up to **5 Skills** (letters and spaces only, max 20 characters per skill)
- Add up to **3 Metrics** (letters and spaces only, max 20 characters per metric)
- Upload an **Agent Image** (`.jpeg` or `.png`) that auto-fits the 150x150 display area
- **Display toggle**: ON shows the Display button, OFF hides it
- **Execute toggle**: ON shows the Execute button, OFF hides it
- Real-time **validation feedback** (invalid fields highlight in red)

## Usage

1. Launch the application:
   - Double-click `agentic_ai_builder.py` or open it via your Python environment.
2. Fill in the **Agent Name** and **Description**.
3. Use **Add Skill** and **Remove Skill** buttons to define up to 5 skills.
4. Use **Add Metric** and **Remove Metric** buttons to define up to 3 metrics.
5. Upload an image for the agent (JPEG or PNG). The image will automatically fit into the preview area.
6. Use **Display** and **Execute** toggles to show/hide the respective buttons.
7. The agent card will be generated and displayed in the preview area.

## Validation Rules

- **Agent Name**
  - Must contain letters and spaces only
  - Cannot be empty
  - Turns red if invalid
- **Agent Description**
  - Letters and spaces only
  - Maximum 60 characters
  - Turns red if invalid
- **Skills**
  - Letters and spaces only
  - Maximum 20 characters per skill
  - Maximum 5 skills
  - Turns red if invalid
- **Metrics**
  - Letters and spaces only
  - Maximum 20 characters per metric
  - Maximum 3 metrics
  - Turns red if invalid
- **Agent Image**
  - JPEG or PNG only
  - Auto-fits 150x150 display area

## Notes

- This is a **GUI-only application**; no backend execution or API calls are implemented.
- All fields provide **real-time visual feedback** to ensure input validity.
- Designed for **cross-platform use** (Windows, macOS, Linux) with Python and Tkinter.
