from dependency_injector import containers, providers

from app.core.database import Database
from app.core.config import Configs
from app.repository import UserRepository
from app.service import UserService


class Container(containers.DeclarativeContainer):
    """Dependency injection container for the application."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.user_endpoints",
        ]
    )

    config = providers.Singleton(Configs)

    database = providers.Singleton(
        Database,
        db_url=config.provided.DATABASE_URL,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=database.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
