# Django Scalar API Reference

[![PyPI version](https://badge.fury.io/py/django-scalar.svg)](https://badge.fury.io/py/django-scalar) <!-- TODO: Add actual PyPI link/badge if published -->

A simple Django app to integrate the beautiful [Scalar API Reference](https://github.com/scalar/scalar) viewer.

## Features

*   Easily display your OpenAPI schema using Scalar.
*   Configurable via Django settings.
*   Allows multiple, differently configured Scalar instances within one project.
*   Supports custom themes and JS library locations.

## Installation

1.  Install the package using `pip` (or your preferred package manager like `uv`):

    ```bash
    pip install django-scalar
    # or
    uv pip install django-scalar
    ```

2.  Add `django_scalar` to your `INSTALLED_APPS` in your Django project's `settings.py`:

    ```python
    # settings.py
    INSTALLED_APPS = [
        # ... other apps
        'django_scalar',
        # ... other apps
    ]
    ```

## Quick Start

1.  Ensure you have an OpenAPI schema file (e.g., `openapi.yaml` or `schema.json`) served by your Django project or accessible via a URL. A common pattern is to use a library like `drf-spectacular` to generate and serve this at a specific path.

2.  Add the Scalar view to your project's `urls.py`:

    ```python
    # project/urls.py
    from django.urls import path
    from django_scalar import views as scalar_views

    urlpatterns = [
        # ... other url patterns
        # Add the Scalar view, assuming your schema is at /api/schema/
        path('api/docs/', scalar_views.scalar_viewer, name='scalar_api_docs'),
        # Make sure you have a view serving your schema at the configured URL
        # Example using drf-spectacular:
        # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    ]
    ```

3.  Visit `/api/docs/` in your browser to see the Scalar API Reference.

## Configuration

You can customize the Scalar view by adding `SCALAR_` prefixed settings to your Django project's `settings.py`. If not set, sensible defaults are used.

Available settings:

*   `SCALAR_OPENAPI_URL` (str): The URL to your OpenAPI schema file.
    *   Default: `"/api/schema/"`
*   `SCALAR_TITLE` (str): The title displayed on the Scalar page tab and header.
    *   Default: `"Scalar API Reference"`
*   `SCALAR_THEME` (str | None): The theme for the Scalar viewer (e.g., `'light'`, `'dark'`, `'moonlight'`, `'purplehaze'`, `'eclipse'`, `'solarized'`). Set to `None` to use Scalar's default theme detection.
    *   Default: `None`
*   `SCALAR_JS_URL` (str): The URL for the Scalar JavaScript library bundle. Use this to point to a specific version or a self-hosted copy.
    *   Default: `"https://cdn.jsdelivr.net/npm/@scalar/api-reference"`
*   `SCALAR_PROXY_URL` (str): The URL to use for the Scalar API proxy service, if needed.
    *   Default: `""` (empty string, proxy disabled)
*   `SCALAR_FAVICON_URL` (str): The URL for the favicon displayed on the documentation page browser tab.
    *   Default: `"/static/favicon.ico"`

**Example `settings.py`:**

```python
# settings.py

# ... other settings

SCALAR_TITLE = "My Awesome Project API"
SCALAR_OPENAPI_URL = "/api/v1/openapi.json"
SCALAR_THEME = "dark"

# Make sure you serve your schema at SCALAR_OPENAPI_URL
# REST_FRAMEWORK = {
#     'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
# }
# SPECTACULAR_SETTINGS = {
#     'TITLE': SCALAR_TITLE, # Keep titles consistent
#     'VERSION': '1.0.0',
#     # etc.
# }
```

### Using Multiple Instances

The `scalar_viewer` view function accepts arguments that allow you to override the global settings defined in `settings.py`. This is useful if you need to display multiple, different API documentation pages within the same project. A prominent example of this is publishing different API versions or internal vs. external APIs (_coming soon_: setting of separate authentication requirements).

You can pass these arguments as the third item (a dictionary) in the `path()` definition in your `urls.py`.

**Available View Arguments:**

*   `openapi_url` (str): Overrides `SCALAR_OPENAPI_URL`.
*   `title` (str): Overrides `SCALAR_TITLE`.
*   `theme` (str | None): Overrides `SCALAR_THEME`.
*   `scalar_js_url` (str): Overrides `SCALAR_JS_URL`.
*   `scalar_proxy_url` (str): Overrides `SCALAR_PROXY_URL`.
*   `scalar_favicon_url` (str): Overrides `SCALAR_FAVICON_URL`.

**Example for Multiple Instances:`urls.py`**

```python
# project/urls.py
from django.urls import path
from django_scalar import views as scalar_views

# Assuming you have views to serve different schemas:
# from myapp.views import serve_v1_schema, serve_v2_schema

urlpatterns = [
    # Instance 1: Public API v1 (using default settings mostly)
    # Assumes SCALAR_OPENAPI_URL points to the v1 schema or is overridden here
    path('api/v1/docs/', scalar_views.scalar_viewer, {
        'title': 'Public API v1 Docs',
        'openapi_url': '/api/v1/schema.json'  # Explicitly set schema URL for v1
        # theme will use SCALAR_THEME or default if not set
    }, name='scalar_v1'),

    # Instance 2: Public API v2 (different title, schema, maybe theme)
    path('api/v2/docs/', scalar_views.scalar_viewer, {
        'title': 'Public API v2 Docs',
        'openapi_url': '/api/v2/schema.yaml',  # Point to the v2 schema
        'theme': 'moonlight',  # Use a specific theme for v2
    }, name='scalar_v2'),

    # Instance 3: Internal API (different title, schema, uses default theme)
    path('internal/api/docs/', scalar_views.scalar_viewer, {
        'title': 'Internal Services API',
        'openapi_url': '/internal/api/schema.json',
        # theme will use SCALAR_THEME or default
        # js_url, proxy_url, favicon_url use defaults from settings
    }, name='scalar_internal'),

    # --- Your views serving the schemas ---
    # path('api/v1/schema.json', serve_v1_schema, name='schema_v1'),
    # path('api/v2/schema.yaml', serve_v2_schema, name='schema_v2'),
    # path('internal/api/schema.json', serve_internal_schema, name='schema_internal'),

    # ... other url patterns
]
```
Now, visiting `/api/v1/docs/`, `/api/v2/docs/`, and `/internal/api/docs/` will show differently configured Scalar instances.

## Contributing
Contributions are always welcome! Please feel free to open an issue or submit a pull request.
