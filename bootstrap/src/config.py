from kin import config as kin_config
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Config options for the bootstrap server

    If an environmental variable exist for the same name, it will override the default value given here
    """

    SEED: str = 'SCOMIY6IHXNIL6ZFTBBYDLU65VONYWI3Y6EN4IDWDP2IIYTCYZBCCE6C'
    HORIZON_ENDPOINT: str = kin_config.HORIZON_URI_TEST
    NETWORK_PASSPHRASE: str = kin_config.HORIZON_PASSPHRASE_TEST
    APP_ID: str = kin_config.ANON_APP_ID
    CHANNEL_COUNT: int = 100
    CHANNEL_SALT: str = 'bootstrap'
    CHANNEL_STARTING_BALANCE: int = 1
    PORT: int = 8000
    LOG_LEVEL: str = 'INFO'

    class Config:
        env_prefix = ''
