"""
RVT_fixme
things todo on workshared model
"""
import os.path as op
from ConfigParser import ConfigParser
from scriptutils import this_script
from Autodesk.Revit.DB import BuiltInCategory, ElementId, WorksharingUtils


def get_tasks(user_name, ini_file):
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
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
    print("-" * 59)
    print("| thank you, that is all I have for now,")
    print("| have a great day!")
    print("-" * 59)


def connect_to_rvt(fixme_ini):
    user = __revit__.Application.Username
    get_tasks(user, fixme_ini)


oc_path = op.dirname(__file__)
# print("-" + oc_path)
