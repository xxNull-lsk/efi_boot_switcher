import os
import shlex
import subprocess


def decode_text(txt) -> str:
    for code in ['gbk', 'itf-8']:
        try:
            return txt.decode(code)
        except UnicodeDecodeError as err:
            print(err)
            continue
        except Exception as err:
            print(err)
            continue
    return ""


def run_app(cmd, env=None, cwd=None, shell=False, log_function=None):
    if not cwd:
        cwd = os.getcwd()

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    try:
        p = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            bufsize=0,
            cwd=cwd
        )
        while p.poll() is None:
            line = p.stdout.readline()
            line = decode_text(line)
            if log_function:
                log_function(line)
        p.wait()
        for line in p.stdout.readlines():
            line = decode_text(line)
            if log_function:
                log_function(line)
        p.stdout.close()
        return p.returncode
    except Exception as ex:
        print("Exception: {}".format(ex))
    return -1
