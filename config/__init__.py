from ruamel.yaml import YAML
from config import setting


class Settings(object):
    def __init__(self) -> None:
        # 获取全局变量中的配置信息
        for attr in dir(setting):
            setattr(self, attr, getattr(setting, attr))

        path_to_yaml = self.root_directory.joinpath("config.yaml")
        if path_to_yaml.exists():
            yaml = YAML()
            with open(path_to_yaml, mode="r", encoding="utf-8") as docs:
                try:
                    configuration = yaml.load(docs)
                except Exception as exc:
                    exit(exc)

            for item in configuration:
                setattr(self, item, configuration[item])

settings = Settings()
