# core/management/commands/delete_all_reviews.py

from django.core.management.base import BaseCommand
from core.models import Review

class Command(BaseCommand):
    help = 'Deletes all Review instances'

    def handle(self, *args, **options):
        num_deleted, _ = Review.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {num_deleted} Review instances'))
