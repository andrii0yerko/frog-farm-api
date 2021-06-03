# Frog Farm
A simple web application that allows users to have neural frogs, wash and feed them, and as result,
receive income that can be spent for the new frogs.

This repo contains the back-end part of the project, that provides connection in two alternative ways: as RESTful API and through WebSocket connection, that mostly duplicate HTTP requests functionality (watch [documentation](#documentation) for more)

Implemented as Python application, core made on Flask and SQLAlchemy, APIs implemented with Flask-RESTful and Flask-Socket.
Image generation based on a GAN model created with PyTorch.

The application is ready for deployment on Heroku, `Procfile` provided as well (watch [installation documentation](./docs/installation.md) for more)

## Related Links
- [Original front-end application](https://github.com/trilgar/jaba-front) by @trilgar
- [GAN creating and training on frog images](https://github.com/andrii0yerko/deep-learning-stuff#1-dcgan-with-pytorch)

## Documentation
- [Installation](./docs/installation.md)
- [WebSocket API documentation](./docs/websocket_api_docs.md)
- [HTTP API documentation](./docs/http_api_docs.md)