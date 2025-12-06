import streamlit as st
from core.generator import generate_visual_card
from PIL import Image
import os

st.set_page_config(page_title="AgenticAI Builder", layout="centered")

st.title("🧠 AgenticAI Builder")

# Upload agent image
st.header("Step 1: Upload Agent Image (.png or .jpeg)")
agent_image = st.file_uploader("Choose an image", type=["png", "jpeg", "jpg"])
if agent_image:
    st.image(agent_image, caption="Agent Image", use_column_width=True)
    image_path = os.path.join("assets", agent_image.name)
    with open(image_path, "wb") as f:
        f.write(agent_image.getbuffer())

# Agent name
st.header("Step 2: Agent Name")
agent_name = st.text_input("Enter Agent Name", max_chars=40)

# Agent description
st.header("Step 3: Agent Description")
agent_description = st.text_area("Enter a short paragraph describing the Agent", height=150, max_chars=400)

# Core Skills (max 5)
st.header("Step 4: Core Skills (Max 5)")
core_skills = []
for i in range(5):
    skill = st.text_input(f"Skill #{i+1}", key=f"skill_{i}")
    if skill:
        core_skills.append(skill)

# Custom KPIs or Info Metrics (up to 3)
st.header("Step 5: Key Metrics or Info (Optional, Max 3)")
info_metrics = []
for i in range(3):
    label = st.text_input(f"Metric Label #{i+1}", key=f"label_{i}")
    value = st.text_input(f"Metric Value #{i+1}", key=f"value_{i}")
    if label and value:
        info_metrics.append((label, value))

# Generate Button
if st.button("🚀 Generate AgenticAI Visual"):
    if not agent_image or not agent_name or not agent_description:
        st.warning("Please provide all required inputs: Agent image, name, and description.")
    else:
        image_path = os.path.join("assets", agent_image.name)
        output_path = generate_visual_card(
            image_path=image_path,
            agent_name=agent_name,
            agent_description=agent_description,
            core_skills=core_skills,
            info_metrics=info_metrics
        )
        st.success("✅ Visual Card Generated!")
        st.image(output_path, caption="AgenticAI Visual", use_column_width=True)
        with open(output_path, "rb") as file:
            st.download_button("📥 Download Visual", data=file, file_name="agenticai_card.png")
