"""
Tests for validators.py
"""
import json
import pytest
from ckan.plugins.toolkit import missing

from ckanext.eaw_theme.validators import repeating_text, repeating_text_output


class TestRepeatingText:
    """Tests for the repeating_text validator."""

    def _make_key(self, field_name="authors"):
        return ("package", field_name)

    def _make_data(self, key, value):
        return {key: value}

    def _make_errors(self, key):
        return {key: []}

    def test_list_of_strings(self):
        """Test case 1: a list of strings is converted to JSON."""
        key = self._make_key()
        data = self._make_data(key, ["Person One", "Person Two"])
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert errors[key] == []
        assert data[key] == '["Person One", "Person Two"]'

    def test_single_string(self):
        """Test case 2: a single string is wrapped in a list and converted to JSON."""
        key = self._make_key()
        data = self._make_data(key, "Person One")
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert errors[key] == []
        assert data[key] == '["Person One"]'

    def test_empty_list(self):
        """Test that an empty list is converted to empty JSON array."""
        key = self._make_key()
        data = self._make_data(key, [])
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert errors[key] == []
        assert data[key] == '[]'

    def test_separate_fields(self):
        """Test case 3: separate fields per index are combined."""
        key = self._make_key()
        data = {
            key: missing,
            ("package", "__extras"): {
                "authors-0": "Person One",
                "authors-1": "Person Two",
                "authors-2": "Person Three",
            },
        }
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert errors[key] == []
        result = json.loads(data[key])
        assert result == ["Person One", "Person Two", "Person Three"]

    def test_separate_fields_with_gaps(self):
        """Test that separate fields with gaps in indices still work."""
        key = self._make_key()
        data = {
            key: missing,
            ("package", "__extras"): {
                "authors-0": "Person One",
                "authors-5": "Person Two",
            },
        }
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert errors[key] == []
        result = json.loads(data[key])
        assert result == ["Person One", "Person Two"]

    def test_separate_fields_with_empty_values(self):
        """Test that empty values in separate fields are ignored."""
        key = self._make_key()
        data = {
            key: missing,
            ("package", "__extras"): {
                "authors-0": "Person One",
                "authors-1": "",
                "authors-2": "Person Two",
            },
        }
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        result = json.loads(data[key])
        assert result == ["Person One", "Person Two"]

    def test_invalid_type_not_list_or_string(self):
        """Test that non-list/string types produce an error."""
        key = self._make_key()
        data = self._make_data(key, 123)
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert len(errors[key]) == 1
        assert "expecting list" in errors[key][0]

    def test_invalid_element_type_in_list(self):
        """Test that non-string elements in the list produce errors."""
        key = self._make_key()
        data = self._make_data(key, ["Valid", 123, "Also Valid"])
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert len(errors[key]) == 1
        assert "invalid type" in errors[key][0]

    def test_preexisting_errors_bails_out(self):
        """Test that validator bails out if there are pre-existing errors."""
        key = self._make_key()
        data = self._make_data(key, ["Person One"])
        errors = {key: ["Pre-existing error"]}

        repeating_text(key, data, errors, {})

        # Data should be unchanged
        assert data[key] == ["Person One"]
        assert errors[key] == ["Pre-existing error"]

    def test_missing_value_no_extras(self):
        """Test missing value with no __extras produces empty JSON array."""
        key = self._make_key()
        data = {key: missing}
        errors = self._make_errors(key)

        repeating_text(key, data, errors, {})

        assert data[key] == '[]'


class TestRepeatingTextOutput:
    """Tests for the repeating_text_output validator."""

    def test_list_passthrough(self):
        """Test that a list is passed through unchanged."""
        value = ["Person One", "Person Two"]
        result = repeating_text_output(value)
        assert result == ["Person One", "Person Two"]

    def test_none_returns_empty_list(self):
        """Test that None returns an empty list."""
        result = repeating_text_output(None)
        assert result == []

    def test_valid_json_string(self):
        """Test that a valid JSON string is parsed to a list."""
        value = '["Person One", "Person Two"]'
        result = repeating_text_output(value)
        assert result == ["Person One", "Person Two"]

    def test_empty_json_array(self):
        """Test that an empty JSON array string returns empty list."""
        value = '[]'
        result = repeating_text_output(value)
        assert result == []

    def test_invalid_json_returns_single_item_list(self):
        """Test that invalid JSON is wrapped in a list."""
        value = "Not valid JSON"
        result = repeating_text_output(value)
        assert result == ["Not valid JSON"]

    def test_empty_string(self):
        """Test that empty string is wrapped in a list."""
        value = ""
        result = repeating_text_output(value)
        assert result == [""]
