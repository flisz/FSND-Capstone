import os
import json
import sys
import platform
import yaml
from pathlib import Path

from mymed.setup.loggers import LOGGERS

log = LOGGERS.Setup


class SetupConfig:
    def __init__(self, config_yaml=None):
        self.__properties = dict()
        self.__properties['ROOT'] = self.__init_root()
        self.__properties['CONFIG'] = self.__init_config(config_yaml=config_yaml)
        self.__properties['DATABASE_INFO'] = self.__init_db_info()
        self.__properties['PROJECT_NAME'] = self.__init_project_name()
        self.__properties['APP_DOMAIN'] = self.__init_app_domain()
        self.__properties['APP_HOST'] = self.__init_app_host()
        self.__properties['APP_PORT'] = self.__init_app_port()
        self.__properties['AUTH0_DOMAIN'] = self.__init_auth0_domain()
        self.__properties['AUTH0_ALGORITHMS'] = self.__init_auth0_algorithms()
        self.__properties['AUTH0_API_AUDIENCE'] = self.__init_auth0_api_audience()
        self.__properties['AUTH0_CLIENT_ID'] = self.__init_auth0_client_id()
        self.__properties['AUTH0_CALLBACK_URL'] = self.__init_auth0_callback_url()
        self.__properties['JWT_SECRET'] = self.__init_jwt_secret()
        self.__properties['APP_MODE'] = self.__init_mode()
        self.__properties['HOSTNAME'] = self.__init_host_name()
        self.__properties['USER_HOME'] = self.__init_user_home()
        self.__properties['TEMPLATES'] = self.__init_templates()
        self.__properties['STATIC_FILES'] = self.__init_static_files()
        self.__properties['SECRET_KEY'] = self.__init_secret_key()

    @property
    def ROOT(self):
        return self.__properties['ROOT']

    @staticmethod
    def __init_root():
        levels_up = -2
        env_file_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        root = '/'.join(env_file_path.split('/')[:levels_up])
        sys.path.append(root)
        log.debug(f'ROOT: {root}')
        return root

    @property
    def CONFIG(self):
        return self.__properties['CONFIG']

    def __init_config(self, config_yaml=None):
        if not config_yaml:
            config_yaml = os.path.join(self.ROOT, 'config.yaml')
        data = dict()
        if os.path.isfile(config_yaml):
            with open(config_yaml) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                log.debug('CONFIG: Successfully loaded')
                log.debug(f'CONFIG: {json.dumps(data, indent=4)}')
                return data
        else:
            raise FileNotFoundError(f'{config_yaml} missing!')

    @property
    def DATABASE_INFO(self):
        return self.__properties['DATABASE_INFO']

    def __init_db_info(self):
        database_info_yaml = os.path.join(self.ROOT, 'db-info.yaml')
        data = dict()
        if os.path.isfile(database_info_yaml):
            with open(database_info_yaml) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                log.debug('DATABASE_INFO: Successfully loaded')
                log.debug(f'DATABASE_INFO: {json.dumps(data, indent=4)}')
                return data
        else:
            raise FileNotFoundError(f'{database_info_yaml} missing!')

    @property
    def PROJECT_NAME(self):
        return self.__properties['PROJECT_NAME']

    def __init_project_name(self):
        project_name = self.CONFIG.get('project_name')
        if project_name:
            log.debug(f'PROJECT_NAME: {project_name}')
            return project_name
        else:
            raise ValueError('project_name field missing from config.yaml')

    @property
    def APP_MODE(self):
        return self.__properties['APP_MODE']

    def __init_mode(self):
        mode = self.CONFIG.get('app', dict()).get('mode')
        log.debug(f'APP_MODE: {mode}')
        return mode

    @property
    def APP_DOMAIN(self):
        return self.__properties['APP_DOMAIN']

    def __init_app_domain(self):
        domain = self.CONFIG.get('app', dict()).get('domain', 'http://127.0.0.1')
        log.debug(f'APP_DOMAIN: {domain}')
        return domain

    @property
    def APP_HOST(self):
        return self.__properties['APP_HOST']

    def __init_app_host(self):
        host = self.CONFIG.get('app', dict()).get('host')
        log.debug(f'APP_HOST: {host}')
        return host

    @property
    def APP_PORT(self):
        return self.__properties['APP_PORT']

    def __init_app_port(self):
        port = self.CONFIG.get('app', dict()).get('port')
        log.debug(f'APP_PORT: {port}')
        return port

    @property
    def AUTH0_DOMAIN(self):
        return self.__properties['AUTH0_DOMAIN']

    def __init_auth0_domain(self):
        domain = self.CONFIG.get('auth0', dict()).get('domain')
        log.debug(f'AUTH0_DOMAIN: {domain}')
        return domain

    @property
    def AUTH0_ALGORITHMS(self):
        return self.__properties['AUTH0_ALGORITHMS']

    def __init_auth0_algorithms(self):
        algorithms = audience = self.CONFIG.get('auth0', dict()).get('algorithms', ['RS256'])
        log.debug(f'AUTH0_ALGORITHMS: {algorithms}')
        return algorithms

    @property
    def AUTH0_API_AUDIENCE(self):
        return self.__properties['AUTH0_API_AUDIENCE']

    def __init_auth0_api_audience(self):
        audience = self.CONFIG.get('auth0', dict()).get('audience')
        log.debug(f'AUTH0_API_AUDIENCE: {audience}')
        return audience

    @property
    def AUTH0_CLIENT_ID(self):
        return self.__properties['AUTH0_CLIENT_ID']

    def __init_auth0_client_id(self):
        client_id = self.CONFIG.get('auth0', dict()).get('client_id')
        log.debug(f'AUTH0_CLIENT_ID: {client_id}')
        return client_id

    @property
    def AUTH0_CALLBACK_URL(self):
        return self.__properties['AUTH0_CALLBACK_URL']

    def __init_auth0_callback_url(self):
        callback_url = f'{self.APP_DOMAIN}:' \
                       f'{self.APP_PORT}/auth/callback/'
        log.debug(f'AUTH0_CALLBACK_URL: {callback_url}')
        return callback_url

    @property
    def JWT_SECRET(self):
        return self.__properties['JWT_SECRET']

    def __init_jwt_secret(self):
        jwt_secret = self.CONFIG.get('jwt', dict()).get('secret')
        log.debug(f'JWT_SECRET: {jwt_secret}')
        return jwt_secret

    @property
    def USER_HOME(self):
        return self.__properties['USER_HOME']

    def __init_user_home(self):
        home = str(Path.home())
        log.debug(f'USER_HOME: {home}')
        return home

    @property
    def HOSTNAME(self):
        return self.__properties['HOSTNAME']

    def __init_host_name(self):
        hostname = platform.uname()[1].upper()
        log.debug(f'HOSTNAME: {hostname}')
        return hostname

    @property
    def TEMPLATES(self):
        return self.__properties['TEMPLATES']

    def __init_templates(self):
        templates = os.path.join(self.ROOT, self.PROJECT_NAME, 'templates')
        if os.path.isdir(templates):
            return templates
        else:
            raise NotADirectoryError(f'{templates} directory missing!')

    @property
    def STATIC_FILES(self):
        return self.__properties['STATIC_FILES']

    def __init_static_files(self):
        static_files = os.path.join(self.ROOT, self.PROJECT_NAME, 'static')
        if os.path.isdir(static_files):
            return static_files
        else:
            raise NotADirectoryError(f'{static_files} directory missing!')

    @property
    def SECRET_KEY(self):
        return self.__properties['SECRET_KEY']

    def __init_secret_key(self):
        secret_key = self.CONFIG.get('app', dict()).get('secret_key')
        if secret_key:
            log.debug(f'SECRET_KEY: {secret_key}')
            return secret_key
        else:
            raise ValueError('secret_key field missing from config.yaml')
