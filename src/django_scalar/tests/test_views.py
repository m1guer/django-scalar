"""
Tests for the views module.
"""

import pytest
from django.test import RequestFactory
from django.urls import reverse
from bs4 import BeautifulSoup

from django_scalar.views import scalar_viewer


@pytest.mark.django_db
class TestScalarViewer:
    """Tests for the scalar_viewer view function."""

    def test_scalar_viewer_returns_200(self, client):
        """Test that `scalar_viewer` returns a 200 status code."""
        url = reverse("django_scalar:docs")
        response = client.get(url)
        assert response.status_code == 200

    def test_scalar_viewer_uses_correct_template(self, client):
        """Test that `scalar_viewer` uses the correct template."""
        url = reverse("django_scalar:docs")
        response = client.get(url)
        assert "django_scalar/scalar.html" in [t.name for t in response.templates]

    def test_scalar_viewer_context(self):
        """Test that `scalar_viewer` passes the correct context to the template."""
        request = RequestFactory().get("/")
        response = scalar_viewer(request)

        # Check that the context contains the expected variables
        assert "openapi_url" in response.context_data
        assert "title" in response.context_data
        assert "theme" in response.context_data
        assert "scalar_js_url" in response.context_data
        assert "scalar_proxy_url" in response.context_data
        assert "scalar_favicon_url" in response.context_data

        # Check the values of the context variables
        assert response.context_data["openapi_url"] == "/api/schema/"
        assert response.context_data["title"] == "Scalar API Reference"
        assert response.context_data["theme"] is None  # Default theme is None
        assert (
            response.context_data["scalar_js_url"]
            == "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
        )
        assert response.context_data["scalar_proxy_url"] == ""
        assert response.context_data["scalar_favicon_url"] == "/static/favicon.ico"

    def test_scalar_viewer_with_custom_parameters(self):
        """Test that `scalar_viewer` accepts and uses custom parameters."""
        request = RequestFactory().get("/")
        custom_openapi_url = "/custom/schema/"
        custom_title = "Custom API Reference"
        custom_theme = "purple"
        custom_js_url = "https://example.com/scalar.js"
        custom_proxy_url = "https://example.com/proxy/"
        custom_favicon_url = "/custom/favicon.ico"

        response = scalar_viewer(
            request,
            openapi_url=custom_openapi_url,
            title=custom_title,
            scalar_theme=custom_theme,
            scalar_js_url=custom_js_url,
            scalar_proxy_url=custom_proxy_url,
            scalar_favicon_url=custom_favicon_url,
        )

        # Check that the custom parameters are used
        assert response.context_data["openapi_url"] == custom_openapi_url
        assert response.context_data["title"] == custom_title
        assert response.context_data["theme"] == custom_theme
        assert response.context_data["scalar_js_url"] == custom_js_url
        assert response.context_data["scalar_proxy_url"] == custom_proxy_url
        assert response.context_data["scalar_favicon_url"] == custom_favicon_url

    def test_html_content_contains_context_data(self, client):
        """Test that the HTML content contains the expected context data."""
        url = reverse("django_scalar:docs")
        response = client.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Check that the title is correctly set
        assert soup.title.string == "Scalar API Reference"

        # Check that the favicon link is correctly set
        favicon_link = soup.find("link", rel="shortcut icon")
        assert favicon_link["href"] == "/static/favicon.ico"

        # Check that the API reference script has the correct data attributes
        api_reference_script = soup.find("script", id="api-reference")
        assert api_reference_script["data-url"] == "/api/schema/"
        assert api_reference_script["data-proxy-url"] == ""

        # Check that the scalar JS script has the correct source
        scalar_js_script = soup.find_all("script")[-1]  # Last script tag
        assert (
            scalar_js_script["src"]
            == "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
        )

    def test_html_structure_integrity(self, client):
        """Test the overall structure and integrity of the HTML document."""
        url = reverse("django_scalar:docs")
        response = client.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Check basic HTML structure
        assert soup.html["lang"] == "en"
        assert soup.head is not None
        assert soup.body is not None

        # Check for required meta tags
        meta_charset = soup.find("meta", charset="utf-8")
        assert meta_charset is not None

        meta_viewport = soup.find("meta", attrs={"name": "viewport"})
        assert meta_viewport is not None
        assert "width=device-width" in meta_viewport["content"]

        # Check for noscript message
        noscript = soup.find("noscript")
        assert noscript is not None
        assert "Scalar requires Javascript" in noscript.text

        # Check for CSS link
        css_link = soup.find("link", rel="stylesheet")
        assert css_link is not None

    def test_theme_configuration_in_html(self):
        """Test that the theme configuration is correctly added to the HTML when a theme is provided."""
        # Create a request and call scalar_viewer directly with a theme
        request = RequestFactory().get("/")
        response = scalar_viewer(request, scalar_theme="purple")

        # Render the response
        response.render()

        # Parse the HTML content
        soup = BeautifulSoup(response.content.decode(), "html.parser")

        # Find the configuration script (should be after the api-reference script)
        api_reference_script = soup.find("script", id="api-reference")
        config_script = api_reference_script.find_next("script")

        # Check that the configuration script exists and contains the theme
        assert config_script is not None
        assert "configuration" in config_script.text
        assert "theme" in config_script.text
        assert "purple" in config_script.text
