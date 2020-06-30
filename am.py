from Tools import tools_v000 as tools
import os
from os.path import dirname

# -2 for the name of this project AM
save_path = dirname(__file__)[ : -2]
propertiesFolder_path = save_path + "Properties"

# Example of used
user_text = tools.readProperty(propertiesFolder_path, 'AM', 'user_text=')

