from __future__ import unicode_literals

from django.db import transaction

from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.models import Contact

from ..models import Group, Member


class JoinHandler(KeywordHandler):
    keyword = 'join'

    def handle(self, text):
        """Join an existing group."""

        try:
            group = Group.objects.get(slug=text.strip())
        except Group.DoesNotExist:
            self.respond('Unknown group id "%s"' % text.strip())
        else:
            with transaction.atomic():
                connection = self.msg.connections[0]
                contact = connection.contact
                if not contact:
                    contact = Contact.objects.create(name='')
                    connection.contact = contact
                    connection.save(update_fields=('contact', ))
                _, created = Member.objects.get_or_create(
                    contact=contact, group=group, defaults={'is_creator': False})
                if created:
                    reply = 'You are now a member.'
                else:
                    reply = 'You are already a member.'
                reply = '%s SEND msgs the group by using the "%s:" prefix.' % (reply, group.slug)
                self.respond(reply)

    def help(self):
        """Handle message which is missing the slug parameter."""
        self.respond('To join a group, send JOIN <id> for an existing group.')
