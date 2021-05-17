import logging
from unittest import TestCase, mock

from generate_artists import find_multiple_artists

"""
Stuff to test:
Partition:
    - Name dne
    - Name exists
    - Multiple names exist

    - Artists joined w/o /
    - Malformed input

"""


class Test(TestCase):
    thelist = ["AC/DC", "Au/Ra"]

    @mock.patch('generate_artists.logger')
    def test_NameDoesNotExist(self, *_):
        result = find_multiple_artists("Kygo/K-391/Alan Walker/Mangoo", self.thelist)
        self.assertTupleEqual(result, ("Kygo", "K-391", "Alan Walker", "Mangoo"))

    @mock.patch('generate_artists.logger')
    def test_OneNameExists(self, *_):
        result = find_multiple_artists("Kygo/K-391/Alan Walker/Au/Ra/Mangoo", self.thelist)
        self.assertTupleEqual(result, ("Au/Ra", "Kygo", "K-391", "Alan Walker", "Mangoo"))

    @mock.patch('generate_artists.logger')
    def test_MultipleNamesExist(self, *_):
        result = find_multiple_artists("Kygo/K-391/Alan Walker/Au/Ra/Mangoo/AC/DC", self.thelist)
        self.assertSetEqual(set(result), {"Au/Ra", "AC/DC", "Kygo", "K-391", "Alan Walker", "Mangoo"})

    @mock.patch('generate_artists.logger')
    def test_withoutSlash(self, *_):
        result = find_multiple_artists("Kygo/K-391/Alan Walker Au/Ra/Mangoo", self.thelist)
        self.assertSetEqual(set(result), {"Ra", "Kygo", "K-391", "Alan Walker Au", "Mangoo"})

    @mock.patch('generate_artists.logger')
    def test_OneArtist(self, *_):
        result = find_multiple_artists("Kygo Walker", self.thelist)
        self.assertSetEqual(set(result), {"Kygo Walker"})

    @mock.patch('generate_artists.logger')
    def test_TwoArtist(self, *_):
        result = find_multiple_artists("Kygo/Alan Walker", self.thelist)
        self.assertSetEqual(set(result), {"Kygo", "Alan Walker"})

    @mock.patch('generate_artists.logger')
    def test_TwoArtistFromList(self, *_):
        result = find_multiple_artists("Kygo/AC/DC", self.thelist)
        self.assertSetEqual(set(result), {"Kygo", "AC/DC"})
