from injector import inject

from linkedinapi.variable.SecretKeyVariable import SecretKeyVariable


class SecretManager:

    @inject
    def __init__(self, secret_key: SecretKeyVariable):
        self.secret_key = secret_key

    def get_secret_key(self):
        return self.secret_key