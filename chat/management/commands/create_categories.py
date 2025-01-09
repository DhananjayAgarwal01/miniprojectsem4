from django.core.management.base import BaseCommand
from chat.models import Category

class Command(BaseCommand):
    help = 'Creates initial categories for donations'

    def handle(self, *args, **kwargs):
        categories = [
            'Clothing',
            'Electronics',
            'Furniture',
            'Books',
            'Toys',
            'Kitchen Items',
            'Sports Equipment',
            'School Supplies',
            'Medical Equipment',
            'Baby Items',
            'Home Decor',
            'Tools',
            'Musical Instruments',
            'Art Supplies',
            'Pet Supplies',
            'Office Supplies',
            'Garden Tools',
            'Food (Non-perishable)',
            'Personal Care Items',
            'Automotive'
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}')) 