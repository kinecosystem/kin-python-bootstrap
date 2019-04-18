"""Main entry point"""

from src.config import Settings
from src.init import init_app

config = Settings()
app = init_app(config)
app.run(access_log=False, host='0.0.0.0', port=config.PORT)
