# AgenticAI_Builder


AgenticAI Builder is a flexible, no-code/low-code visual card generator for creating customized agent profiles. This framework lets users upload an image, input agent text, define up to five core skills, and set up to three KPI-style metrics — all wrapped into a single, styled PNG output with optional action buttons (`Details`, `Execute`).

## 🔧 Features

- Upload `.png` or `.jpeg` agent image
- Input agent name and rich text description
- Define **up to 5** core skills
- Enter **up to 3** metrics (KPI-style or custom)
- Toggle **Details** button on/off
- Auto-generate PNG visual card output
- Streamlit interface for fast interaction
- Lightweight and extensible Python backend

---

## 📂 Directory Structure
AgenticAI_Builder/
│
├── app/
│   ├── main.py             # Streamlit frontend
│   ├── generator.py        # Image generation logic
│   └── assets/
│       └── Roboto-Bold.ttf # Font file
│
├── output/                 # Generated PNG files
│
└── README.md               # Project info
