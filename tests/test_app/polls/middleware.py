import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.db import transaction
from django.utils.deprecation import MiddlewareMixin


class CleanupMiddleware(MiddlewareMixin):

    @transaction.atomic
    def process_response(self, request, response):
        """
        10% of requests will cause all data to be reset
        """

        if settings.PERIODIC_RESET:
            if random.randint(1, 10) == 1:
                User.objects.all().delete()
                Group.objects.all().delete()

                call_command('loaddata', 'initial_data')

                messages.add_message(request, messages.INFO, 'All data has been reset')

        return response
