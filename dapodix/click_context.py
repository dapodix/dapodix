import attr
from click import Context
from typing import Optional

from dapodik import Dapodik, __semester__


@attr.dataclass
class ContextObject:
    username: str = ""
    password: str = ""
    pengguna: int = 0
    server: str = "http://localhost:5774/"
    semester: str = __semester__
    rememberme: bool = True
    _dapodik: Optional[Dapodik] = None

    @property
    def dapodik(self) -> Dapodik:
        if self._dapodik:
            return self._dapodik
        assert self.username
        assert self.password
        self._dapodik = Dapodik(
            username=self.username,
            password=self.password,
            semester_id=self.semester,
            server=self.server,
            pengguna=self.pengguna,
            rememberme=self.rememberme,
        )
        return self._dapodik


class ClickContext(Context):
    obj: ContextObject
