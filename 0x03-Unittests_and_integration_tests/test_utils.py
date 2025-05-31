#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    This class tests the access_nested_map function from utils.py
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """
        This method tests the access nested map and asserts if the nested
        map and path params are equal to expected.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",), "a"),
            ({"a": 1}, ("a", "b"), "b"),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        This method tests the access nested map
        and asserts if the nested
        map and path params and raises keyerror
        indicating the wrong key
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Tests the utils.get_json function.
    """

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """
        Test that utils.get_json returns the expected result
        without making external HTTP calls.

        This method uses unittest.mock.patch to mock 'requests.get'.
        It parametrizes test URLs and payloads to ensure the function
        behaves correctly for different inputs.
        It asserts that the mocked 'get' method is called exactly once
        with the correct URL and that the output matches the expected payload.
        """
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test that a memoized method is only called once."""

        class TestClass:
            """Helper class to test memoization behaviour."""

            def a_method(self):
                """Method to be mocked during test."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method()."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mck_methd:
            obj = TestClass()
            result_one = obj.a_property
            result_two = obj.a_property

            self.assertEqual(result_one, 42)
            self.assertEqual(result_two, 42)

            mck_methd.assert_called_once()
