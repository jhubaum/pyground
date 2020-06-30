import sys
import re
import os

NOTE_REGEX = re.compile(r'\n-+\n\n')

class Note:
    def __init__(self, title):
        self.title = title
        self.notes = []
        self.bookmarks = []

    def add_entry(self, note_type, content):
        if note_type == 'Bookmark':
            self.add_bookmark(content)
            return

        if note_type == 'Highlight':
            self.add_note(content)
            return

        self.add_note(content, content[content.find(':')+2: content.find('\n')])

    def add_bookmark(self, content):
        self.bookmarks.append(content.split(':')[0])

    def add_note(self, content, note=None):
        begin = content.find('\"') + 1
        end = content.find('\"', begin)

        self.notes.append((content[begin:end], note))

    def write_to_file(self, path='.', print_bookmarks=True):
        filename = re.sub(r'\W+', '', self.title.lower().replace(' ', '_')) + '.org'
        with open(os.path.join(path, filename), 'w+', encoding='utf-8') as f:
            f.write('-----\n')
            f.write(f'title: {self.title}\n')
            f.write('-----\n\n* Highlights\n')

            for highlight, note in self.notes:
                f.write(highlight)
                f.write('\n')
                if note is not None:
                    f.write(f'-> {note}\n')
                f.write('\n')

            if print_bookmarks:
                f.write('\n* Bookmarks\n')
                for b in self.bookmarks:
                    f.write(b)
                    f.write('\n')

            f.write('\0')


def parse_notes(string):
    notes = dict()
    for i, n in enumerate(NOTE_REGEX.split(string)):
        if not n.strip():
            # reached end of file
            break

        split_index = n.find('\n')
        title = n[0:split_index]
        note_type, rest = n[split_index+1:].split(maxsplit=1)

        if title not in notes:
            notes[title] = Note(title)
        notes[title].add_entry(note_type, rest)

    return notes


def selection_menu(options):
    print('Select titles to parse')
    print('--------')
    for i, n in enumerate(options):
        print(f"{i}: {n}")
    sel = input("Enter selection. Split multiple values with space or leave empty to select everything. Enter \'c\' to cancel: ")

    if sel == 'c':
        return

    if len(sel.strip()) == 0:
        for o in options:
            yield o
        return

    tmp = set()
    for s in sel.split(' '):
        try:
            tmp.add(int(s))
        except:
            pass

    for i, o in enumerate(options):
        if i in tmp:
            yield o


def parse_file(filename):
    with open(filename, encoding='utf-8') as f:
        notes = parse_notes(f.read())

        for k in selection_menu(notes.keys()):
            notes[k].write_to_file()


if __name__ == '__main__':
    if len(sys.argv) == 0:
        print(f"usage: {sys.argv[0]} <filename>")
    else:
        parse_file(sys.argv[1])
