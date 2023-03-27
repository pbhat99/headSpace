#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: RV
#
#----------------------------------------------------------------------------------------------------------

import subprocess
import shlex
import wiz

context = wiz.resolve_context(["mill-rv"])

for node in nuke.selectedNodes("Write"):
    command = context["command"]["rv"]
    command += " " + node["file"].value()
    subprocess.Popen(shlex.split(command), env=context["environ"])