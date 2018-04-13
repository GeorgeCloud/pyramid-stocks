def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_route('home', '/')
    config.add_route('auth', '/auth')
    config.add_route('add-stock', '/add-stock')
    config.add_route('logout', '/logout')
    config.add_route('portfolio', '/portfolio')
    config.add_route('stock_detail', '/portfolio/{symbol}')
