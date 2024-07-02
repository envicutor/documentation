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

Isolation using isolation tools (Judge0, Envicutor)
===================================================

Judge0 :cite:`judge0-repo` uses Isolate :cite:`isolate-repo` process isolation tool to isolate submissions from each other. This tool uses certain features of the Linux kernel such as namespaces and control groups to isolate processes from each other and control their execution limits as explained in ":ref:`isolation_tools`".

Insecure Isolate ``--share-net`` option
---------------------------------------

Isolate by default does not allow network access inside sandboxes. Judge0 has a configuration option that can enable submissions to choose whether or not they want internet access while executing the submission. If this configuration option is enabled, and if the submissions choose to have internet access, Judge0 will make use of the ``--share-net`` option in Isolate as seen in Judge0's code :cite:`judge0-share-net`:

.. code-block:: ruby
  :emphasize-lines: 6

  command = "isolate #{cgroups} \
  -s \
  -b #{box_id} \
  -M #{metadata_file} \
  #{submission.redirect_stderr_to_stdout ? "--stderr-to-stdout" : ""} \
  #{submission.enable_network ? "--share-net" : ""} \
  -t #{submission.cpu_time_limit} \
  -x #{submission.cpu_extra_time} \
  -w #{submission.wall_time_limit} \
  -k #{submission.stack_limit} \
  -p#{submission.max_processes_and_or_threads} \
  #{submission.enable_per_process_and_thread_time_limit ? (cgroups.present? ? "--no-cg-timing" : "") : "--cg-timing"} \
  #{submission.enable_per_process_and_thread_memory_limit ? "-m " : "--cg-mem="}#{submission.memory_limit} \
  -f #{submission.max_file_size} \
  -E HOME=/tmp \
  -E PATH=\"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\" \
  -E LANG -E LANGUAGE -E LC_ALL -E JUDGE0_HOMEPAGE -E JUDGE0_SOURCE_CODE -E JUDGE0_MAINTAINER -E JUDGE0_VERSION \
  -d /etc:noexec \
  --run \
  -- /bin/bash $(basename #{run_script}) \
  < #{stdin_file} > #{stdout_file} 2> #{stderr_file} \
  "

In Isolate's user manual, this option is documented as follows:

  By default, isolate creates a new network namespace for its child process. This namespace contains no network devices except for a per-namespace loopback. This prevents the program from communicating with the outside world. If you want to permit communication, you can use this switch to keep the child process in parent’s network namespace.

Sharing the parent's network namespace leads to the violation of principles of isolation: if a submission binds on a certain localhost port, another submission cannot bind on it and can communicate with the other submission through this port.

This violation of isolation is illustrated by the following Linux command which spawns two Isolate sandboxes with the ``--share-net`` option. One sandbox binds on localhost:8000 and the other fetches data from it:

.. code-block:: bash

  isolate --init -b0 &&
  isolate --run --share-net --processes=4 --wall-time=10 -- /bin/python3 -m http.server &
  isolate --init -b1 &&
  sleep 0.2 && isolate --run --share-net -b1 --processes=4 -- /bin/curl http://127.0.0.1:8000

The following output can be observed indicating that the second sandbox was able to receive data from the first:

.. code-block:: html

  <!DOCTYPE HTML>
  <html lang="en">
  <head>
  <meta charset="utf-8">
  <title>Directory listing for /</title>
  </head>
  <body>
  <h1>Directory listing for /</h1>
  <hr>
  <ul>
  </ul>
  <hr>
  </body>
  </html>

In order to solve such problem, one would need to implement an network-interface-cloning method like the one used in Docker containers. However, even that does not entirely solve the problem; submissions might be able to send requests to nodes on the same network as the host node (the router does not know such requests are coming from the sandboxes). So if we have a database server in the same network as that of the node hosting the code execution system, the submissions will be to access it. Some sort of firewall would be needed. This was the cause of a critical security vulnerability in Judge0 :cite:`judge0-share-net-vulnerability`.

As a result of the previous complications, we decided that the return-on-investment for securely implementing an internet access solution is low and that the risk of insecurely implementing one is high.

Having a per-submission loopback interface
------------------------------------------

Web development assignment graders require submissions to bind to specific ports on localhost. This binding is accomplished through Linux network interfaces known as loopback interfaces. Envicutor, utilizing an updated version of Isolate, can create an isolated loopback interface for each submission (without the ``--share-net`` option). As of this writing, this capability is not available on Judge0 because it uses an older version of Isolate.

.. _isolate_systemd:

Using Isolate without systemd
-----------------------------

New versions of Isolate use cgroup2 :cite:`cgroup2-documentation` which is an improved way to manage processes' resources in Linux. The following diagram illustrates how cgroup2 works:

.. figure:: figures/cgroup2.png
  :alt: cgroup2
  :scale: 50%

  How cgroup2 works

Initially, Isolate ensured the presence of the "Isolate cgroup" by leveraging a systemd :cite:`systemd-homepage` service that initializes after system boot :cite:`isolate-systemd-service`. However, Docker containers, such as those used by Envicutor, better operate without a traditional heavyweight init system like systemd, which disrupts their streamlined workflow.

To address this, we've developed a custom fork of Isolate that operates independently of systemd. Moreover, we use a container startup script (an entrypoint) to emulate the systemd service's functionality. This approach guarantees the proper initialization of the Isolate cgroup while aligning seamlessly with Docker's lightweight container model.

The following, as of this writing, is the snippet of the startup script we use that is concerned with setting up the cgroup (additional comments are added for illustration):

.. code-block:: bash

  cd /sys/fs/cgroup && \
  # Create the isolate cgroup
  mkdir isolate/ && \
  # Move the init process under the isolate cgroup tree to be able to modify the root cgroup
  echo 1 > isolate/cgroup.procs && \
  # Any cgroup created under the root cgroup tree can manage cpu and memory limits in addition to other constraints
  echo '+cpuset +cpu +io +memory +pids' > cgroup.subtree_control && \
  cd isolate && \
  # Make a cgroup under the isolate tree
  mkdir init && \
  # Move the init process under the child cgroup to be able to modify the isolate cgroup
  echo 1 > init/cgroup.procs && \
  # Any cgroup created under the Isolate cgroup can manage cpu and memory limits
  echo '+cpuset +memory' > cgroup.subtree_control && \
  echo "Initialized cgroup"

Judge0 uses cgroup v1 since it is using an older Isolate version as of this writing :cite:`judge0-isolate`.

Deciding between Isolate and NsJail
-----------------------------------

NsJail is another process isolation tool for Linux :cite:`nsjail-repo`. From NsJail's GitHub repository's README:

  NsJail is a process isolation tool for Linux. It utilizes Linux namespace subsystem, resource limits, and the seccomp-bpf syscall filters of the Linux kernel.

It is used by code execution systems like Sandkasten :cite:`sandkasten-repo`.

Nsjail, however, does not provide ways for limiting the total CPU time via cgroup (only CPU-time-per-second can be limited) that can be used by the submission processes and does not provide a built-in way to report the metrics used by the submission. Hence, we opted to use Isolate since it seems to be better suited for code execution systems like Envicutor.

Execution limits
****************

Time limits
===========

Piston code execution system :cite:`piston-repo` uses the ``timeout`` Linux command and a programmed timeout interval to terminate a process that exceeds its time limit :cite:`piston-timeout`. This method measures wall-time, which is the total elapsed time from start to finish of the process, and does not consider CPU-time, which is the actual time the CPU spends executing the process.

As a result, if multiple submissions are running on the system simultaneously and the CPU is frequently context-switching between them due to the scheduling algorithm, the wall-time will include periods when the process is not being actively executed by the CPU. This can lead to inconsistencies in time-limiting submissions for competitive programming contests. Therefore, the preferred method for limiting the execution time in such contests is to measure CPU-time, as it provides a more accurate representation of the resources consumed by the process. Wall-time limitations are used mainly to ensure that a process does not run indefinitely and cause system hang-ups.

Envicutor and Judge0 provide options to limit both wall-time and CPU-time via their usage of Isolate.

Memory limits
=============

Piston code execution system uses the ``prlimit`` system command with the ``--as`` option to limit the amount of memory a process can allocate :cite:`piston-as`. This approach, however, enforces the memory limits on the processes and their children individually.

This can be suboptimal in some client systems which might want to limit that total memory that is used by a submission. Client systems that wish to limit the total memory usage will either have to limit the total number of processes in a submission to 1 or to ensure that ``max_number_of_processes * memory_limit = total_limit``. Both options can be constraining.

Envicutor and Judge0 provide an option to limit the total used memory through their usage of cgroup via Isolate. Though, Envicutor uses cgroup v2 while Judge0 uses cgroup v1 as discussed in ":ref:`isolate_systemd`".

Execution metrics
=================

Piston only reports standard output, standard error, exit signal and exit code :cite:`piston-metrics`. Envicutor and Judge0 add performance metrics such as cpu time, wall time and memory. These metrics are reported by Isolate and can be useful as described in ":ref:`improvement_areas`".

Package installation and runtimes management
********************************************

This section describes different approaches code execution systems use to manage package installation and managing runtimes as explained in :ref:`improvement_areas`, and the approach Envicutor uses.

All the runtime packages and dependencies are baked in the Docker image (Judge0)
================================================================================

Judge0 specifies the packages that are needed for the runtimes of the code execution system in its system's docker image :cite:`judge0-base-docker-image`.
The implications of such method is that a system reboot is needed to add new packages, and build/runtimes dependencies that a package requires need to be installed globally on the system. This can be problematic if two packages have conflicting dependencies.

For example, notice how the dependencies for the Octave programming language are installed globally using the ``apt`` package manager in the following snippet from the Dockerfile of the base docker image:

.. code-block:: dockerfile
  :emphasize-lines: 5

  ENV OCTAVE_VERSIONS \
        5.1.0
  RUN set -xe && \
      apt-get update && \
      apt-get install -y --no-install-recommends gfortran libblas-dev liblapack-dev libpcre3-dev && \
      rm -rf /var/lib/apt/lists/* && \
      for VERSION in $OCTAVE_VERSIONS; do \
        curl -fSsL "https://ftp.gnu.org/gnu/octave/octave-$VERSION.tar.gz" -o /tmp/octave-$VERSION.tar.gz && \
        mkdir /tmp/octave-$VERSION && \
        tar -xf /tmp/octave-$VERSION.tar.gz -C /tmp/octave-$VERSION --strip-components=1 && \
        rm /tmp/octave-$VERSION.tar.gz && \
        cd /tmp/octave-$VERSION && \
        ./configure \
          --prefix=/usr/local/octave-$VERSION && \
        make -j$(nproc) && \
        make -j$(nproc) install && \
        rm -rf /tmp/*; \
      done

In this example, several packages required for building Octave, such as ``gfortran``, ``libblas-dev``, ``liblapack-dev``, and ``libpcre3-dev``, are installed using apt-get. The curl command is then used to download the Octave source code, which is subsequently compiled and installed.

However, this method can pose challenges. For instance, if another language or tool requires a different version of ``liblapack-dev``, it could lead to conflicts and potentially break existing setups.

Runtime packages are installed while running the system, dependencies are baked in the Docker image (Piston)
============================================================================================================

Piston allows pre-compiled binaries of the packages required for the runtime to be downloaded while the code execution system is running :cite:`piston-runtime-installation`. This solves the problem of having to reboot a system to add a new runtime, but still does not solve the problem of having the dependencies for running the packages of the runtime installed globally on the system.

The following is a snippet from the Dockerfile of Piston's base Docker image :cite:`piston-dockerfile`:

.. code-block:: dockerfile

  RUN apt-get update && \
      apt-get install -y libxml2 gnupg tar coreutils util-linux libc6-dev \
      binutils build-essential locales libpcre3-dev libevent-dev libgmp3-dev \
      libncurses6 libncurses5 libedit-dev libseccomp-dev rename procps python3 \
      libreadline-dev libblas-dev liblapack-dev libpcre3-dev libarpack2-dev \
      libfftw3-dev libglpk-dev libqhull-dev libqrupdate-dev libsuitesparse-dev \
      libsundials-dev libpcre2-dev && \
      rm -rf /var/lib/apt/lists/*

Runtime packages and their dependencies are installed while running the system and all packages are isolated from each other (Envicutor)
========================================================================================================================================

As explained in ":ref:`nix_package_management`", Envicutor uses Nix to handle runtime installation while the system is running. Nix operates in such a way that all packages and their dependencies are isolated from each other and that packages with different dependencies can co-exist on the same system :cite:`nix-phd`.

The client system passes a "nix shell file" :cite:`nix-shell-docs` (shell.nix) to Envicutor, specifies the runtime name, the compile command, the run command, and the main source file name, and Envicutor handles setting up this runtime. The following pseudocode is an example of a request that is sent to Envicutor to have a Python runtime available:

.. code-block::

  sendRequest('POST', `${BASE_URL}/runtimes`, {
        name: 'Python',
        nix_shell: `
  { pkgs ? import (
    fetchTarball {
      url="https://github.com/NixOS/nixpkgs/archive/72da83d9515b43550436891f538ff41d68eecc7f.tar.gz";
      sha256="177sws22nqkvv8am76qmy9knham2adfh3gv7hrjf6492z1mvy02y";
    }
  ) {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
        python3
    ];
  }`,
        compile_script: '',
        run_script: 'python3 main.py',
        source_file_name: 'main.py'
      })

This leads to the following nix file being sent to Envicutor:

.. code-block:: nix

  { pkgs ? import (
    fetchTarball {
      url="https://github.com/NixOS/nixpkgs/archive/72da83d9515b43550436891f538ff41d68eecc7f.tar.gz";
      sha256="177sws22nqkvv8am76qmy9knham2adfh3gv7hrjf6492z1mvy02y";
    }
  ) {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
        python3
    ];
  }

Overcoming the slow startup time of nix-shell
---------------------------------------------

Since Nix packages are isolated from each other and from the global execution environment, the ``nix-shell`` command must be used to make the packages specified in the ``shell.nix`` file available in the current environment (even if the Nix packages are downloaded on the system).

The problem is that Nix needs to do a lot of computations in order to parse the packages in ``shell.nix``, identify where they point to on the system and download non-existing packages. For example, running the ``nix-shell`` command on the previous nix file containing the python package takes about 650 milliseconds to make the environment available on the machine of the author of this part of the document (with the Nix Python packages already downloaded).

If we consider that the following Python program, that does about one million Python operations, takes 150 milliseconds on the same machine, we can see how large of an overhead the ``nix-shell`` command becomes:

.. code-block:: python

  i = 0
  for i in range(1000000):
      i += 1

One million operations can be considered a common number of operations in competitive programming problems test cases. So, aside from performance problems, such overhead will also introduce challenges with setting the time limits on problems (having to account for the cpu time of the nix-shell startup in addition to the cpu time of the submission).

To optimize our environment setup process, we implemented a solution where the ``nix-shell`` command is executed only once after adding the runtime. Adding the runtime is handled by a separate endpoint from the code execution endpoint. We then cache the resulting environment variables by running the ``env`` command within the created Nix environment and saving its output to a file. Before executing a code submission, these cached environment variables are loaded into the environment, eliminating the need to run ``nix-shell`` again.

The following code snippet from Envicutor shows how the ``env`` command is used to get the environment variables of the nix shell while adding a new runtime:

.. code-block:: rust
  :emphasize-lines: 1,4,12

  let mut cmd = Command::new("env");
  cmd.arg("-i")
      .arg("PATH=/bin")
      .arg(format!("{NIX_BIN_PATH}/nix-shell"))
      .args(["--timeout".to_string(), installation_timeout.to_string()])
      .arg(nix_shell_path)
      .args(["--run", "/bin/bash -c env"]);
  let cmd_res = cmd.output().await.map_err(|e| {
      eprintln!("Failed to run nix-shell: {e}");
      INTERNAL_SERVER_ERROR_RESPONSE.into_response()
  })?;
  let stdout = String::from_utf8_lossy(&cmd_res.stdout).to_string();
  let stderr = String::from_utf8_lossy(&cmd_res.stderr).to_string();

The following snippet shows how the output of the ``env`` command is saved to a file to cache the environment variables:

.. code-block:: rust
  :emphasize-lines: 4

  let env_script_path = format!("{runtime_dir}/env");
  crate::fs::write_file_and_set_permissions(
      &env_script_path,
      &stdout,
      Permissions::from_mode(0o755),
  )
  .await
  .map_err(|e| {
      eprintln!("Failed to write env script: {e}");
      INTERNAL_SERVER_ERROR_RESPONSE.into_response()
  })?;

The following snippet shows a part of the process of loading the environment variables into the environment of the submission:

.. code-block:: rust
  :emphasize-lines: 37

  async fn add_env_vars_from_file(cmd: &mut Command, file_path: &str) -> Result<(), Error> {
      let env = fs::read_to_string(file_path)
          .await
          .map_err(|e| anyhow!("Failed to read environment variables from: {file_path}: {e}"))?;
      let lines = env.lines();

      let mut line_count = 0;
      let mut key = String::new();
      let mut value = String::new();
      for line in lines {
          if line.contains('=') {
              if !key.is_empty() {
                  cmd.env(&key, &value);
              }
              let mut entry: Vec<&str> = line.split('=').collect();
              value = match entry.pop() {
                  Some(e) => e.to_string(),
                  None => {
                      return Err(anyhow!("Found a bad line in the env file: {file_path}"));
                  }
              };
              key = match entry.pop() {
                  Some(e) => e.to_string(),
                  None => {
                      return Err(anyhow!("Found a bad line in the env file: {file_path}"));
                  }
              };
          } else {
              value.push('\n');
              value.push_str(line);
          }
          line_count += 1;
          if line_count % 500 == 0 {
              yield_now().await;
          }
      }
      cmd.env(&key, &value);
      Ok(())
  }

Concurrency
***********

For reasons discussed in ":ref:`objectives`", only a certain number of submissions shall be allowed to run at a time on the system. This section describes different approaches code execution systems take to ensure that, and the approach that Envicutor takes.

Programmed semaphore in Node.js (Piston)
========================================

Piston uses a semaphore that is manually programmed in Node.js to limit the number of submissions that can run at a time. The following code snippet in Piston shows the process of a acquiring a semaphore permit with some added comments for illustration :cite:`piston-job-file`:

.. code-block:: javascript

  if (remaining_job_spaces < 1) { // If all semaphore permits are taken
      this.logger.info(`Awaiting job slot`);
      await new Promise(resolve => {
          job_queue.push(resolve);
      }); // Stay blocked till this promise gets resolved (by releasing a permit in another semaphore)
  }
  this.logger.info(`Priming job`);
  remaining_job_spaces--; // Acquire the semaphore

The following code snippet in Piston shows the process of releasing the semaphore permit after the submission finishes with some added comments for illustration:

.. code-block:: javascript

  async cleanup() {
      this.logger.info(`Cleaning up job`);

      this.exit_cleanup(); // Run process janitor, just incase there are any residual processes somehow
      this.close_cleanup();
      await this.cleanup_filesystem();

      remaining_job_spaces++; // Increase the number of available permits
      if (job_queue.length > 0) {
          job_queue.shift()(); // Release the permit (unblock the waiting jobs)
      }
  }

Using manually programmed semaphores like this can lead to data races and inefficiencies, particularly if not carefully managed.

Resque workers (Judge0)
=======================

Judge0 makes use of task queues and workers that pull tasks from these queues using Resque :cite:`resque-homepage`. It provides a way to configure the number of workers that can run concurrently :cite:`judge0-workers`. Such approach helps in scalability since workers can distributed across multiple machines.

Tokio Semaphore and RwLock (Envicutor)
======================================

Envicutor makes use of the Semaphore :cite:`tokio-semaphore` and RwLock :cite:`tokio-rwlock` objects in Rust's asynchronous runtime: Tokio :cite:`tokio-homepage`. These primitives help manage concurrent access to resources and ensure safety through Rust's ownership system and compile-time checks.

In Envicutor, we ensure that no submissions can run while a runtime installation is in progress. This is to ensure that the resources used by the installation process does not affect the resources needed by the submissions. We also ensure that no two installation processes can run at the same time. This is to avoid concurrency issues with Nix.

To ensure that only one installation can run at a time without any concurrent submissions, an RwLock is used. An RwLock is a synchronization primitive that allows multiple readers but only one writer at a time. During the installation process, a "write lock" is acquired before it begins and released after it ends, ensuring exclusive access for the installation. The submission execution process acquires a "read lock" before it begins and releases it after it ends. Because the read lock is acquired from the same RwLock as the installation, submissions are blocked if there is an ongoing installation, preventing any concurrent submissions during that time. However, if there is no installation in progress, multiple submissions can run concurrently as they only require read locks, allowing them to proceed simultaneously.

We believe such blocking should not cause major performance downsides since runtimes installation is an infrequent operation.

To limit the number of submissions that can run concurrently at a time, we use a Semaphore. A Semaphore is a synchronization primitive that controls access to a shared resource by maintaining a set number of permits. Each submission acquires a permit before it begins and releases it after it ends. If all permits are taken, additional submissions must wait until a permit is released. This ensures that no more than the specified number of submissions can run at the same time, effectively limiting concurrency and preventing resource exhaustion.

Envicutor leaves scalability decisions up to the client system.
