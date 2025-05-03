from django.conf import settings


class ScalarSettings:
    """
    Centralized settings access for django-scalar.

    Reads settings prefixed with 'SCALAR_' from django.conf.settings.
    Default values are defined directly within the properties below.
    """

    PREFIX = "SCALAR_"

    @property
    def OPENAPI_URL(self) -> str:
        """
        URL to the OpenAPI schema.
        Defaults to '/api/schema/'.
        """
        # Default value is now the 3rd argument to getattr
        return getattr(settings, self.PREFIX + "OPENAPI_URL", "/api/schema/")

    @property
    def TITLE(self) -> str:
        """
        Title for the API documentation page.
        Defaults to 'Scalar API Reference'.
        """
        return getattr(settings, self.PREFIX + "TITLE", "Scalar API Reference")

    @property
    def THEME(self) -> str | None:
        """
        Theme for the Scalar viewer ('light', 'dark', etc.).
        Defaults to None (Scalar's default theme).
        """
        # The default here is None
        return getattr(settings, self.PREFIX + "THEME", None)

    @property
    def JS_URL(self) -> str:
        """
        URL to the Scalar JS library.
        Defaults to 'https://cdn.jsdelivr.net/npm/@scalar/api-reference'.
        """
        return getattr(
            settings,
            self.PREFIX + "JS_URL",
            "https://cdn.jsdelivr.net/npm/@scalar/api-reference",
        )

    @property
    def PROXY_URL(self) -> str:
        """
        URL for the Scalar proxy service.
        Defaults to an empty string ''.
        """
        return getattr(settings, self.PREFIX + "PROXY_URL", "")

    @property
    def FAVICON_URL(self) -> str:
        """
        URL for the favicon displayed on the documentation page.
        Defaults to '/static/favicon.ico'.
        """
        return getattr(settings, self.PREFIX + "FAVICON_URL", "/static/favicon.ico")

    # --- Example of how you could add more complex/dynamic settings ---
    # @property
    # def IS_SOMETHING_ENABLED(self) -> bool:
    #     # Example: Check if another app is installed
    #     from django.apps import apps
    #     if apps.is_installed('some_dependency'):
    #          # Or read an explicit setting
    #          explicit_setting = getattr(settings, self.PREFIX + "ENABLE_SOMETHING", False)
    #          return explicit_setting
    #     return False


# Create a single, accessible instance of the settings class
app_settings = ScalarSettings()

# Implement PEP 562 for module-level attribute access
# This allows importing settings like `from django_scalar.app_settings import TITLE`
_KNOWN_SETTINGS_ATTRS = {
    "OPENAPI_URL",
    "TITLE",
    "THEME",
    "JS_URL",
    "PROXY_URL",
    "FAVICON_URL",
    # Add any future setting property names here
}


def __getattr__(name: str):
    if name == "app_settings":
        # Allow access to the instance itself if needed, though direct property access is preferred
        return app_settings
    if name in _KNOWN_SETTINGS_ATTRS:
        # Access the corresponding property on the instance
        return getattr(app_settings, name)
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")
