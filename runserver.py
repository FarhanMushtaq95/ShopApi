from waitress import serve

from shop_api.wsgi import application
# documentation: https://docs.pylonsproject.org/projects/waitress/en/stable/api.html

if __name__ == '__main__':
    serve(application, host = '51.79.173.143', port='8090', connection_limit=1500,
              threads=50, asyncore_use_poll=True)
