import logging

def setup_root_logger():
    fmt = "%(asctime)s [%(levelname)s] [%(project)s] [%(component)s] %(message)s"
    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # avoid adding multiple handlers in interactive sessions
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(handler)
    else:
        for h in root.handlers:
            h.setFormatter(formatter)

def get_logger(component: str, project: str = "PostAggregatorEx1"):
    base = logging.getLogger(component)
    return logging.LoggerAdapter(base, {"project": project, "component": component})
