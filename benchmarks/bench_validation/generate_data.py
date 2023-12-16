import datetime
import random
import string
from rich import print


class Generator:
    UTC = datetime.timezone.utc
    DATE_2018 = datetime.datetime(2018, 1, 1, tzinfo=UTC)
    DATE_2023 = datetime.datetime(2023, 1, 1, tzinfo=UTC)
    PERMISSIONS = ["READ", "WRITE", "READ_WRITE"]
    NAMES = [
        "alice",
        "ben",
        "carol",
        "daniel",
        "esther",
        "franklin",
        "genevieve",
        "harold",
        "ilana",
        "jerome",
        "katelyn",
        "leonard",
        "monique",
        "nathan",
        "ora",
        "patrick",
        "quinn",
        "ronald",
        "stephanie",
        "thomas",
        "uma",
        "vince",
        "wendy",
        "xavier",
        "yitzchak",
        "zahra",
    ]

    def __init__(self, capacity, seed=42):
        self.capacity = capacity
        self.random = random.Random(seed)

    def randdt(self, min, max):
        ts = self.random.randint(min.timestamp(), max.timestamp())
        return datetime.datetime.fromtimestamp(ts).replace(tzinfo=self.UTC)

    def randstr(self, min=None, max=None):
        if max is not None:
            min = self.random.randint(min, max)
        return "".join(self.random.choices(string.ascii_letters, k=min))

    def _make(self, is_dir=False):
        name = self.randstr(4, 30)
        created_by = self.random.choice(self.NAMES)
        created_at = self.randdt(self.DATE_2018, self.DATE_2023)
        data = {
            "type": "directory" if is_dir else "file",
            "name": name,
            "created_by": created_by,
            "created_at": created_at.isoformat(),
        }
        if self.random.random() > 0.75:
            updated_by = self.random.choice(self.NAMES)
            updated_at = self.randdt(created_at, self.DATE_2023)
            data.update(
                updated_by=updated_by,
                updated_at=updated_at.isoformat(),
            )
        return data

    def make_file(self):
        data = self._make()
        data["nbytes"] = self.random.randint(0, 1000000)
        data["permissions"] = self.random.choice(self.PERMISSIONS)
        return data

    def make_dir(self):
        data = self._make(True)
        n = min(self.random.randint(0, 30), self.capacity)
        self.capacity -= n
        data["contents"] = self.make_node()
        return data

    def make_node(self):
        return [self.make_file() for _ in range(self.random.randint(1, 30))]

    def generate(self):
        directories = []
        for _ in range(self.capacity):
            directories.append(self.make_dir())
        out = {
            "type": "directories",
            "directories": directories,
        }
        return out


def make_filesystem_data(n):
    return Generator(n).generate()


if __name__ == "__main__":
    print(make_filesystem_data(1))
