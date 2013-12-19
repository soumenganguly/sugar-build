import logging
import os
import sys


build_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
base_dir = os.path.dirname(build_dir)
home_state_dir = os.path.join(base_dir, "home")
commands_dir = os.path.join(build_dir, "commands")
logs_dir = os.path.join(build_dir, "logs")
root_dir = os.path.dirname(build_dir)
log_path = os.path.join(logs_dir, "osbuild.log")

from osbuild import main
from osbuild import config


def is_buildbot():
    return "SUGAR_BUILDBOT" in os.environ


def get_config_args():
    config_args = {"config_dir": os.path.join(build_dir),
                   "source_dir": os.path.join(root_dir),
                   "docs_dir": os.path.join(build_dir, "out", "docs"),
                   "dist_dir": os.path.join(build_dir, "out", "dist"),
                   "build_state_dir": os.path.join(build_dir, "state"),
                   "home_state_dir": home_state_dir,
                   "profile_name": os.environ.get("SUGAR_PROFILE", "default"),
                   "prefs_path": os.path.join(root_dir, "prefs.json"),
                   "interactive": not is_buildbot()}

    if is_buildbot():
        config_args["git_user_name"] = "buildbot"
        config_args["git_email"] = "buildbot@sugarlabs.org"

    return config_args


def print_close_message():
    print "Type Shift-Alt-Q inside sugar to close."


def setup_logging():
    try:
        os.unlink(log_path)
    except OSError:
        pass

    try:
        os.makedirs(logs_dir)
    except OSError:
        pass

    logging.basicConfig(level=logging.DEBUG,
                        filename=log_path)


def setup():
    setup_logging()


    config_args = get_config_args()

    if not main.setup(config_args):
        sys.exit(1)

    commands_path = os.path.join(commands_dir, "broot")

    os.environ["SUGAR_DEVELOPER"] = "1"
    os.environ["SUGAR_ACTIVITIES_PATH"] = os.path.join(base_dir, "activities")
    os.environ["SUGAR_HOME"] = os.path.join(home_state_dir, "dotsugar")
    os.environ["PATH"] = os.path.expandvars("PATH=$PATH:%s" % commands_path)


def run(command):
    setup()
    if not getattr(main, "cmd_%s" % command)():
        sys.exit(1)
