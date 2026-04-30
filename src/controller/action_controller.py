class ActionController:
    def __init__(self, actions: dict, action_map: dict, app_map: dict = {}):
        self.actions = actions
        self.action_map = {**action_map, **app_map}  # объединяем

    def execute(self, gesture: str, hand_label: str, gesture_type: str):
        if gesture_type == "complex":
            action_name = self.actions.get("complex", {}).get(gesture)
        else:
            section = self.actions.get(f"simple_{hand_label.lower()}", {})
            action_name = section.get(gesture)

        action_func = self.action_map.get(action_name)
        if action_func:
            action_func()