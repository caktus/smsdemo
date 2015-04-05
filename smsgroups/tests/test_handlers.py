from __future__ import unicode_literals

from django.test import TestCase

from ..handlers.create_group import CreateHandler
from ..handlers.join_group import JoinHandler
from ..models import Group


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
