import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class TemplateRenderer:
    def __init__(self, template_dir: str):
        path = Path(template_dir)
        if not path.exists():
            logging.error(f"❌ Template directory not found: {template_dir}")
            raise FileNotFoundError(f"Template directory not found: {template_dir}")

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False
        )

    def render(self, template_name: str, context: dict) -> str:
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**context)
            logging.debug(f"Rendered template: {template_name}")
            return rendered
        except TemplateNotFound:
            logging.error(f"❌ Template not found: {template_name}")
            raise
        except Exception as e:
            logging.error(f"❌ Failed to render template '{template_name}': {e}")
            raise
