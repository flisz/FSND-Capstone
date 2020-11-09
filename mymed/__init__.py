from mymed.setup.loggers import LOGGERS  # import loggers will also initialize the loggers

log = LOGGERS.Setup
log.debug(f'__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))


if any(__name__ == case for case in ['__main__', 'mymed']):
    from mymed.app import create_app
    app = create_app()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
