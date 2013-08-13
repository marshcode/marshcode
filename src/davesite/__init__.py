from davesite.app import factory
app = factory.create_app(__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
