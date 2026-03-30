#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Submit to Deadline
#
#----------------------------------------------------------------------------------------------------------

import os
import nuke
import subprocess
import tempfile
import time
import re


def clean_output_name(path):

    filename = os.path.basename(path)
    name = os.path.splitext(filename)[0]

    # remove padding
    name = re.sub(r"%\d+d", "", name)
    name = re.sub(r"\$F\d*", "", name)
    name = re.sub(r"#+", "", name)

    return name.rstrip("._-")


def build_comment(node):

    prefix = node["render_prefix"].value() if node.knob("render_prefix") else ""
    channels = node["channels"].value() if node.knob("channels") else ""

    if prefix and channels:
        return f"{prefix} | {channels}"

    return prefix or channels


def submit_selected_writes_to_deadline():

    write_nodes = nuke.selectedNodes("Write")

    if not write_nodes:
        nuke.message("Please select at least one Write node.")
        return


    # -------- LOCAL SETTINGS --------
    pool = "zcomp"
    priority = 50
    chunk_size = 1

    DEADLINE_COMMAND = r"C:\Program Files\Thinkbox\Deadline10\bin\deadlinecommand.exe"
    NUKE_EXECUTABLE = r"C:\Program Files\Nuke16.0v3\Nuke16.0.exe"
    # --------------------------------


    script_path = nuke.root().name()

    if not script_path or script_path == "Root":
        nuke.message("Please save the Nuke script before submitting.")
        return

    nuke.scriptSave()

    root = nuke.root()
    start_frame = int(root["first_frame"].value())
    end_frame = int(root["last_frame"].value())
    frame_range = f"{start_frame}-{end_frame}"

    script_name = os.path.splitext(os.path.basename(script_path))[0]

    submitted_jobs = []

    for node in write_nodes:

        write_node_name = node.name()
        write_path = node["file"].value()

        if not write_path:
            nuke.message(f"{write_node_name} has no output path.")
            continue


        # -------- Job Name from output filename --------
        job_name = clean_output_name(write_path)

        # -------- Comment --------
        comment = build_comment(node)


        timestamp = int(time.time())

        job_info_path = os.path.join(
            tempfile.gettempdir(),
            f"deadline_job_{timestamp}_{write_node_name}.job"
        )

        plugin_info_path = os.path.join(
            tempfile.gettempdir(),
            f"deadline_plugin_{timestamp}_{write_node_name}.job"
        )


        username = os.environ.get("USERNAME", "User")


        job_lines = [
            "Plugin=CommandLine",
            f"Name={job_name}",
            f"BatchName={script_name}",
            f"UserName={username}",
            f"Frames={frame_range}",
            f"ChunkSize={chunk_size}",
            f"Priority={priority}",
            f"Pool={pool}",
            f"Comment={comment}",
        ]


        nuke_args = f'-X {write_node_name} -F {frame_range} "{script_path}"'


        plugin_lines = [
            f"Executable={NUKE_EXECUTABLE}",
            f"Arguments={nuke_args}",
            "Shell=False",
        ]


        with open(job_info_path, "w") as f:
            f.write("\n".join(job_lines))

        with open(plugin_info_path, "w") as f:
            f.write("\n".join(plugin_lines))


        try:

            proc = subprocess.Popen(
                [DEADLINE_COMMAND, job_info_path, plugin_info_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate()

            if proc.returncode == 0:

                match = re.search(r"JobID=([0-9a-fA-F]+)", stdout)

                if match:
                    job_id = match.group(1)
                    submitted_jobs.append((job_name, job_id))

        except Exception as e:
            nuke.message(f"Submission failed: {str(e)}")


    if submitted_jobs:

        msg = "\n".join([f"{name} (ID: {jid})" for name, jid in submitted_jobs])
        nuke.message(f"Submitted {len(submitted_jobs)} job(s):\n{msg}")

    else:
        nuke.message("No jobs submitted.")


submit_selected_writes_to_deadline()