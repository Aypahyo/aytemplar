from genericpath import exists
from logging import Logger, getLogger
import os
import re

class Replacer:
    __filepath : str = None
    __content : str = None
    __blacklist: 'list[str]' = []
    __whitelist: 'list[str]' = []

    def __init__(self, logger : Logger = None) -> None:
        self.__logger = getLogger() if logger is None else logger

    def load(self, filepath) -> None:
        if not exists(filepath):
            raise FileNotFoundError(f'expected to find "{filepath}" but found no file')
        self.__filepath = filepath

        with open(filepath, "r") as file:
            self.__content = file.read()

    def setBlacklist(self, blacklist : 'list[str]') -> None:
        self.__blacklist = blacklist

    def setWhitelist(self, whitelist : 'list[str]') -> None:
        self.__whitelist = whitelist

    def replace_from_env(self) -> None:
        env_names_target = self.__figure_out_targets()
        env_name_missing = []
        env_name_not_missing = []
        for env_n in env_names_target:
            if env_n not in os.environ.keys():
                env_name_missing.append(env_n)
            else:
                env_name_not_missing.append(env_n)       
        if len(env_name_missing) > 0:
            raise TypeError(f'The following keys are missing in the environemnt: "{env_name_missing}"')
        for env_n in env_name_not_missing:
            self.__content = self.__content.replace("${" + env_n + "}", os.getenv(env_n, "noooo") )

    def __figure_out_targets(self) -> 'list[str]':
        if len(self.__whitelist) > 0 and len(self.__blacklist) > 0:
            raise ValueError("blacklist and whitelist are mutually exclusive")
        envname_pattern = r"\$\{(?P<ENVNAME>[^\}\n]+)\}"
        env_names = list([match.group("ENVNAME") for match in re.finditer(envname_pattern, self.__content, re.MULTILINE)])
        env_names_target = []
        if len(env_names) == 0:
            self.__logger.warn("expected {} to contain placeholders but found none", self.__filepath)
            return env_names_target
        if len(self.__whitelist) > 0:
            env_names_whitelisted = []
            env_names_not_whitelisted = []
            for env_n in env_names:
                if env_n in self.__whitelist:
                    env_names_whitelisted.append(env_n)
                else:
                    env_names_not_whitelisted.append(env_n)
            if len(env_names_not_whitelisted) > 0:
                self.__logger.info(f'Ignoring: "{env_names_not_whitelisted}" due to not whitelisted')
            env_names_target = env_names_whitelisted
        elif len(self.__blacklist) > 0:
            env_names_blacklisted = []
            env_names_not_blacklisted = []
            for env_n in env_names:
                if env_n in self.__blacklist:
                    env_names_blacklisted.append(env_n)
                else:
                    env_names_not_blacklisted.append(env_n)
            if len(env_names_blacklisted) > 0:
                self.__logger.info(f'Ignoring: "{env_names_blacklisted}" due to blacklist')
            env_names_target = env_names_not_blacklisted
        else:
            env_names_target = env_names
        return env_names_target

    def store(self, filepath) -> None:
        if self.__content is None:
            self.__logger.error("Content was of type None - did loading happen?")
            raise TypeError("Content was of type None - did loading happen?")

        with open(filepath, "w") as file:
            file.write(self.__content)