import time
import uuid
import logging
from pathlib import Path

from app.generator import AgentGenerator
from templates.renderer import TemplateRenderer
from config.loader import ConfigLoader
from outputs.logger import OutputLogger


class AgentEngine:
    def __init__(self, config_path: str):
        self.config = ConfigLoader.load(config_path)
        self.renderer = TemplateRenderer(self.config["template_dir"])
        self.generator = AgentGenerator(self.config)
        self.logger = OutputLogger(self.config["output_dir"])
        self.session_id = str(uuid.uuid4())
        self.history = []

    def run(self):
        tasks = self.config.get("tasks", [])
        if not tasks:
            logging.warning("No tasks configured. Exiting.")
            return

        logging.info(f"Agent session {self.session_id} started with {len(tasks)} task(s).")
        for index, task in enumerate(tasks, 1):
            logging.info(f"[{index}/{len(tasks)}] Executing task: {task['name']}")
            start_time = time.time()

            # Prepare context and prompt
            context = self._build_context(task)
            prompt = self.renderer.render(task["template"], context)

            # Generate agent response
            result = self.generator.generate(prompt)

            # Log output
            record = {
                "task": task["name"],
                "prompt": prompt,
                "result": result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.logger.save(record)
            self.history.append(record)

            elapsed = time.time() - start_time
            logging.info(f"✅ Task '{task['name']}' completed in {elapsed:.2f} seconds")

        logging.info(f"Agent session {self.session_id} finished.")

    def _build_context(self, task: dict) -> dict:
        context = {
            "input": task.get("input", ""),
            "metadata": task.get("metadata", {}),
            "session_id": self.session_id,
        }
        return context
