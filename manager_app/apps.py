from django.apps import AppConfig


class ManagerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager_app'

class GroupCollaboratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GroupCollaborator'

    def ready(self):
        import manager_app.signals
