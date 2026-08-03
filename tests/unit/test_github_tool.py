"""Tests for agent/tools/github_tool.py.

REPRODUCTION for issue #50 (issue-catalog id C-10):
    "Add a has_tests boolean to the repo analysis output"
    https://github.com/ascherj/pathreview/issues/50

`GitHubTool` is the agent-side repo analysis tool named in the issue. Its
`_fetch_repo_metadata()` output (github_tool.py lines 99-110) currently reports
`has_readme` but NOT `has_tests`. The test below drives that code path with a
mocked GitHub API and asserts the analysis output exposes a `has_tests`
boolean.

It FAILS today (the key is absent) — that failure IS the reproduction: it
proves the gap is real and pins it to the exact dict the fix must extend. Once
`has_tests` detection is added to `GitHubTool`, this test will pass.
"""

from unittest.mock import MagicMock, patch

import pytest

from agent.tools.github_tool import GitHubTool


@pytest.mark.unit
class TestGitHubToolHasTests:
    """Reproduce the missing has_tests field in the agent repo analysis output."""

    @pytest.fixture
    def tool(self) -> GitHubTool:
        return GitHubTool()

    @patch("agent.tools.github_tool.httpx")
    def test_analysis_output_includes_has_tests(
        self, mock_httpx: MagicMock, tool: GitHubTool
    ) -> None:
        # Mock the repository-metadata GET call.
        mock_get_response = MagicMock()
        mock_get_response.json.return_value = {
            "name": "example-repo",
            "description": "A test repository",
            "language": "Python",
            "stargazers_count": 42,
            "forks_count": 7,
            "open_issues_count": 3,
            "pushed_at": "2024-01-01T00:00:00Z",
            "topics": ["python"],
            "homepage": "",
        }
        mock_get_response.raise_for_status.return_value = None
        mock_httpx.get.return_value = mock_get_response

        # Mock the README HEAD probe used by the existing _has_readme helper.
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_httpx.head.return_value = mock_head_response

        result = tool.execute({"github_username": "octocat", "repo_name": "example-repo"})

        assert result.success is True

        # Regression guard: the existing has_readme field should still be present.
        assert "has_readme" in result.data

        # Issue #50: the analysis output MUST expose a has_tests boolean.
        # This assertion FAILS today (key is absent) — that is the reproduction.
        assert (
            "has_tests" in result.data
        ), "has_tests missing from GitHubTool analysis output — see issue #50"
        assert isinstance(result.data["has_tests"], bool)
