"""
Tests for the app_settings module.
"""

import pytest
from django.test import override_settings

from django_scalar.app_settings import app_settings


class TestScalarSettings:
    """Tests for the ScalarSettings class."""

    def test_default_settings(self):
        """Test that default settings are correctly returned when not overridden."""
        # Check default values
        assert app_settings.OPENAPI_URL == "/api/schema/"
        assert app_settings.TITLE == "Scalar API Reference"
        assert app_settings.THEME is None
        assert (
            app_settings.JS_URL == "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
        )
        assert app_settings.PROXY_URL == ""
        assert app_settings.FAVICON_URL == "/static/favicon.ico"

    @override_settings(SCALAR_OPENAPI_URL="/custom/schema/")
    def test_override_openapi_url(self):
        """Test that SCALAR_OPENAPI_URL setting can be overridden."""
        assert app_settings.OPENAPI_URL == "/custom/schema/"

    @override_settings(SCALAR_TITLE="Custom API Reference")
    def test_override_title(self):
        """Test that SCALAR_TITLE setting can be overridden."""
        assert app_settings.TITLE == "Custom API Reference"

    @override_settings(SCALAR_THEME="dark")
    def test_override_theme(self):
        """Test that SCALAR_THEME setting can be overridden."""
        assert app_settings.THEME == "dark"

    @override_settings(SCALAR_JS_URL="https://example.com/scalar.js")
    def test_override_js_url(self):
        """Test that SCALAR_JS_URL setting can be overridden."""
        assert app_settings.JS_URL == "https://example.com/scalar.js"

    @override_settings(SCALAR_PROXY_URL="https://example.com/proxy/")
    def test_override_proxy_url(self):
        """Test that SCALAR_PROXY_URL setting can be overridden."""
        assert app_settings.PROXY_URL == "https://example.com/proxy/"

    @override_settings(SCALAR_FAVICON_URL="/custom/favicon.ico")
    def test_override_favicon_url(self):
        """Test that SCALAR_FAVICON_URL setting can be overridden."""
        assert app_settings.FAVICON_URL == "/custom/favicon.ico"

    @override_settings(
        SCALAR_OPENAPI_URL="/custom/schema/",
        SCALAR_TITLE="Custom API Reference",
        SCALAR_THEME="dark",
        SCALAR_JS_URL="https://example.com/scalar.js",
        SCALAR_PROXY_URL="https://example.com/proxy/",
        SCALAR_FAVICON_URL="/custom/favicon.ico",
    )
    def test_override_all_settings(self):
        """Test that all settings can be overridden at once."""
        assert app_settings.OPENAPI_URL == "/custom/schema/"
        assert app_settings.TITLE == "Custom API Reference"
        assert app_settings.THEME == "dark"
        assert app_settings.JS_URL == "https://example.com/scalar.js"
        assert app_settings.PROXY_URL == "https://example.com/proxy/"
        assert app_settings.FAVICON_URL == "/custom/favicon.ico"

    def test_module_level_attribute_access(self):
        """Test that module-level attribute access works correctly."""
        from django_scalar.app_settings import (
            OPENAPI_URL,
            TITLE,
            THEME,
            JS_URL,
            PROXY_URL,
            FAVICON_URL,
        )

        assert OPENAPI_URL == app_settings.OPENAPI_URL
        assert TITLE == app_settings.TITLE
        assert THEME == app_settings.THEME
        assert JS_URL == app_settings.JS_URL
        assert PROXY_URL == app_settings.PROXY_URL
        assert FAVICON_URL == app_settings.FAVICON_URL

    def test_attribute_error_for_unknown_attribute(self):
        """Test that accessing an unknown attribute raises AttributeError."""
        with pytest.raises(AttributeError):
            # Access an unknown attribute on the app_settings instance
            app_settings.UNKNOWN_SETTING


class TestEdgeCases:
    """Tests for edge cases in the app_settings module."""

    @override_settings(SCALAR_OPENAPI_URL="")
    def test_empty_string_settings(self):
        """Test that empty string settings are handled correctly."""
        assert app_settings.OPENAPI_URL == ""

    @override_settings(SCALAR_THEME="")
    def test_empty_theme(self):
        """Test that an empty theme string is handled correctly."""
        assert app_settings.THEME == ""

    @override_settings(SCALAR_THEME=False)
    def test_boolean_theme(self):
        """Test that a boolean theme value is handled correctly."""
        assert app_settings.THEME is False
