from Switcher.switcher import Switcher

if __name__ == '__main__':
    switcher = Switcher("junior", "project")
    logger = Switcher.logger
    logger.append("hello")
