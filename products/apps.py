from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = "products"

    # django signal
    def ready(self):
        import products.signals


