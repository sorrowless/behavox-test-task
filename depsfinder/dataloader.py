from logging import getLogger
from typing import Dict

import sys
import yaml


class DataLoader(object):
    def __init__(self):
        self.logger = getLogger(__name__)
    
    def load(self, filepath: str) -> Dict:
        data = {}
        try:
            with open(filepath, 'rt') as fh:
                data = yaml.load(fh, Loader=yaml.Loader)
                self.logger.debug(data)
        except FileNotFoundError:
            self.logger.error('You passed filepath as argument but seems this file does '
                'not exist. Fix it and try again.'
            )
            sys.exit(1)
        except yaml.scanner.ScannerError:
            self.logger.error("Seems that file you're trying to parse is not valid yaml. "
                "Fix it and try again."
            )
            sys.exit(1)
        except Exception:
            self.logger.exception("We're found an error while parsing yaml file")
            sys.exit(1)
        return data