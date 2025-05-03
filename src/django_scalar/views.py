from django.template.response import TemplateResponse

from .app_settings import OPENAPI_URL, TITLE, THEME, JS_URL, PROXY_URL, FAVICON_URL


def scalar_viewer(
    request,
    openapi_url=None,
    title=None,
    scalar_theme=None,
    scalar_js_url=None,
    scalar_proxy_url=None,
    scalar_favicon_url=None,
):
    """
    Render the Scalar API Reference viewer.

    Defaults are sourced from django_scalar.app_settings.

    Args:
        request: The Django request object
        openapi_url: URL to the OpenAPI schema (defaults to `SCALAR_OPENAPI_URL` setting)
        title: Title for the API documentation (defaults to `SCALAR_TITLE` setting)
        scalar_theme: Theme for the Scalar viewer (defaults to `SCALAR_THEME` setting)
        scalar_js_url: URL to the Scalar JS library (defaults to `SCALAR_JS_URL` setting)
        scalar_proxy_url: URL for the Scalar proxy (defaults to `SCALAR_PROXY_URL` setting)
        scalar_favicon_url: URL for the favicon (defaults to `SCALAR_FAVICON_URL` setting)

    Returns:
        TemplateResponse: The rendered Scalar viewer
    """
    # Use provided view arguments or fall back to app_settings properties
    # Using "is not None" check allows passing empty strings or False if needed for future settings
    final_openapi_url = openapi_url if openapi_url is not None else OPENAPI_URL
    final_title = title if title is not None else TITLE
    final_theme = scalar_theme if scalar_theme is not None else THEME
    final_js_url = scalar_js_url if scalar_js_url is not None else JS_URL
    final_proxy_url = scalar_proxy_url if scalar_proxy_url is not None else PROXY_URL
    final_favicon_url = (
        scalar_favicon_url if scalar_favicon_url is not None else FAVICON_URL
    )

    context = {
        "openapi_url": final_openapi_url,
        "title": final_title,
        "theme": final_theme,
        "scalar_js_url": final_js_url,
        "scalar_proxy_url": final_proxy_url,
        "scalar_favicon_url": final_favicon_url,
    }
    return TemplateResponse(request, "django_scalar/scalar.html", context)
