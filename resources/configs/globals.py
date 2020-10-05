path_to_config_json = r'resources/configs/configs.json'

from resources.configs.configs_utils import get_app_config
app_config = get_app_config()['config']
