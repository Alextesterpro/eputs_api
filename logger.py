import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Настройка обработчика (вывод в консоль)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)