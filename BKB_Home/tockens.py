from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TockenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk)+text_type(timestamp)  # This is unique string which will be link for user
        )
generate_token=TockenGenerator()