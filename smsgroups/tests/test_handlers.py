from __future__ import unicode_literals

from django.test import TestCase

from ..handlers.create_group import CreateHandler
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
