import mock

from rapidsms.contrib.handlers.app import App as HandlerApp
from rapidsms.tests.harness import TestScript


class GroupTestCase(TestScript):
    """Integration testing of the group interactions."""

    apps = (HandlerApp, )

    def test_multiple_user_script(self):
        """One user creates the group, another joins and says ping, reply with pong."""

        with mock.patch('smsgroups.handlers.create_group.get_random_string') as mock_random:
            mock_random.return_value = '1234567890'
            self.runScript('''
15553437777 > create
15553437777 < Group "1234567890" created! Use this identifier to SEND msgs or for others to JOIN.
15557773434 > join 1234567890
15557773434 < You are now a member. SEND msgs the group by using the "1234567890:" prefix.
15557773434 > 1234567890: ping
15557773434 < Message was sent to 1 member.
15553437777 < From 1234567890: ping
15553437777 > 1234567890: pong
15553437777 < Message was sent to 1 member.
15557773434 < From 1234567890: pong
            ''')
