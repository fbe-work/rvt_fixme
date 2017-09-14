"""
RVT_fixme
things todo on workshared model
"""
import os.path as op
import json
from ConfigParser import ConfigParser
from scriptutils import this_script
from Autodesk.Revit.DB import BuiltInCategory, ElementId, WorksharingUtils


def get_tasks(user_name, fixme_task_list):
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument

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
                    print(str_id)
                    this_script.output.print_md("--- " + this_script.output.linkify(elem_id))
                    presented_ids += 1
                    if presented_ids == 5:
                        break

    print("-" * 59)
    print("| thank you, that is all I have for now,")
    print("| have a great day!")
    print("-" * 59)


def connect_to_rvt(fixme_task_list):
    user = __revit__.Application.Username
    get_tasks(user, fixme_task_list)


def read_json_to_dict(json_file):
    with open(json_file, 'r') as jsn:
        return json.load(jsn)


oc_path = op.dirname(__file__)
# print("-" + oc_path)
