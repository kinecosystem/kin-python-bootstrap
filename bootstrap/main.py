"""Main entry point"""

from src.config import config
from src.routes import app

app.run(access_log=False, host='0.0.0.0', port=config.PORT)
