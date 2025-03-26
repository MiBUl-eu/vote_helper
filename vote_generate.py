from dataclasses import dataclass
import person

@dataclass
class vote:
    id: int
    vote_id: int = None
    location: str = None
    max_mustermann: int = 0
    matilda_musterfrau: int = 0


def get_fields():
    persons = []
    persons.append(person.person(name='Max Mustermann', field='max_mustermann', number=0))
    persons.append(person.person(name='Matilda Musterfrau', field='matilda_musterfrau', number=1))
    return persons
