import unittest
import sys
from unittest.mock import patch 
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.insert(0, 'C:/Users/fredy/Downloads/Coding_Projects/Rag/NLP/src')

from new_videos import get_video_id

class TestScraper(unittest.TestCase):

    def test_get_video_id(self):
        self.assertEqual(get_video_id("https://www.youtube.com/watch?v=abc123"), "abc123")

    


if __name__ == '__main__':
    unittest.main()

