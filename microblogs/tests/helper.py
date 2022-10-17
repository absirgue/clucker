class LogInTester():
    def _is_logged_in(self):
        # self.client.session is a dictionnary containing all the session data
        return '_auth_user_id' in self.client.session.keys()
