from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cms.models import ContentItem
from events.models import Event

class Command(BaseCommand):
    help = 'Create default user groups and permissions'

    def handle(self, *args, **kwargs):
        # Create Groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        coordinator_group, _ = Group.objects.get_or_create(name='Coordinator')
        member_group, _ = Group.objects.get_or_create(name='Member')

        # Get content types
        content_ct = ContentType.objects.get_for_model(ContentItem)
        event_ct = ContentType.objects.get_for_model(Event)

        # Admin permissions (full access)
        admin_permissions = Permission.objects.filter(
            content_type__in=[content_ct, event_ct]
        )
        admin_group.permissions.set(admin_permissions)

        # Coordinator permissions (can add/change/view)
        coordinator_permissions = Permission.objects.filter(
            content_type__in=[content_ct, event_ct],
            codename__in=[
                'add_contentitem', 'change_contentitem', 'view_contentitem',
                'add_event', 'change_event', 'view_event'
            ]
        )
        coordinator_group.permissions.set(coordinator_permissions)

        # Member permissions (can add/view only)
        member_permissions = Permission.objects.filter(
            content_type__in=[content_ct, event_ct],
            codename__in=['add_contentitem', 'view_contentitem', 'view_event']
        )
        member_group.permissions.set(member_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created user groups'))
