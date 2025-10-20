import unittest
from src.chatbot import EkkoChatbot

class TestEkkoChatbot(unittest.TestCase):
    def setUp(self):
        self.bot = EkkoChatbot()

    def test_knowledge_base(self):
        self.assertEqual(self.bot.get_response("What is EKKO?"), 
                         "EKKO is your personal offline AI assistant for students.")

    def test_calculation(self):
        self.assertEqual(self.bot.get_response("2+3"), "The result is 5")

    def test_gpt2_response(self):
        response = self.bot.get_response("Hello")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

if __name__ == "__main__":
    unittest.main()
