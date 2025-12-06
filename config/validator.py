import logging


class ConfigValidator:
    REQUIRED_TASK_FIELDS = ["name", "template"]
    
    @staticmethod
    def validate_task(task: dict, index: int):
        missing = [field for field in ConfigValidator.REQUIRED_TASK_FIELDS if field not in task]
        if missing:
            raise ValueError(f"Task {index} is missing required fields: {missing}")

    @staticmethod
    def validate_all_tasks(task_list: list):
        if not isinstance(task_list, list):
            raise ValueError("The 'tasks' field must be a list.")

        for index, task in enumerate(task_list, start=1):
            try:
                ConfigValidator.validate_task(task, index)
            except ValueError as e:
                logging.error(f"❌ Invalid task config at index {index}: {e}")
                raise

        logging.info(f"✅ Validated {len(task_list)} task(s)")
