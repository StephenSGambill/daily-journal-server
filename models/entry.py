class Entry():
    """Class that defines the properties for a journal entry"""

    def __init__(self, id, concept, entry, mood_id, date):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.mood = None
        self.date = date
