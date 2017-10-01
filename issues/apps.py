from django.apps import AppConfig


class IssuesConfig(AppConfig):
    name = 'issues'

    def ready(self):
        import issues.signals