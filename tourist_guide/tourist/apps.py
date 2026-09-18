from django.apps import AppConfig


# class TouristConfig(AppConfig):
#     name = 'tourist'


from django.apps import AppConfig


class TouristConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "tourist"

    def ready(self):
        import tourist.signals