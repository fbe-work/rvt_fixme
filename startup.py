"""
RVT_fixme
detects a task list in your project folder 
and reminds you of errors/warnings to fix
"""

import System
from System import EventHandler
from Autodesk.Revit.DB.Events import DocumentOpenedEventArgs
import sys
import os.path as op
import datetime
startup_path = op.dirname(__file__)
sys.path.append(startup_path)

# TODO add support for reading bcf/bcfzip guids, comments


def event_handler_function(sender, args):
    print(15*"-" + "event_handler file opened" + 15*"-")
    now_utc = str(datetime.datetime.utcnow())
    log_path = "d:/delme/model_open_log.txt"
    doc_path = doc.PathName
    model_name = op.basename(doc_path)
    model_path = op.dirname(doc_path)
    model_central_name = model_name.split("_"+user)[0]
    assume_fix_tasks_dir = op.join(model_path, "RVT_fixme")
    ini = op.join(assume_fix_tasks_dir, "fixme_{}.ini".format(model_central_name))
    if op.exists(ini):
        print("- found corresponding RVT_fixme to this model.")
        # print(doc_path)
        # print("file was opened at {0}".format(now_utc))
        # print("ini found at: {0}".format(ini))
        if doc.IsWorkshared:
            import on_ws_model_opened
            print("- workshared model found at:\n- {0}".format(doc_path))
            # print("attempt reload")
            # reload(on_ws_model_opened)
            # print("after_reload")
            on_ws_model_opened.connect_to_rvt(ini)
        with open(log_path, "a") as model_log:
            model_log.write("ws file was opened at \n- {0}\n-".format(now_utc))


__revit__.Application.DocumentOpened += EventHandler[DocumentOpenedEventArgs](event_handler_function)
rvt_user = __revit__.Application.Username

doc = None
uidoc = None

print("-"*59)
print(" | dear {0} welcome to RVT_fixme!!".format(rvt_user))
print("-"*59)
