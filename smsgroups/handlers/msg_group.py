from __future__ import unicode_literals

from rapidsms.contrib.handlers import PatternHandler
from rapidsms.models import Contact, Connection
from rapidsms.router import send

from ..models import Group


class BroadcastHandler(PatternHandler):
    pattern = '^([0-9]{10}):\s?(\S+)'

    def handle(self, slug, text):
        """Broadcast messages to users in a group."""
        try:
            group = Group.objects.get(slug=slug)
        except Group.DoesNotExist:
            self.respond('Unknown group id "%s"' % slug.strip())
        else:
            # Check for membership
            connection = self.msg.connections[0]
            contacts = Contact.objects.filter(member__group=group)
            if not contacts.filter(connection__pk=connection.pk):
                self.respond('You are not a member of this group.')
            else:
                connections = Connection.objects.filter(
                    contact__in=contacts, backend=connection.backend,
                ).exclude(pk=connection.pk)
                count = connections.count()
                if count:
                    send('From %s: %s' % (slug, text), connections=connections)
                self.respond('Message was sent to %s member%s.' % (
                    count, count != 1 and 's' or ''))
