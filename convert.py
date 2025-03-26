f = open("choices.txt", "r")

c = open("vote_generate.py", "w")
c.write("from dataclasses import dataclass\nimport person\n\n@dataclass\nclass vote:\n")
c.write("    id: int\n")
c.write("    vote_id: int = None\n") 
c.write("    location: str = None\n")
lines = []

for line in f:
    if line == "\n":
        continue
    c.write("    " + line.strip().lower().replace('-', '_').replace(' ', '_').replace('ß', 'ss').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue') + ": int = 0\n")
    lines.append(line.strip())
c.write("\n\n")
c.write("def get_fields():\n")
c.write("    persons = []\n")
for i, line in enumerate(lines):
    if line == "\n":
        continue
    c.write("    persons.append(person.person(name='" + line.strip() + "', field='" + line.strip().lower().replace('-', '_').replace(' ', '_').replace('ß', 'ss').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue') + "', number=" + str(i) + "))\n")

c.write("    return persons\n")

c.close()
f.close()