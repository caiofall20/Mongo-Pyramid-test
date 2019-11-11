from pyramid.config import Configurator

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

# from pymongo import MongoClient

# def main(global_config, **settings):
#     config = Configurator(settings=settings)

#     db_url = urlparse(settings['mongo_uri'])
#     config.registry.db = MongoClient(
#        host=db_url.hostname,
#        port=db_url.port,
#     )
#     def add_db(request):
#         db = config.registry.db[db_url.path[1:]]
#         if db_url.username and db_url.password:
#             db.authenticate(db_url.username, db_url.password)
#         return db
#     config.add_request_method(add_db, 'db', reify=True)
from gridfs import GridFS
from pymongo import MongoClient

def main(global_config, **settings):
    # """ This function returns a Pyramid WSGI application.
    # """
     with Configurator(settings=settings) as config:
    #     config.include('pyramid_jinja2')
    #     config.include('.routes')

        db_url = urlparse(settings['mongo_uri'])
        config.registry.db = MongoClient(
            host='mongodb+srv://admin:fac280895@cluster0-cieon.mongodb.net/test?retryWrites=true&w=majority'
        )

        def add_db(request):
            db = config.registry.db[db_url.path[1:]]
            return db
        
        def add_fs(request):
            return GridFS(request.db)

        config.add_request_method(add_db, 'db', reify=True)
        config.add_request_method(add_fs, 'fs', reify=True)

        config.scan()
    return config.make_wsgi_app()    

    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route('add', '/add')
    config.add_route('rank', '/rank')
    config.add_static_view(name='static', path='PyMovie:static')
    config.scan('.views')
    return config.make_wsgi_app()
