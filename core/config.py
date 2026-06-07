from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
import hvac
import logging


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    VAULT_ADDR: str | None = None
    VAULT_TOKEN: str | None = None
    VAULT_SECRET_PATH: str = "secret/data/auth-service"

    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/authdb"
    REDIS_URL: str = "redis://localhost:6379"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def load_secrets(self) -> "Settings":
        if self.VAULT_ADDR and self.VAULT_TOKEN:
            self._load_from_vault()
        else:
            logger.info("Has no Vault credentials, using .env")
            self._validate_local_keys()
        return self

    def _load_from_vault(self) -> None:
        logger.info(f"Loading secrets from Vault: {self.VAULT_ADDR}")

        try:
            client = hvac.Client(
                url=self.VAULT_ADDR,
                token=self.VAULT_TOKEN,
            )

            if not client.is_authenticated():
                raise RuntimeError("Vault: invalid token")

            secret = client.secrets.kv.v2.read_secret_version(
                path=self.VAULT_SECRET_PATH,
            )
            data = secret["data"]["data"]

            self.JWT_PRIVATE_KEY = data["JWT_PRIVATE_KEY"]
            self.JWT_PUBLIC_KEY = data["JWT_PUBLIC_KEY"]

            logger.info("Loading secrets from Vault was successful!")
        except Exception as e:
            raise RuntimeError(f"Can't load secrets from Vault: {e}")

    def _validate_local_keys(self) -> None:
        if not self.JWT_PRIVATE_KEY:
            raise ValueError(
                "JWT_PRIVATE_KEY is empty "
                "Write it in .env or use Vault (VAULT_ADDR + VAULT_TOKEN)"
            )
        if not self.JWT_PUBLIC_KEY:
            raise ValueError("JWT_PUBLIC_KEY is empty")

    @property
    def jwt_private_key(self) -> str:
        return self.JWT_PRIVATE_KEY.replace("\\n", "\n")

    @property
    def jwt_public_key(self) -> str:
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n")


settings = Settings()