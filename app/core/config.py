from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "llama3.2:1b"
    api_key: str = ""
    request_timeout: float = 120.0
    default_temperature: float = 0.2
    default_max_tokens: int = 128
    log_level: str = "INFO"
    reports_dir: str = "reports"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
