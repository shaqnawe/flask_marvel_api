import click, os

def register(app):
    @app.cli.group()
    def blueprint():
        """Blueprint creation commands."""
        pass

    @blueprint.command()
    @click.argument('name')
    def create(name):
        """Create new Flask blueprint."""

        basedir = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}'

        try:
            # check if the blueprint directory already exists
            if not os.path.exists(basedir):
                os.makedirs(basedir)
                filenames = ['__init__', 'routes', 'models']
                [open(f'{basedir}/{file}.py', 'w') for file in filenames]
                print("Blueprint created successfully")
        except Exception as error:
            print(f"Something went wrong with creating your blueprint called {name}")
            print(error)
