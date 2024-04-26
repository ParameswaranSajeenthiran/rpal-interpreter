import logging

from ASTNode import ASTNode


class Envronment:
    logger = logging.getLogger(__name__)

    def __init__(self, index):
        self.idx = index
        self.map_vars = {}
        self.parent = None

    def set_env_params(self, parent_env, key, value):
        self.map_vars[key] = value
        if isinstance(key, ASTNode) and isinstance(value, ASTNode):
            pass
            # print("setEnvParams: {} | {} | value: {}".format(key, key.name, value.name))
        else:
            # self.logger.info("setEnvParams: key: {} | value: {}".format(key, value.name))
            pass
        self.parent = parent_env
        # print(self.map_vars)
        # print("setting parent of environment: {} as env: {}".format(self.idx, parent_env.idx))

    def get_env_idx(self):
        return self.idx

    def get_val(self, key):
        # self.logger.info("getVal: {} | {}".format(key, key.name))
        if key in self.map_vars.keys():
            value = self.map_vars[key]
            self.logger.info("found in cur env id {}".format(self.idx))
            if isinstance(value, ASTNode):
                self.logger.info("value: {}".format(value.value))
            return value
        else:
            self.logger.info("not found in cur env")
            return None
