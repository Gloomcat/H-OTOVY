from contacts_book import ContactsBook
from notes_manager import NotesManager
from assistant import Assistant

if __name__ == "__main__":
    with ContactsBook() as contacts, NotesManager() as notes:
        assistant_bot = Assistant(contacts, notes)
        assistant_bot.run()
