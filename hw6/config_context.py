GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def init(self, updates:dict, validator=None):
        self.original_config = {}
        self.updates = updates
        if validator is not None:
            self.validator = validator

    def enter(self):
        self.original_config = GLOBAL_CONFIG.copy()
        new_config = GLOBAL_CONFIG.copy()
        new_config.update(self.updates)

        if self.validator:
            if not self.validator(new_config):
                raise ValueError("Invalid configuration")

        GLOBAL_CONFIG.update(self.updates)

        return self

    def exit(self, exc_type, exc_value, traceback):
        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original_config)

def validate_config(config):
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0


print("Before:", GLOBAL_CONFIG)

with Configuration({"feature_a": False, "max_retries": 10}, validator=validate_config):
    print("Inside context:", GLOBAL_CONFIG)

print("After:", GLOBAL_CONFIG)