from flask import Response

class endpoints:
    CALENDAR_FILENAME = 'hello.txt'
    USERS_ROOT = 'users'
    ACTION_ROOT = 'action'

    HELLO_WORLD = "/hello-world"




class web_server():
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }

    @staticmethod
    def generate_web_app():
        from flask import Flask
        from flask_restx import Resource, Api


        app: Flask = Flask(__name__)
        api = Api(app, doc='/docs',
                  prefix="/api/v1",
                  # authorizations=web_server.authorizations, security='apikey'
                  )

        queues = api.namespace(endpoints.ACTION_ROOT, description='Dynamically Stuff')

        @queues.route(endpoints.HELLO_WORLD)
        class GetProjects(Resource):
            @api.doc(responses={200: endpoints.CALENDAR_FILENAME})
            def get(self):

                file = 'hello world'

                response = Response(file, mimetype="text/text")
                response.headers.set(
                    "Content-Disposition", "attachment", filename=endpoints.CALENDAR_FILENAME
                )
                return response


        return app  # Return the application object at the end of the call