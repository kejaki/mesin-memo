"""
Script to create predefined badges
Run: python manage.py shell < create_badges.py
"""
from users.models import Badge

badges_data = [
    {'name': 'PIC Divisi', 'slug': 'pic-divisi', 'color': 'purple', 'icon': '👑', 'description': 'Person In Charge Divisi'},
    {'name': 'Ketua Media Moklet', 'slug': 'ketua-memo', 'color': 'blue', 'icon': '🎖️', 'description': 'Ketua Media Moklet'},
    {'name': 'Wakil Ketua', 'slug': 'waka-memo', 'color': 'green', 'icon': '🥈', 'description': 'Wakil Ketua Media Moklet'},
    {'name': 'Sekretaris', 'slug': 'sekretaris', 'color': 'yellow', 'icon': '📝', 'description': 'Sekretaris Media Moklet'},
    {'name': 'Top Contributor', 'slug': 'top-contributor', 'color': 'red', 'icon': '⭐', 'description': 'Kontributor Terbaik'},
]

for badge_data in badges_data:
    badge, created = Badge.objects.get_or_create(
        slug=badge_data['slug'],
        defaults=badge_data
    )
    if created:
        print(f"✅ Created badge: {badge.name}")
    else:
        print(f"ℹ️  Badge already exists: {badge.name}")

print(f"\n🎉 Total badges: {Badge.objects.count()}")
