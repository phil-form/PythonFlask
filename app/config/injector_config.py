from app.framework.auth_service import AuthService
from app.framework.injector import ContainerConfig, DependencyConfig, Scope
from app.services.role_service import RoleService
from app.services.auth_service_impl import AuthServiceImpl
from app.services.basket_item_service import BasketItemService
from app.services.product_service import ProductService
from app.services.user_service import UserService


def config_injector(config: ContainerConfig):
    # Je dis que quand on me demande d'injecter le AuthService, j'injecte la AuthServiceImpl
    # Et je crée un nouveau AuthService à chaque requête.
    config.bind(DependencyConfig(AuthService, AuthServiceImpl, Scope.SCOPED))
    # !!! Le BasketItemService nécissite l'AuthService, donc il faut qu'il soit aussi en SCOPED
    # pour que chaque requête ait son propre AuthService.
    config.bind(DependencyConfig(BasketItemService, BasketItemService, Scope.SCOPED))
    # Je dis que le BasketItemService, implémente le BasketItemService
    # Et n'existe qu'une seule fois au niveau de l'application.
    config.bind(DependencyConfig(UserService, UserService, Scope.SINGLETON))
    config.bind(DependencyConfig(ProductService, ProductService, Scope.SINGLETON))
    config.bind(DependencyConfig(RoleService, RoleService, Scope.SINGLETON))
