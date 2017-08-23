"""
currently WIP!!!
Button will present different issues for the user.
"""
import os.path as op


def convert_path(path):
    return path.replace(op.sep, '/')


print("greetings, thank you for your interest in rvt_fixme! questions? ask Frederic")

ext_dir = op.dirname(op.dirname(op.dirname(op.dirname(op.dirname(__file__)))))

print(op.join(ext_dir, "startup.py"))
restart = convert_path(op.join(ext_dir, "startup.py"))
print(restart)
# execfile(restart)