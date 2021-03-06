# Import first to fix paths.
import config as config

from locale_redirect_middleware import LocaleRedirectMiddleware
from static_file_server_app import StaticFileServerApplication
from sheets_auth_middleware import SheetsAuthMiddleware
from protorpc.wsgi import service
import access_requests
import cors
import logging
import protected_middleware
import os
import search_app
import users
import webapp2
import yaml

build_server_config = config.instance()

backend = webapp2.WSGIApplication([
    access_requests.FormResponseHandler.mapping(),
    ('/_grow/access-requests/approve/(.*)', access_requests.ApproveAccessRequestHandler),
    ('/_grow/access-requests/process', access_requests.ProcessHandler),
    ('/_grow/access-requests', access_requests.ManageAccessHandler),
    ('/_grow/users/csv', access_requests.DownloadCsvHandler),
    ('/_grow/users/import', access_requests.ImportFromSheetsHandler),
    ('/_grow/users/(.*)', access_requests.ManageUserHandler),
    ('/_grow/users', access_requests.ManageUsersHandler),
    ('/_grow/protected/cache-sheets', protected_middleware.CacheSheetsHandler),
    ('/_grow/search/index', search_app.IndexHandler),
    ('/_ah/warmup', search_app.IndexHandler),
], config=build_server_config)

root = build_server_config['root']
locales = build_server_config['locales']
default_locale = build_server_config['default_locale']
static_paths = build_server_config['static_paths']

_static_app = StaticFileServerApplication(root=root)
_locale_app = LocaleRedirectMiddleware(
        _static_app, root=root, locales=locales,
        default_locale=default_locale)
_protected_app = protected_middleware.ProtectedMiddleware(_locale_app, config=build_server_config)
app = SheetsAuthMiddleware(
        _protected_app, static_paths=static_paths,
        config=build_server_config)

api = cors.CorsMiddleware(service.service_mappings([
    ('/_grow/api/users.*', users.UsersService),
    ('/_grow/api/search.*', search_app.SearchService),
]))
