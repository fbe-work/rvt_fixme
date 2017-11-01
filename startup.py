"""
RVT_fixme
detects a task list in your project folder 
and reminds you of errors/warnings to fix
"""

import System
from System import EventHandler
from Autodesk.Revit.DB.Events import DocumentOpenedEventArgs
from Autodesk.Revit.DB.Events import DocumentOpeningEventArgs
from Autodesk.Revit.DB.Events import ProgressChangedEventArgs
from Autodesk.Revit.DB import ModelPathUtils
from Autodesk.Revit.UI import TaskDialog, TaskDialogIcon
import sys
import os.path as op
import datetime
startup_path = op.dirname(__file__)
sys.path.append(startup_path)

# TODO add support for reading bcf/bcfzip guids, comments


def event_handler_function(sender, args):
    print(15*"-" + "event_handler file opened" + 15*"-")
    doc = __revit__.ActiveUIDocument.Document
    now_utc = str(datetime.datetime.utcnow())
    log_path = "d:/delme/model_open_log.txt"

    if doc.IsWorkshared:
        doc_central_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(doc.GetWorksharingCentralModelPath())
        doc_local_path = doc.PathName
        doc_path = doc_central_path
        in_central = doc_central_path == doc_local_path
        if in_central:
            task_dialog = TaskDialog("rvt_fixme_central_model_warning")
            task_dialog.Id = "rvt_fixme_central_model_warning"
            task_dialog.MainIcon = TaskDialogIcon.TaskDialogIconWarning
            task_dialog.Title = "Attention - you are in central model!!!"
            task_dialog.MainContent = task_dialog.Title
            task_dialog.TitleAutoPrefix = True
            task_dialog.AllowCancellation = True
            task_dialog.Show()
        model_name = op.basename(doc_path)
        model_path = op.dirname(doc_path)
        # model_central_name = model_name.split("_" + rvt_user)[0]
        model_central_name = model_name.split(".rvt")[0]
        assume_fix_tasks_dir = op.join(model_path, "RVT_fixme")
        ini = op.join(assume_fix_tasks_dir, "fixme_{}.ini".format(model_central_name))
        jsn = op.join(assume_fix_tasks_dir, "fixme_{}_ids.json".format(model_central_name))

        # print("searching for fixme: {}".format(ini))
        if op.exists(ini):
            print("- found corresponding RVT_fixme ini to this model.")
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

        # print("searching for fixme: {}".format(jsn))
        if op.exists(jsn):
            print("- found corresponding RVT_fixme json to this model.")
            if doc.IsWorkshared:
                import on_ws_model_opened
                print("- workshared model found at:\n- {0}".format(doc_path))
                on_ws_model_opened.connect_to_rvt(jsn)

        with open(log_path, "a") as model_log:
            model_log.write("ws file was opened at \n- {0}\n-".format(now_utc))


def open_notify(sender, args):
    print("--opening a project!!")


def progress_notify(sender, args):
    global refs_updated
    topic = args.Caption
    stage = args.Stage.ToString()
    # print(sender, args, topic)
    if topic == "Updating References":

        if stage == "Started":
            print("--------!!started_updating_refs!!")
            if refs_updated > 1:
                print("ref loading! cancellable?: ------------- {}".format(args.Cancellable))

                if args.Cancellable:
                    # args.Cancel()
                    # print("cancelled!")
                    pass

            refs_updated += 1

        elif stage == "Finished":
            print("--------!!finished_updating_refs!! current ref_count: {}".format(refs_updated))

        print(args.Caption, stage, args.Position)


refs_updated = 0
__revit__.Application.DocumentOpened += EventHandler[DocumentOpenedEventArgs](event_handler_function)
__revit__.Application.DocumentOpening += EventHandler[DocumentOpeningEventArgs](open_notify)
# __revit__.Application.ProgressChanged += EventHandler[ProgressChangedEventArgs](progress_notify)
rvt_user = __revit__.Application.Username

doc = None
uidoc = None

print("-"*59)
print(" | dear {0} welcome to RVT_fixme!!".format(rvt_user))
print(" | I will try to inform you on:".format(rvt_user))
print(" | disk space left, central model opened".format(rvt_user))
print(" | and things to fix in project model".format(rvt_user))
# print(" | rvt_fix at {0}".format(__file__))
print("-"*59)
