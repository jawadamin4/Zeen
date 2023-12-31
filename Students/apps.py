from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Students'
    verbose_name = '1:Students Application Process'

    def ready(self):
        import Students.signals

