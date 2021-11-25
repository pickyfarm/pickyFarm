from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = "comments"

    # django signal
    def ready(self):
        import comments.signals
