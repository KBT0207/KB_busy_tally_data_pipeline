import unittest
from unittest.mock import MagicMock, patch
from busy import rep1

class TestStartBusy(unittest.TestCase):

    @patch('rep1.pg')
    #@patch('rep1.time.sleep')
    def test_start_busy(self, mock_pg):
        # Mocking the return values and behaviors of pyautogui functions
        mock_pg.locateCenterOnScreen.return_value = (100, 100)

        # Call the function
        rep1.start_busy()

        # Assertions
        mock_pg.hotkey.assert_any_call("win", "r")
        mock_pg.typewrite.assert_any_call("mstsc")
        mock_pg.press.assert_any_call("enter")
        mock_pg.typewrite.assert_any_call("192.168.0.233:7217")
        mock_pg.press.assert_any_call("enter")
        mock_pg.typewrite.assert_any_call("GA@ur0107$")
        mock_pg.click.assert_called_with((100, 100))
        mock_pg.hotkey.assert_any_call("win", "d")
        mock_pg.doubleClick.assert_called_with((100, 100), duration=0.3)
        #mock_time_sleep.assert_any_call(2)

if __name__ == '__main__':
    unittest.main()
