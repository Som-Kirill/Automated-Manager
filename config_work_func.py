class ConfigReader:
    def __init__(self, config={}):
        self.config = config

    def read_config(self):
        try:
            with open('config.cfg', 'r') as config_file:
                cfg = config_file.read()

            cfg = cfg[cfg.index('{')+1:cfg.index('}')]
            cfg = cfg.split(',')

            for data in cfg:
                data = data.strip().split(':')
                key = data[0].strip().replace("'", "")
                value = data[1].strip().replace("'", "")
                # Перевірка, чи є рядок value числовим
                if value.isdigit():
                    self.config[key] = int(value)  # Записуємо числове значення у словнику
                else:
                    self.config[key] = value  # Записуємо рядок value у словнику
        except FileNotFoundError:
            print("Файл config.cfg не знайдено.")
        except Exception as e:
            print(f"Помилка при читанні конфігураційного файлу: {e}")