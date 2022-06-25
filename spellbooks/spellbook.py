class SpellBook():
    def __init__(self, args):
        self.spell_list = []
        if args.name:
            self.read_spellbook(args.name)
        else:
            print("This is not yet implemented, please specify a name.")
            quit()


    def read_spellbook(self, name):
        self.name = name
        try:
            with open(name + "-Spellbook.txt") as spellbook:
                for line in spellbook:
                    self.read_spell_line(line)
        except IOError:
            print(name + "-Spellbook.txt was not found.")
            quit(2)
        self.read_ignorelist()


    def read_ignorelist(self):
        try:
            with open(self.name + "-Ignore.txt") as spellbook:
                for line in spellbook:
                    self.read_spell_line(line)
        except IOError:
            pass


    def read_spell_line(self, line):
        split_line = line.split()
        try:
            level = split_line[0]
            spell_name = ' '.join(split_line[1:]).strip()
            self.spell_list.append(BookSpell(spell_name, level))
        except IndexError:
            if split_line != []:
                print("WARNING: This line was ignored")
                print(split_line)


class BookSpell():
    def __init__(self, name, level):
        self.name = name
        self.level = level
