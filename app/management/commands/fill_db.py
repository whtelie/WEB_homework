from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data filling')

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Create users
        self.stdout.write(self.style.SUCCESS(f'Creating {ratio} users...'))
        users = []
        for _ in range(ratio):
            user = User.objects.create(username=fake.user_name() + str(_), password=fake.password())
            users.append(user)

        # Create programming languages as tags
        programming_languages = ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Swift', 'Go', 'TypeScript', 'PHP']
        self.stdout.write(self.style.SUCCESS(f'Creating {len(programming_languages)} programming language tags...'))
        tags = []
        for language in programming_languages:
            tag = Tag.objects.create(name=language)
            tags.append(tag)

        # Create questions and answers
        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 10} questions and {ratio * 100} answers...'))
        for _ in range(ratio * 10):
            question = Question.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                author=random.choice(users)
            )
            question.tags.set(random.sample(tags, random.randint(1, len(programming_languages))))

            for _ in range(ratio * 10):
                answer = Answer.objects.create(
                    content=fake.text(),
                    author=random.choice(users),
                    question=question
                )

        # Create likes
        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 200} likes...'))
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(Question.objects.all())
            answer = random.choice(Answer.objects.all())
            Like.objects.create(user=user, question=question, answer=answer)

        self.stdout.write(self.style.SUCCESS('Database successfully filled.'))
