class LetterFilter():
    def __init__(self, s):
        self.s = list(s)
        self.vowels = "a","e","i","o","u"

    def filter_vowels(self):
        for count, letter in enumerate(self.s):
            if letter in self.vowels:
                self.s.pop(count)
        word = "".join(self.s)
        return word

    def filter_consonants(self):
        for count, letter in enumerate(self.s):
            if letter not in self.vowels:
                self.s.pop(count)
        word = "".join(self.s)
        
        return word