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
        This method tests the access nested map and asserts if the nested
        map and path params and raises keyerror indicating the wrong key
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Tests the test_get_json() method to make sure it returns expected results.
    """

    # replaces requests.get in th utils with mock object during the test
    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        # mock_get is the mocked version of requests.get, passed in by @patch
        """
        Test the utils.get_json function returns the expected result without making external http calls
        """
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:

            mock_response = Mock()
            # this object will simulate http response object returned by requests.get
            mock_response.json.return_value = test_payload
            # configure .json() of the mock response to return the expected JSON `test_payload`
            mock_get.return_value = mock_response
            # sets the mocked requests.get to return the mock_response when called

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """This class implements test for utils.memoize function"""

    def test_memoize(self):
        """
        Tests that a method decorated with @memoize calls its underlying logic
        only once, caching the result for subsequent calls.
        """

        class TestClass:
            """
            Tests the behaviour of the memoize decorator
            """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            object = TestClass()

            # 1. First call to a_property should call a_method
            result_one = object.a_property

            # 2. Second call to a_property should use cached value not call a_method
            result_two = object.a_property

            # Assert both results are correct
            self.assertEqual(result_one, 42)
            self.assertEqual(result_two, 42)

            mock_method.assert_called_once()
