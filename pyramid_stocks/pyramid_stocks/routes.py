def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('register', '/auth')
    config.add_route('stock', '/stock')
    config.add_route('portfolio', '/portfolio')
    config.add_route('adding', '/portfolio/{symbol}')
