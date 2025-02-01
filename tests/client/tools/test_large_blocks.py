import unittest
from unittest.mock import patch, MagicMock
from wcgw.client.tools import BASH_STATE, execute_bash
from wcgw.types_ import BashCommand

class TestLargeBlocks(unittest.TestCase):
    @patch("wcgw.client.tools.BASH_STATE")
    def test_execute_bash_large_output(self, mock_bash_state):
        # Setup mock shell
        mock_shell = MagicMock()
        mock_shell.before = "large output\n" * 1000
        mock_shell.expect.return_value = 0

        # Setup mock BASH_STATE
        mock_bash_state.shell = mock_shell
        mock_bash_state.state = "repl"
        mock_bash_state.update_cwd.return_value = "/test/dir"
        mock_bash_state.update_repl_prompt.return_value = False
        mock_bash_state.prompt = "TEST_PROMPT>"
        mock_bash_state.bash_command_mode.allowed_commands = "all"
        mock_bash_state.ensure_env_and_bg_jobs.return_value = 0

        # Mock get_status() function
        def mock_get_status():
            return "\n\nstatus = process exited\ncwd = /test/dir"

        with patch("wcgw.client.tools.get_status", side_effect=mock_get_status):
            # Test command with large output
            command = BashCommand(command="generate_large_output")
            output, cost = execute_bash(MagicMock(), command, max_tokens=100, timeout_s=1)

            # Verify output
            self.assertIn("large output", output)
            self.assertEqual(cost, 0)

if __name__ == "__main__":
    unittest.main()