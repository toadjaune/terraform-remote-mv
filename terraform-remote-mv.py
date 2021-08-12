#!/usr/bin/env python3

import os, sys, subprocess

if len(sys.argv) < 4:

    print("")
    print("USAGE : ./terraform-remote-mv.py /path/to/source/config /path/to/dest/config type1.resource1 type2.resource2 type3.resource3 [...]")
    print("")

    print("`terraform state mv` cannot move resources from one remote tfstate to another, requiring you to fiddle with local tfstates.")
    print("This script does exactly that.")
    print("")
    print("Please note that since terraform doesn't support manually locking the state (https://github.com/hashicorp/terraform/issues/17203),")
    print("we can't do this in a safe way. You'll have to ensure yourself nobody modifies any of the remote states while this script runs.")
    print("")
    print("If trying to move complex structures, be careful not to let your shell eat brackets or string delimitors, you might want to do :")
    print("""terraform state list | grep SOMETHING | sed "s/^/'/;s/$/'/" | xargs ./terraform-remote-mv.py /path/a /path/b""")
    sys.exit("Not enough arguments")

source_config_path = os.path.abspath(sys.argv[1])
dest_config_path = os.path.abspath(sys.argv[2])
current_path = os.getcwd()
resource_names = sys.argv[3:]

# Import the tfstate to a local file
# The script execution is stopped in case of failure
with open("source.tfstate", 'w') as output_file:

    print(f"Saving remote tfstate from {source_config_path} to ./source.tfstate")
    subprocess.run(["terraform", "state", "pull"], cwd=source_config_path, stdout=output_file, check=True)

with open("dest.tfstate", 'w') as output_file:

    print(f"Saving remote tfstate from {dest_config_path} to ./dest.tfstate")
    subprocess.run(["terraform", "state", "pull"], cwd=dest_config_path, stdout=output_file, check=True)

# NB : If a given mv command fails, keep going. That's often the case when copying modules, being able to do it in several stages is useful.
print(f"Now moving items between local states")
for resource in resource_names:
    print(f"Moving {resource}")
    subprocess.run(["terraform", "state", "mv", "-state=source.tfstate", "-state-out=dest.tfstate", resource, resource])

print(f"Pushing back ./source.tfstate to {source_config_path} remote state")
subprocess.run(["terraform", "state", "push", current_path + "/source.tfstate"], cwd=source_config_path, check=True)

print(f"Pushing back ./dest.tfstate to {dest_config_path} remote state")
subprocess.run(["terraform", "state", "push", current_path + "/dest.tfstate"], cwd=dest_config_path, check=True)

print(f"Resource migration complete !")
print(f"NB : local tfstates and their backups are not deleted, to allow you to recover in case of issue")
