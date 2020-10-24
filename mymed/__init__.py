from mymed.setup.loggers import LOGGERS  # import loggers will also initialize the loggers


if any(__name__ == case for case in ['__main__', 'project']):
    from mymed.app import create_app
    app = create_app()
    app.run(host='127.0.0.1', port=5000)
