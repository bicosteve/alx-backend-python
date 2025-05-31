import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand(
        [
            ("google", {"login": "google", "id": 1}),
            ("abc", {"login": "abc", "id": 2}),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)

        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url retuns the correct repos URL."""
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list and mocks are called once."""
        test_repos_payload = [
            {"name": "repo_one", "license": {"key": "mit"}},
            {"name": "repo_two", "license": {"key": "apache-2.0"}},
            {"name": "repo_three", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = test_repos_payload
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/testorg/repos",
        ) as mock_repos_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected_repos = ["repo_one", "repo_two", "repo_three"]
            self.assertEqual(result, expected_repos)

            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean value."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([{"org_payload": TEST_PAYLOAD}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get and mock .json responses."""

        cls.get_patcher = patch("utils.requests.get")
        mocked_get = cls.get_patcher.start()

        # Create a side_effect function to match URLs
        def side_effect(url):
            mock_response = MagicMock()
            if url == f"https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mocked_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down patcher."""
        cls.get_patcher.stop()
