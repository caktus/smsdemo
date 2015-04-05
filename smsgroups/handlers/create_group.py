from __future__ import unicode_literals

from django.db import transaction
from django.utils.crypto import get_random_string

from rapidsms.contrib.handlers import PatternHandler
from rapidsms.models import Contact

from ..models import Group, Member


class CreateHandler(PatternHandler):
    pattern = 'create'

    def handle(self):
        """Create a new group."""

        created = False
        while not created:
            slug = get_random_string(length=10, allowed_chars='01234567890')
            with transaction.atomic():
                group, created = Group.objects.get_or_create(slug=slug)
                if created:
                    connection = self.msg.connections[0]
                    contact = connection.contact
                    if not contact:
                        contact = Contact.objects.create(name='')
                        connection.contact = contact
                        connection.save(update_fields=('contact', ))
                    Member.objects.create(contact=contact, group=group, is_creator=True)
        reply = (
            'Group "%(slug)s" created! '
            'Use this identifier to SEND msgs or for others to JOIN.'
        ) % {'slug': slug}
        self.respond(reply)
