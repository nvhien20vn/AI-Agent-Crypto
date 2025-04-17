import yaml
import os



def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config



# Get the absolute path to the settings directory
settings_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(settings_dir, 'llm.yaml')



LLM_CONF = load_config(yaml_path)