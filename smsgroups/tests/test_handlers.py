from __future__ import unicode_literals

import mock

from django.test import TestCase
from rapidsms.models import Backend, Connection, Contact

from ..handlers.create_group import CreateHandler
from ..handlers.join_group import JoinHandler
from ..handlers.msg_group import BroadcastHandler
from ..models import Group, Member


class CreateHandlerTestCase(TestCase):
    """Create new SMS group."""

    def test_create_group(self):
        """Create a new group with the CREATE command."""

        replies = CreateHandler.test('CREATE')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        group = Group.objects.latest('pk')
        self.assertIn('Group "%s" created!' % group.slug, replies[0])
        self.assertEqual(group.member_set.count(), 1)


class JoinHandlerTestCase(TestCase):
    """Join an existing SMS group."""

    def setUp(self):
        self.group = Group.objects.create(slug='1234567890')

    def test_join_group(self):
        """Join group with the JOIN command."""

        replies = JoinHandler.test('JOIN %s' % self.group.slug)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertIn('You are now a member.', replies[0])
        self.assertEqual(self.group.member_set.count(), 1)

    def test_help(self):
        """If group ID is missing then show the HELP message."""

        replies = JoinHandler.test('JOIN')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual(
            'To join a group, send JOIN <id> for an existing group.', replies[0])

    def test_unknown_group(self):
        """Handle invalid group IDs."""

        slug = self.group.slug
        self.group.delete()
        replies = JoinHandler.test('JOIN %s' % self.group.slug)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Unknown group id "%s"' % slug, replies[0])

    def test_already_joined(self):
        """Handle a user which has already joined the group."""

        JoinHandler.test('JOIN %s' % self.group.slug, identity='abcxyz')
        replies = JoinHandler.test('JOIN %s' % self.group.slug, identity='abcxyz')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertIn('You are already a member.', replies[0])
        self.assertEqual(self.group.member_set.count(), 1)


@mock.patch('smsgroups.handlers.msg_group.send')
class BroadcastHandlerTestCase(TestCase):
    """Send message to other members of a group."""

    def setUp(self):
        self.group = Group.objects.create(slug='1234567890')
        self.backend = Backend.objects.create(name='test_backend')
        self.test_contact = Contact.objects.create(name='test')
        self.test_connection = Connection.objects.create(
            identity='test', backend=self.backend, contact=self.test_contact)
        self.test_member = Member.objects.create(
            group=self.group, contact=self.test_contact)
        self.other_contact = Contact.objects.create(name='other')
        self.other_connection = Connection.objects.create(
            identity='other', backend=self.backend, contact=self.other_contact)
        self.other_member = Member.objects.create(
            group=self.group, contact=self.other_contact)
        BroadcastHandler._mock_backend = self.backend

    def test_send_message(self, mock_send):
        """Send messages to the other user in the group."""

        replies = BroadcastHandler.test(
            '%s: hello' % self.group.slug, identity=self.test_connection.identity)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Message was sent to 1 member.', replies[0])
        self.assertTrue(mock_send.called)
        args, kwargs = mock_send.call_args
        self.assertEqual(args, ('From %s: hello' % self.group.slug, ))
        recipients = kwargs['connections']
        self.assertItemsEqual(recipients, [self.other_connection, ])

    def test_unknown_group(self, mock_send):
        """Handle unknown group."""

        replies = BroadcastHandler.test(
            '0987654321: hello', identity=self.test_connection.identity)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Unknown group id "0987654321"', replies[0])
        self.assertFalse(mock_send.called)

    def test_not_a_member(self, mock_send):
        """Handle message from user not in the group."""

        replies = BroadcastHandler.test(
            '%s: hello' % self.group.slug, identity='unknown')
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('You are not a member of this group.', replies[0])
        self.assertFalse(mock_send.called)

    def test_no_other_members(self, mock_send):
        """Handle group with only one memember."""

        self.other_member.delete()
        replies = BroadcastHandler.test(
            '%s: hello' % self.group.slug, identity=self.test_connection.identity)
        self.assertTrue(replies)
        self.assertEqual(len(replies), 1)
        self.assertEqual('Message was sent to 0 members.', replies[0])
        self.assertFalse(mock_send.called)
