from django.http import HttpResponse
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

scalar_theme = """
/* basic theme */
.light-mode {
  --scalar-color-1: #2a2f45;
  --scalar-color-2: #757575;
  --scalar-color-3: #8e8e8e;
  --scalar-color-accent: #009485;

  --scalar-background-1: #fff;
  --scalar-background-2: #fcfcfc;
  --scalar-background-3: #f8f8f8;
  --scalar-background-accent: #ecf8f6;

  --scalar-border-color: rgba(0, 0, 0, 0.1);
}
.dark-mode {
  --scalar-color-1: rgba(255, 255, 255, 0.9);
  --scalar-color-2: rgba(255, 255, 255, 0.62);
  --scalar-color-3: rgba(255, 255, 255, 0.44);
  --scalar-color-accent: #00ccb8;

  --scalar-background-1: #1f2129;
  --scalar-background-2: #282a35;
  --scalar-background-3: #30323d;
  --scalar-background-accent: #223136;

  --scalar-border-color: rgba(255, 255, 255, 0.1);
}
/* Document Sidebar */
.light-mode .t-doc__sidebar {
  --sidebar-background-1: var(--scalar-background-1);
  --sidebar-item-hover-color: currentColor;
  --sidebar-item-hover-background: var(--scalar-background-2);
  --sidebar-item-active-background: var(--scalar-background-accent);
  --sidebar-border-color: var(--scalar-border-color);
  --sidebar-color-1: var(--scalar-color-1);
  --sidebar-color-2: var(--scalar-color-2);
  --sidebar-color-active: var(--scalar-color-accent);
  --sidebar-search-background: transparent;
  --sidebar-search-border-color: var(--scalar-border-color);
  --sidebar-search--color: var(--scalar-color-3);
}

.dark-mode .sidebar {
  --sidebar-background-1: var(--scalar-background-1);
  --sidebar-item-hover-color: currentColor;
  --sidebar-item-hover-background: var(--scalar-background-2);
  --sidebar-item-active-background: var(--scalar-background-accent);
  --sidebar-border-color: var(--scalar-border-color);
  --sidebar-color-1: var(--scalar-color-1);
  --sidebar-color-2: var(--scalar-color-2);
  --sidebar-color-active: var(--scalar-color-accent);
  --sidebar-search-background: transparent;
  --sidebar-search-border-color: var(--scalar-border-color);
  --sidebar-search--color: var(--scalar-color-3);
}

/* advanced */
.light-mode {
  --scalar-button-1: rgb(49 53 56);
  --scalar-button-1-color: #fff;
  --scalar-button-1-hover: rgb(28 31 33);

  --scalar-color-green: #009485;
  --scalar-color-red: #d52b2a;
  --scalar-color-yellow: #ffaa01;
  --scalar-color-blue: #0a52af;
  --scalar-color-orange: #953800;
  --scalar-color-purple: #8251df;

  --scalar-scrollbar-color: rgba(0, 0, 0, 0.18);
  --scalar-scrollbar-color-active: rgba(0, 0, 0, 0.36);
}
.dark-mode {
  --scalar-button-1: #f6f6f6;
  --scalar-button-1-color: #000;
  --scalar-button-1-hover: #e7e7e7;

  --scalar-color-green: #00ccb8;
  --scalar-color-red: #e5695b;
  --scalar-color-yellow: #ffaa01;
  --scalar-color-blue: #78bffd;
  --scalar-color-orange: #ffa656;
  --scalar-color-purple: #d2a8ff;

  --scalar-scrollbar-color: rgba(255, 255, 255, 0.24);
  --scalar-scrollbar-color-active: rgba(255, 255, 255, 0.48);
}
:root {
  --scalar-radius: 3px;
  --scalar-radius-lg: 6px;
  --scalar-radius-xl: 8px;
}
.scalar-card:nth-of-type(3) {
  display: none;
}"""


def scalar_viewer(request):
    openapi_url = "/api/schema/"
    title = "Scalar Api Reference"
    scalar_js_url = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
    scalar_proxy_url = ""
    scalar_favicon_url = "/static/favicon.ico"
  
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" href="{scalar_favicon_url}">
        <style>
        body {{
            margin: 0;
            padding: 0;
        }}
        </style>
        <style>
         {scalar_theme} #this can be removed if you want to use custom themes or the defaults that scalar already provides.
        </style>
    </head>
    <body>
        <noscript>
            Scalar requires Javascript to function. Please enable it to browse the documentation.
        </noscript>
        <script
            id="api-reference"
            data-url="{openapi_url}"
            data-proxy-url="{scalar_proxy_url}"
            >
        </script>
        #  <script>
        # var configuration = {{
        #    # authentication: {{
        #    #    preferredSecurityScheme: 'apiKey',
        #    #    apiKey: {{
        #    #       token: 'Token {{token}}',
        #    #    }}
        #    # }}
        #    # theme:'purple' # if {scalar_theme} is on top of it, the defaults themes will not work.
        # }};
        # document.getElementById('api-reference').dataset.configuration =
        #     JSON.stringify(configuration);
        # </script>
        <script src="{scalar_js_url}"></script>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns_scalar = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"), # im using drf_spectacular and is the one that i tested with. ps: this endpoint need to be the same from {openapi_url}
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ), # is not needed but if you want can keep it.
    path("api/docs/", scalar_viewer, name="docs"), # scalar view.
]
