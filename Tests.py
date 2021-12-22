import pytest
from Teodoro import Teodoro

class Tests:

    def test_tellNames(self):
        test = Teodoro(del_speak=False)
        speech, text = test.tellNames()
        assert all(name in speech for name in ["Teodoro", "Teo"]), "speech values has not all allowed names"
        assert all(name in text for name in ["Teodoro", "Teo"]),  "text values has not all allowed names"
        print("Allowed names was set correctly")
        del test

    def test_weather(self):
        test = Teodoro(del_speak=False)
        test.getAction("Qué tiempo hace en Madrid")
        del test