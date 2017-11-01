"""
RVT_fixme
things todo on workshared model
"""
import os.path as op
import json
import ctypes
from ConfigParser import ConfigParser
from scriptutils import this_script
from Autodesk.Revit.DB import BuiltInCategory, ElementId, WorksharingUtils


def disk_space_left(drive):
    # checking available drive space
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),
                                               None,
                                               None,
                                               ctypes.pointer(free_bytes))

    free_hd_space = float(free_bytes.value) / (1024 ** 3)
    if free_hd_space < 10.0:
        this_script.output.print_md("<font color='red'>**Remaining space on {} "
                                    "is less than 10GB!!**</font>".format(drive))
        this_script.output.print_md("<font color='red'>**Clean up drive first "
                                    "before you risk broken syncs!!**</font>")
    else:
        print("- free disk space on {} is: {} GB".format(drive, free_hd_space))


def get_tasks(user_name, fixme_task_list):
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    jrn_drive = op.abspath(op.splitdrive(doc.Application.RecordingJournalFilename)[0])
    disk_space_left(jrn_drive)

    if fixme_task_list.endswith("ini"):
        ini_file = fixme_task_list
        config = ConfigParser()
        config.read(ini_file)
        presented_ids = 0
        for sec in config.sections():
            this_script.output.print_md("**{}**".format(sec))
            print("--- list of ids to fix:")
            for elem in config.items(sec):
                topic = elem[0]
                print("--- topic: {0}".format(topic))
                for str_id in elem[1].split(","):
                    # print(str_id)
                    elem_id = ElementId(int(str_id.strip()))
                    if doc.GetElement(elem_id):
                        # print(elem_id)
                        this_script.output.print_md("--- " + this_script.output.linkify(elem_id))
                        presented_ids += 1
                    if presented_ids == 5:
                        break

    elif fixme_task_list.endswith(".json"):
        json_file = fixme_task_list
        presented_ids = 0
        warn_id_dict = read_json_to_dict(json_file)
        for topic in warn_id_dict:
            this_script.output.print_md("**{}**".format(topic))
            for date in warn_id_dict[topic]:
                for str_id in warn_id_dict[topic][date]:
                    elem_id = ElementId(int(str_id))
                    elem = doc.GetElement(elem_id)
                    elem_cat = elem.Category.Name.strip("<>")
                    if elem.ViewSpecific:
                        location = doc.GetElement(elem.OwnerViewId).Name
                    else:
                        location = doc.GetElement(elem.LevelId).Name

                    elem_info = " - {} - {}".format(elem_cat, location)

                    last_changer = WorksharingUtils.GetWorksharingTooltipInfo(doc, elem_id).LastChangedBy
                    if last_changer == user_name:
                        this_script.output.print_md("--- " + this_script.output.linkify(elem_id) + elem_info)
                        this_script.output.print_md("--- " + elem.Category.Name)
                    presented_ids += 1
            if presented_ids == 9:
                break

    print("-" * 59)
    print("| thank you, that is all I have for now,")
    this_script.output.print_md("| **have a great day!**")
    print("-" * 59)


def connect_to_rvt(fixme_task_list):
    user = __revit__.Application.Username
    get_tasks(user, fixme_task_list)


def read_json_to_dict(json_file):
    with open(json_file, 'r') as jsn:
        return json.load(jsn)


oc_path = op.dirname(__file__)
# print("-" + oc_path)
