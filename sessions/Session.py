import os
from sessions.SessionID import SessionID


class Session:
    def __init__(self, host):
        self.path_to_sessions = "temp-sessions/"
        self.session = SessionID(host)
        if not os.path.exists(self.path_to_sessions + str(str(self.session))):
            os.mkdir(self.path_to_sessions + str(self.session))
        else:
            print("Сессия клиента " + str(self.session) + " уже существует")

    def get_current_session_dir(self):
        return self.path_to_sessions + str(self.session)

    def close_session(self):
        files_in_dir = os.listdir(self.get_current_session_dir())
        for file in files_in_dir:
            os.remove(self.get_current_session_dir() + "/" + file)
        try:
            files_in_dir = os.listdir(self.get_current_session_dir() + "/predict")
            for file in files_in_dir:
                os.remove(self.get_current_session_dir() + "/predict/" + file)
        except:
            pass
        os.rmdir(self.get_current_session_dir())

    def __str__(self):
        return self.path_to_sessions + str(self.session)

    def __del__(self):
        return
        self.close_session()
