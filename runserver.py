# -*- coding: utf-8 -*-

from server.app import create_app
from server.settings import override

app = create_app(settings_overrides=override)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
