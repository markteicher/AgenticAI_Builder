import tkinter as tk
from tkinter import ttk, messagebox


class AgenticAIGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AgenticAI Builder")
        self.geometry("700x600")
        self.configure(padx=20, pady=20)

        self._build_form()
        self._build_preview()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self, text="Define Your Agent")
        form_frame.pack(fill="x", padx=5, pady=10)

        # Agent Name
        ttk.Label(form_frame, text="Agent Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.agent_name = ttk.Entry(form_frame, width=40)
        self.agent_name.grid(row=0, column=1, pady=5)

        # Agent Purpose
        ttk.Label(form_frame, text="Agent Role/Purpose:").grid(row=1, column=0, sticky="w", pady=5)
        self.agent_purpose = ttk.Entry(form_frame, width=60)
        self.agent_purpose.grid(row=1, column=1, pady=5)

        # Description
        ttk.Label(form_frame, text="Agent Description:").grid(row=2, column=0, sticky="nw", pady=5)
        self.agent_description = tk.Text(form_frame, width=60, height=4)
        self.agent_description.grid(row=2, column=1, pady=5)

        # Core Skills
        ttk.Label(form_frame, text="Core Skills:").grid(row=3, column=0, sticky="nw", pady=5)
        self.skill_vars = {}
        skills = ["Network Security", "Vulnerability Management", "Threat Intelligence", "Asset Discovery"]
        skill_frame = tk.Frame(form_frame)
        skill_frame.grid(row=3, column=1, sticky="w", pady=5)
        for skill in skills:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(skill_frame, text=skill, variable=var)
            cb.pack(anchor="w")
            self.skill_vars[skill] = var

        # Impact Metrics
        ttk.Label(form_frame, text="Impact Metrics:").grid(row=4, column=0, sticky="nw", pady=5)
        self.impact_entries = []
        impact_frame = tk.Frame(form_frame)
        impact_frame.grid(row=4, column=1, sticky="w", pady=5)

        for i in range(3):
            metric_entry = ttk.Entry(impact_frame, width=20)
            label_entry = ttk.Entry(impact_frame, width=40)
            metric_entry.grid(row=i, column=0, padx=5, pady=2)
            label_entry.grid(row=i, column=1, padx=5, pady=2)
            self.impact_entries.append((metric_entry, label_entry))

        # Generate Button
        ttk.Button(self, text="Generate Agent Card", command=self.generate_card).pack(pady=10)

    def _build_preview(self):
        preview_frame = ttk.LabelFrame(self, text="Agent Card Preview")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=10)

        self.preview_text = tk.Text(preview_frame, wrap="word", state="disabled", height=15)
        self.preview_text.pack(fill="both", expand=True)

    def generate_card(self):
        name = self.agent_name.get().strip()
        purpose = self.agent_purpose.get().strip()
        description = self.agent_description.get("1.0", "end").strip()

        if not name or not purpose:
            messagebox.showwarning("Missing Info", "Agent Name and Purpose are required.")
            return

        skills = [k for k, v in self.skill_vars.items() if v.get()]
        impact_lines = []
        for metric_entry, label_entry in self.impact_entries:
            metric = metric_entry.get().strip()
            label = label_entry.get().strip()
            if metric and label:
                impact_lines.append(f"{metric} {label}")

        # Build the card text
        card = f"👤 **{name}**\n\n"
        card += f"🧠 {purpose}\n\n"
        card += f"{description}\n\n" if description else ""
        if skills:
            card += f"🔧 Core Skills: {', '.join(skills)}\n\n"
        if impact_lines:
            card += "📊 Projected Agent Impact:\n"
            for line in impact_lines:
                card += f"  • {line}\n"

        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", card)
        self.preview_text.configure(state="disabled")


if __name__ == "__main__":
    app = AgenticAIGUI()
    app.mainloop()
