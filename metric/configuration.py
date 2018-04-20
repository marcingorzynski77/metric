""" configuration module"""
import os
import logging
import yaml


class Configuration:
    """ class holding application settings"""
    flask_server_name = ""
    flask_debug = False
    rest_plus_swagger_ui_doc_expansion = ""
    rest_plus_validate = True
    rest_plus_mask_swagger = False
    rest_plus_error_404_help = False
    config_file = None

    def __init__(self):
        pass

    @staticmethod
    def load_default():
        """ load default configuration"""
        Configuration.flask_server_name = "localhost:8080"
        Configuration.flask_debug = False
        Configuration.rest_plus_swagger_ui_doc_expansion = ""
        Configuration.rest_plus_validate = True
        Configuration.rest_plus_mask_swagger = False
        Configuration.rest_plus_error_404_help = False
        Configuration.config_file = None

        logging.info("loading default configuration ")

    @staticmethod
    def load(configfile):
        """ load configuration from the provided file, if not provided defaults will be used"""

        if configfile:
            Configuration.config_file = configfile
            filename = configfile
            if os.path.exists(filename):
                logging.info("opening configuration file from %s", filename)
                cwd = os.getcwd()
                with open(os.path.join(cwd, filename), 'r') as yml_file:
                    cfg = yaml.load(yml_file)

                logging.info("reading config.yml")

                for section in cfg:
                    logging.info("section: %s ", section)
                    logging.info(cfg[section])

                Configuration.flask_server_name = cfg['app_settings']['flask_server_name']
                Configuration.flask_debug = cfg['app_settings']['flask_debug']
                Configuration.rest_plus_swagger_ui_doc_expansion = cfg['app_settings']['rest_plus_swagger_ui_doc_expansion']
                Configuration.rest_plus_validate = cfg['app_settings']['rest_plus_validate']
                Configuration.rest_plus_mask_swagger = cfg['app_settings']['rest_plus_mask_swagger']
                Configuration.rest_plus_error_404_help = cfg['app_settings']['rest_plus_error_404_help']

            else:
                Configuration.load_default()
        else:
            Configuration.load_default()




