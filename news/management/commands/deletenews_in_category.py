from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post

class Command(BaseCommand):
    help = 'Delete news from selected category'
    # missing_args_message = 'Some arguments are missing'
    requires_migrations_checks = True


    # def add_arguments(self, parser):
    #     parser.add_argument('category', nargs='+', type=int)

    def handle(self, *args: Any, **options: Any) -> str | None:
        categories = Category.objects.values_list("category", flat=True)

        self.stdout.readable()
        self.stdout.write(f'Categories: {categories}')
        self.stdout.write('Select category for deleting news in it')
        category = str(input()).upper()
        self.stdout.write(f'You select {category} category')
        category_id = Category.objects.get(category=category).id
        self.stdout.write('Do you really want to delete all news in category? yes/no')
        answer = str(input()).upper()
        self.stdout.write(f'{answer}')
        if answer == 'YES' or answer == 'Y':
            news = Post.objects.filter(category=category_id, type='N')
            self.stdout.write(f'You select {len(news)} news')
            news.delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully wiped news in {category} category!'))
            return
        self.stdout.write(self.style.ERROR('Access denied')) # в случае неправильного подтверждения, говорим, что в доступе отказано