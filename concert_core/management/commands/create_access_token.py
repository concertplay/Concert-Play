from django.core.management.base import BaseCommand
from concert_core.api_helpers import get_new_access_token

class Command(BaseCommand):

    def handle(self, *args, **options):
        get_new_access_token()