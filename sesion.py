# sesion.py

class Sesion:
    def __init__(self) -> None:
        self.user_id = None
        self.user_name = None

    def userID(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def kullaniciID(self):
        return self.user_id

    def kullaniciSurname(self):
        return self.user_name

session_manager = Sesion()
