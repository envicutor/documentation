Comparing Envicutor and other code execution systems
####################################################

Isolation
*********

In this section, we discuss different levels of isolation implemented by different code execution systems and which level Envicutor chooses:

Isolation via running all submissions under a different user than the code execution system (Online IDE)
========================================================================================================

The first Google search for "Online IDE" brings us to a system called Online IDE :cite:`online-ide`. Choosing "bash" as the programming language and running the following code at some point in time:

.. code-block:: bash

  ps aux

gives us the following output:

.. code-block::

  PID   USER     TIME  COMMAND

      1 root      0:06 node server_8080.js
    406 repl      0:00 python3 -i
    686 repl      0:00 python3 main.py
    698 repl      0:00 sh main.sh
    699 repl      0:00 ps aux

This output represents all of the processes that are running on the system. We can see multiple python processes that are not started by us but are started by the same user as ours. We can conclude that in this system, all submissions run under the same user (repl), while the code execution system (PID 1) runs under the root user (root).

This is an ineffective way of doing isolating submissions (which might be OK depending on their requirements). For instance, had we run the command ``killall python3`` instead of ``ps aux``, the python submissions of other users would have been terminated. Moreover, submissions can write into each others directories and read from each other.

Such isolation method would not be appropriate for running a code execution system that is used in competitive programming systems and assignment graders.

Isolation via running each submissions under a different user (Piston)
======================================================================

If, at some point in time, we run the following Bash command to send two Bash ``ps aux`` submissions to Piston :cite:`piston-repo` code execution system:

.. code-block:: bash

  curl -X POST https://emkc.org/api/v2/piston/execute -H 'Content-Type: application/json' -d '{"language": "bash", "version": "*", "files":[{"content": "ps -eo user:20,pid,pcpu,pmem,comm"}]}' | jq & curl -X POST https://emkc.org/api/v2/piston/execute -H 'Content-Type: application/json' -d '{"language": "bash", "version": "*", "files":[{"content": "ps -eo user:20,pid,pcpu,pmem,comm"}]}' | jq

and observe the standard output of one of the submissions, we would notice the following output:

.. code-block::

  USER                   PID %CPU %MEM COMMAND
  root                     1  1.0  2.1 node
  runner1066            3569  0.0  0.0 timeout
  runner1067            3570  0.0  0.0 timeout
  runner1066            3571  0.0  0.1 bash
  runner1067            3572  0.0  0.1 bash
  runner1066            3573  0.0  0.1 bash
  runner1067            3574  0.0  0.1 bash
  runner1066            3575  0.0  0.1 ps
  runner1067            3576  0.0  0.0 bash

This output represents all of the processes that are running on the system. We can see that there are two users who started a bash process (runner1066, runner1067). These two users represent our two submissions that we sent. The code execution system is running under the root user.

While this approach prevents some exploits such as killing other submissions' processes and reading/writing to other submissions' files, there are still some caveats.

The first obvious caveat is that the submissions are aware of each other's existence on the system which violates the principles of isolation we discussed in ":ref:`improvement_areas`".

Another caveat is that submissions can read and write to shared directories such as ``/tmp`` which also violates the principles of isolation. Consider the following two bash submissions


.. code-block:: bash

  echo -e "#!/bin/bash\necho This is a long line. This is a long line $((1+1))" > /tmp/a
  chmod a+x /tmp/a
  sleep 3

.. code-block:: bash

  /tmp/a

If we send the first submission, wait for 500 ms, and send the second submission, we would notice the following standard output in the second submission:

.. code-block::

  This is a long line. This is a long line 2

The second submission was able to run code that the first submission placed in ``/tmp/a``. In addition to being a risk for competitive programming contests, this can also be detrimental to contests styles like code golf :cite:`code-golf-stack-exchange` which ranks submissions by their number of characters.
