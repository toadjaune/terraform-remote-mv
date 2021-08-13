# terraform-remote-mv

## Introduction

This is a very simple script to move resources between different remote terraform states.

You might need to do this in various scenarii, most of them being a variant of "I'm refactoring my terraform config"

The terraform cli doesn't provide any way to do this directly, so you usually end up doing something along the lines of :

* downloading source and destination remote tfstates with `terraform state pull`
* moving whatever you need to move between your local copies with `terraform state mv`
* uploading both modified tfstates with `terraform state push`

(There are plenty of blogposts out there detailing the manual procedure)

This script does exactly that.

## Install

The install is not too complicated :
```
git clone https://github.com/toadjaune/terraform-remote-mv
```

The script has no dependencies besides python >= 3.5, which you most likely already have on your machine.

Then run it with :
```
cd terraform-remote-mv
./terraform-remote-mv.py
```

Now go read the rest of this README before letting it touch your terrafrom states.

## Caveats and limitations

Disclaimer : This is a very simple script, hacked together to help me solve what I think is a very common problem, so I thought I'd share it.
It wasn't extensively tested, and certainly isn't a compendium of good programming practices, so make sure to test it before using it on something too important.

The script leaves behind a myriad of tfstate files in the working directory, to leave you the possibility of recovering data in case of problem. Those contain any sensitive info present in your tfsates, so, make sure to clean them up properly. And not to commit them.

### State locking

Ideally, we would want to start by locking the remote states, do everything we need, then release the locks.

Since terraform doesn't support manually locking the state (https://github.com/hashicorp/terraform/issues/17203), by design, we can't do that.

This means you'll have to ensure yourself nobody modifies any of the remote states while this script runs.


Or, if unlike me, you use terraform directly (not through an external tool such as terragrunt), you might want to give a try to https://github.com/minamijoyo/tflock.
That's still going to depend on your state storage backend.

Either way, make sure you understand the implications of the lack of locking before using this script, or you might lose data.

