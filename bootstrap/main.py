"""Main entry point"""

from config import config
from src.routes import app

app.run(access_log=False, port=config.PORT)