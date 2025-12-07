from tkinter import Tk, Label, Entry, Text, Button, Frame, filedialog, IntVar, Canvas, Checkbutton, LEFT, RIGHT, BOTH, X
from PIL import Image, ImageTk

MAX_SKILLS = 5
MAX_METRICS = 3
IMAGE_WIDTH = 150
IMAGE_HEIGHT = 150
DESCRIPTION_MAX = 60
SKILL_MAX = 20
METRIC_MAX = 20

class AgenticAIBuilder:
def __init__(self, root):
self.root = root
self.root.title("AgenticAI Builder")

self.skills = []
self.metrics = []
self.agent_image = None
self.display_button = None
self.execute_button = None

self._build_ui()

def _build_ui(self):
# Top frame for image + name/description
top_frame = Frame(self.root)
top_frame.pack(fill=X, pady=10)

# Image section
image_section = Frame(top_frame)
image_section.pack(side=LEFT, padx=10)
self.image_canvas = Canvas(image_section, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, bg="lightgray")
self.image_canvas.pack()
Button(image_section, text="Upload Agent Image", command=self.upload_image).pack(pady=5)

# Name and description section
info_section = Frame(top_frame)
info_section.pack(side=RIGHT, fill=BOTH, expand=True)
Label(info_section, text="Agent Name:").pack(anchor="w")
self.agent_name = Entry(info_section, width=40)
self.agent_name.pack(fill=X, padx=5)
self.agent_name.bind("<KeyRelease>", lambda e: self.validate_letters_only(self.agent_name, allow_empty=False))

Label(info_section, text="Agent Description:").pack(anchor="w")
self.agent_description = Text(info_section, height=4, width=40)
self.agent_description.pack(fill=X, padx=5)
self.agent_description.bind("<KeyRelease>", lambda e: self.validate_text_limit(self.agent_description, DESCRIPTION_MAX))

# Skills
Label(self.root, text="Skills:").pack()
self.skills_frame = Frame(self.root)
self.skills_frame.pack()
Button(self.root, text="Add Skill", command=self.add_skill).pack()
Button(self.root, text="Remove Skill", command=self.remove_skill).pack()

# Metrics
Label(self.root, text="Metrics:").pack()
self.metrics_frame = Frame(self.root)
self.metrics_frame.pack()
Button(self.root, text="Add Metric", command=self.add_metric).pack()
Button(self.root, text="Remove Metric", command=self.remove_metric).pack()

# Toggles
self.display_on = IntVar()
self.execute_on = IntVar()
Checkbutton(self.root, text="Toggle Display Button", variable=self.display_on, command=self.toggle_display).pack()
Checkbutton(self.root, text="Toggle Execute Button", variable=self.execute_on, command=self.toggle_execute).pack()

# ---------------------------
# Validation Methods
# ---------------------------
def validate_letters_only(self, entry_widget, allow_empty=True):
text = entry_widget.get() if isinstance(entry_widget, Entry) else entry_widget.get("1.0", "end-1c")
if (not text and not allow_empty) or (any(not c.isalpha() and c != ' ' for c in text)):
self.set_widget_red(entry_widget)
else:
self.set_widget_normal(entry_widget)

def validate_text_limit(self, entry_widget, max_len):
text = entry_widget.get("1.0", "end-1c")
if len(text) > max_len or any(not c.isalpha() and c != ' ' for c in text):
self.set_widget_red(entry_widget)
else:
self.set_widget_normal(entry_widget)

def set_widget_red(self, widget):
if isinstance(widget, Entry):
widget.config(bg="misty rose")
else:
widget.config(bg="misty rose")

def set_widget_normal(self, widget):
if isinstance(widget, Entry):
widget.config(bg="white")
else:
widget.config(bg="white")

# ---------------------------
# Image Upload
# ---------------------------
def upload_image(self):
file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
if not file_path:
return
image = Image.open(file_path)
image.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))
self.agent_image = ImageTk.PhotoImage(image)
self.image_canvas.delete("all")
self.image_canvas.create_image(IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2, image=self.agent_image)

# ---------------------------
# Skills
# ---------------------------
def add_skill(self):
if len(self.skills) >= MAX_SKILLS:
return
entry = Entry(self.skills_frame, width=40)
entry.pack(pady=1)
entry.bind("<KeyRelease>", lambda e: self.validate_letters_only(entry))
self.skills.append(entry)

def remove_skill(self):
if self.skills:
entry = self.skills.pop()
entry.destroy()

# ---------------------------
# Metrics
# ---------------------------
def add_metric(self):
if len(self.metrics) >= MAX_METRICS:
return
entry = Entry(self.metrics_frame, width=40)
entry.pack(pady=1)
entry.bind("<KeyRelease>", lambda e: self.validate_letters_only(entry))
self.metrics.append(entry)

def remove_metric(self):
if self.metrics:
entry = self.metrics.pop()
entry.destroy()

# ---------------------------
# Toggle Buttons
# ---------------------------
def toggle_display(self):
if self.display_on.get():
if not self.display_button:
self.display_button = Button(self.root, text="Display")
self.display_button.pack(pady=5)
else:
if self.display_button:
self.display_button.destroy()
self.display_button = None

def toggle_execute(self):
if self.execute_on.get():
if not self.execute_button:
self.execute_button = Button(self.root, text="Execute")
self.execute_button.pack(pady=5)
else:
if self.execute_button:
self.execute_button.destroy()
self.execute_button = None

# ---------------------------
# Run Application
# ---------------------------
if __name__ == "__main__":
root = Tk()
app = AgenticAIBuilder(root)
root.mainloop()
