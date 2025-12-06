import os
from PIL import Image, ImageDraw, ImageFont

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "output")
FONT_PATH = os.path.join(ASSETS_DIR, "Roboto-Bold.ttf")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_agent_card(agent_name, image_path, description, core_skills, metrics, show_details=True):
    # Constants
    WIDTH, HEIGHT = 1024, 576
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    BOX_COLOR = (80, 80, 80)
    TITLE_FONT_SIZE = 40
    BODY_FONT_SIZE = 24

    # Create image
    img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
        body_font = ImageFont.truetype(FONT_PATH, BODY_FONT_SIZE)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw border boxes
    draw.rectangle([20, 20, WIDTH - 20, HEIGHT - 20], outline=BOX_COLOR, width=2)

    # Agent image
    if image_path and os.path.isfile(image_path):
        agent_img = Image.open(image_path).convert("RGBA")
        agent_img = agent_img.resize((180, 180))
        img.paste(agent_img, (40, 60))

    # Agent Name
    draw.text((240, 60), agent_name, font=title_font, fill=TEXT_COLOR)

    # Description
    draw.text((240, 110), description, font=body_font, fill=TEXT_COLOR)

    # Core Skills
    draw.text((40, 270), "Core Skills:", font=body_font, fill=TEXT_COLOR)
    for idx, skill in enumerate(core_skills[:5]):
        draw.text((60, 300 + idx * 30), f"• {skill}", font=body_font, fill=TEXT_COLOR)

    # Metrics
    draw.text((500, 270), "Metrics:", font=body_font, fill=TEXT_COLOR)
    for idx, metric in enumerate(metrics[:3]):
        draw.text((520, 300 + idx * 30), f"• {metric}", font=body_font, fill=TEXT_COLOR)

    # Buttons
    if show_details:
        draw.rectangle([WIDTH - 200, HEIGHT - 80, WIDTH - 60, HEIGHT - 40], fill=BOX_COLOR)
        draw.text((WIDTH - 185, HEIGHT - 72), "Details", font=body_font, fill=TEXT_COLOR)

    # Execute button
    draw.rectangle([60, HEIGHT - 80, 200, HEIGHT - 40], fill=BOX_COLOR)
    draw.text((80, HEIGHT - 72), "Execute", font=body_font, fill=TEXT_COLOR)

    # Save
    output_path = os.path.join(OUTPUT_DIR, f"{agent_name.replace(' ', '_')}_card.png")
    img.save(output_path)
    return output_path
