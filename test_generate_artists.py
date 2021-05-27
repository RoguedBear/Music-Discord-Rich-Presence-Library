import logging
from unittest import TestCase, mock

from generate_artists import find_multiple_artists, get_album_and_artist

"""
Stuff to test:
Partition:
    - Name dne
    - Name exists
    - Multiple names exist

    - Artists joined w/o /
    - Malformed input

"""


class TestForwardSlashFormat(TestCase):
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


"""
Stuff to test:
    - No artist
    - 1 Artist
    - Multiple Artist
"""


class TestDoubleEqualFormat(TestCase):
    thelist = """AC/DC
Au/Ra
Yusuf / Cat Stevens"""
#     thelist = ["AC/DC", "Au/Ra"]
    
    class MockResponse:
        text = """AC/DC
Au/Ra
Yusuf / Cat Stevens""" 

    @mock.patch('generate_artists.logger')
    def test_ZeroArtist(self, *_):
        result = get_album_and_artist("Never Gonna Give you up==125")
        self.assertTupleEqual(result, ("Never Gonna Give you up", ("Unknown Artist",)))

    @mock.patch('generate_artists.logger')
    @mock.patch('requests.get', return_value=MockResponse)
    def test_OneArtist(self, *_):
        result = get_album_and_artist("Never Gonna Give you up==125==Rick Astley")
        self.assertTupleEqual(result, ("Never Gonna Give you up", ("Rick Astley",)))

    @mock.patch('generate_artists.logger')
    @mock.patch('requests.get', return_value=MockResponse)
    def test_OneArtistOtherfmt(self, *_):
        result = get_album_and_artist("Made Up Tunes==125==Rick Astley/Au/Ra/Kygo")
        self.assertTupleEqual(result, ("Made Up Tunes", ("Au/Ra","Rick Astley", "Kygo")))

    @mock.patch('generate_artists.logger')
    @mock.patch('requests.get', return_value=thelist)
    @mock.patch('time.sleep', return_value=1)
    def test_downloadFailure(self, *_):
        result = get_album_and_artist("Made Up Tunes==125==Rick Astley/Au/Ra/Kygo")
        self.assertTupleEqual(result, ("Made Up Tunes", ("Rick Astley", "Au", "Ra", "Kygo")))



    @mock.patch('generate_artists.logger')
    @mock.patch('requests.get', return_value=MockResponse)
    def test_MoreThanOneArtist(self, *_):
        result = get_album_and_artist("Suicide Squad: The Album==12==Skrillex==Rick Ross==Lil Wayne==Wiz "
                                      "Khalifa==Imagine Dragons==X Ambassadors==Logic==Ty Dolla $ign==Twenty One "
                                      "Pilots==Action Bronson==Mark Ronson==Dan Auerbach==Kehlani==Kevin "
                                      "Gates==SAYGRACE==G-Eazy==Eminem==Skylar Grey==Grimes==Panic! At The "
                                      "Disco==War==Creedence Clearwater Revival==ConfidentialMX==Becky Hanson")
        self.assertTupleEqual(result, ("Suicide Squad: The Album", tuple("Skrillex==Rick Ross==Lil Wayne==Wiz "
                                                                         "Khalifa==Imagine Dragons==X "
                                                                         "Ambassadors==Logic==Ty Dolla $ign==Twenty "
                                                                         "One Pilots==Action Bronson==Mark Ronson==Dan "
                                                                         "Auerbach==Kehlani==Kevin "
                                                                         "Gates==SAYGRACE==G-Eazy==Eminem==Skylar "
                                                                         "Grey==Grimes==Panic! At The "
                                                                         "Disco==War==Creedence Clearwater "
                                                                         "Revival==ConfidentialMX==Becky "
                                                                         "Hanson".split("=="))))
