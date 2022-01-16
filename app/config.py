import dependency_injector.containers as containers
import dependency_injector.providers as providers
from app.user.user_service import DefaultUserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.user.router"])
    user_service = providers.Factory(
        DefaultUserService
    )