import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
print(f"Active users: {User.objects.filter(is_active=True).count()}")
leaders = User.objects.filter(is_active=True).order_by('-points')[:3]
print(f"Top leaders count: {leaders.count()}")
for user in leaders:
    print(f"- {user.username}: {user.points}")
