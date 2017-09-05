import logging
import subprocess

from service_buddy.util.log_handler import print_red_bold


def invoke_process(args, exec_dir=None, dry_run=False):
    if dry_run:
        print_red_bold(u"\t {}".format(str(args)))
        return 0
    else:
        logging.info(u"\t {}".format(str(args)))
        arg_list = {'args': args}
        if exec_dir:
            arg_list['cwd'] = exec_dir
        return subprocess.call(**arg_list)