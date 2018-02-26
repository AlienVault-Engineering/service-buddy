import logging
import subprocess

from service_buddy.util.log_handler import print_red_bold


def invoke_process(args, exec_dir=None, dry_run=False):
    if dry_run:
        print_red_bold(u"\t {}".format(str(args)))
        return 0
    else:
        arg_list = {'args': args}
        arg_list['stderr'] = subprocess.STDOUT
        if exec_dir:
            arg_list['cwd'] = exec_dir

        logging.info(u'[exec] invoke_process args=%r, exec_dir=%r, dry_run=%r', args, exec_dir, dry_run)
        returncode = 0
        try:
            output = subprocess.check_output(**arg_list)
        except subprocess.CalledProcessError, e:
            output = ""
            returncode = e.returncode

        for line in output.splitlines():
            logging.info(u'[exec] %s', line)
        logging.info(u'[exec] invoke_process complete args=%r, exec_dir=%r, dry_run=%r', args, exec_dir, dry_run)

        return returncode
