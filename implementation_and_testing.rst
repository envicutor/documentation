Implementation and Testing
##########################

Introduction
***************

This section outlines the testing methodologies and implementation strategies employed to ensure the robustness and reliability of Envicutor.

Testing Methodologies
*********************

Various methodologies were employed to comprehensively evaluate Envicutor's performance and resilience.

Simulation Testing
==================

**Objective**: validate Envicutor's functionality and performance in a realistic environment.

**Approach**:

* Developed a web application that simulates a real programming contest and uses Envicutor as its code execution system.
* Evaluated Envicutor's ability to handle code execution, and various resource limits.
* Developed a Python script to simulate malicious inputs during the contest, assessing Envicutor's resilience.

**Screenshots**:

The following screenshot shows a simulated contest's results and the verdicts returned by Envicutor against the original verdicts of their respective submissions on Codeforces, where we gathered our dataset.

.. figure:: figures/contest_result.png
  :alt: Contest Result Page

  Contest result

The following screenshots show the addition of a new runtime through the simulation web application.

.. figure:: figures/add_runtime.png
  :alt: Add Runtime Page

  Adding a runtime environment

.. figure:: figures/runtime_added.png
  :alt: Runtime added

  Runtime added successfully

.. figure:: figures/runtime_used.png
  :alt: Runtime in use

  Runtime environment being used



API Testing
============

**Objective**: validate Envicutor's functionality and concurrency-handling.


**Approach**:

* Developed Node.js scripts to perform comprehensive API testing, covering all endpoints and typical usage scenarios.

* Evaluated the API's performance under concurrent access conditions.

**Scripts**:

**installation.js**

#. Installing Python
    Checks that Envicutor can install Python correctly.
#. Installing Python again (should fail)
    Checks that Envicutor handles duplicate installations correctly.
#. Listing runtimes (should have Python)
    Checks that the list of runtimes contains Python after installation.
#. Updating Nix
    Checks if Envicutor can update Nix successfully.
#. Deleting runtime with id 2 (invalid)
    Checks if Envicutor can handle invalid deletion IDs.
#. Deleting runtime with id 1 (delete Python)
    Checks if Envicutor can delete runtimes
#. Listing runtimes (should be empty)
    Checks if Python has been successfully removed.
#. Installing Python
    Checks if Python can be reinstalled after deletion.
#. Installing C++ via gcc
    Checks if Envicutor can install C++
#. Making an installation that will fail
    Checks if Envicutor can handle invalid runtime installation requests.

**Simple.js**

#. Listing runtimes (should have Python and C++)
    Checks that Envicutor lists both Python and C++ after installation.
#. Executing Python code
    Checks if Python operates correctly.
#. Executing C++ code
    Checks if C++ operates correctly.


**Complex.js**

#. Check the environment variables in python
    Check if environment variables are correctly set.
#. Execute C++ with compile error
    Check if Envicutor can handle compile errors.
#. Execute erroneous Python code
    Check if Envicutor can handle run errors.
#. Install Bash
#. Create a directory that can't be removed
    Checks that Envicutor can create and change permissions of the directory even if the submission modified its permissions.
#. Execute over-cpu-time limit Python code
    Checks that Envicutor can handle code that exceeds the time limit and asserts that exit status refers to time out.
#. Execute over-memory-limit C++ code
    Checks that Envicutor can handle code that exceeds the memory limit and asserts that exit status refers to memory limit.
#. Execute under-memory-limit C++ code
    Checks that Envicutor can handle code that is under the memory limit and it runs successfully.
#. Execute over-wall-time-limit Python code
    Checks that Envicutor can handle code that exceeds the wall limit.
#. Execute below-wall-time-limit Python code
    Checks that Envicutor can handle submissions that are under the wall limit and it runs successfully.
#. Execute over-number-of-processes-limit Python code
    Checks that Envicutor can handle submissions that exceeds the number of processes limit.
#. Execute below-number-of-processes-limit Python code
    Checks that Envicutor can handle submissions that are under the number of processes limit and it runs successfully.
#. Execute above-number-of-processes-limit Python code
    Checks that Envicutor can handle submissions that exceeds the number of processes limit.
#. Execute above-number-of-processes-limit Python code using threads
    Checks that Envicutor can handle submissions that exceeds the number of processes limit with threading.
#. Abort mid-submission (should not cause Envicutor errors)
    Checks that Envicutor can handle submissions that are aborted mid-submission.
#. Execute Python code with invalid run wall_time
    Checks that Envicutor can handle submissions with invalid wall time.
#. Execute Python code with invalid run cpu_time
    Checks that Envicutor can handle submissions with invalid cpu time.
#. Execute Python code with invalid run memory
    Checks that Envicutor can handle submissions with invalid memory.
#. Execute Python code with invalid run extra_time
    Checks that Envicutor can handle submissions with invalid extra time.
#. Execute Python code with invalid run max_open_files
    Checks that Envicutor can handle submissions with invalid max open files.
#. Execute Python code with a higher max_open_files limit (should not be able to open all of them)
    Checks that Envicutor can handle submissions that has more files than the max open files limit.
#. Execute Python code with a lower max_open_files limit
    Checks that Envicutor can handle submissions that has less files than the max open files limit and it runs succcessfully.
#. Execute Python code with invalid run max_file_size
    Checks that Envicutor can handle submissions with invalid max file size.
#. Execute over-file-size-limit Python code
    Checks that Envicutor can handle submissions that exceeds the file size limit.
#. Execute under-file-size-limit Python code
    Checks that Envicutor can handle submissions that is under the file size limit and it runs successfully.
#. Execute Python code with invalid run max_number_of_processes
    Checks that Envicutor can handle submissions with invalid max number of processes.
#. Make a runtime for multi-file Python projects that run through first.py
#. Make a runtime for multi-file C++ projects that run through first.cpp
#. Execute a multi-file Python project
    Checks if Envicutor can execute a multi-file project in a runtime that does not require compilation.
#. Execute a multi-file C++ project
    Checks if Envicutor can execute a multi-file project in a runtime that requires compilation.

**Concurrency.js**

#. Executing MAX_CONCURRENT_SUBMISSIONS Python submissions in parallel
    Checks if Envicutor can execute MAX_CONCURRENT_SUBMISSIONS Python submissions in parallel (nothing should be blocked).
#. Executing MAX_CONCURRENT_SUBMISSIONS * 2 Python submissions in parallel (the second MAX_CONCURRENT_SUBMISSIONS should be blocked for some time)
    Checks if Envicutor correctly blocks half of the submissions in case they were double the number of the maximum concurrent submissions.
#. Executing MAX_CONCURRENT_SUBMISSIONS * 2 C++ submissions in parallel (the second MAX_CONCURRENT_SUBMISSIONS should be blocked for some time)
    Same as above but for a runtime that requires compilation.
#. Executing Math.ceil(MAX_CONCURRENT_SUBMISSIONS / 2) submissions after a package installation has started (they should start after the installation)
    Checks if Envicutor correctly blocks submissions while a package installation is running as described in ":ref:`concurrency`".
#. Running a package installation after executing Math.ceil(MAX_CONCURRENT_SUBMISSIONS / 2) submissions has started (it should start after the executions finish)
    Checks if Envicutor can correctly block package installations while executing Math.ceil(MAX_CONCURRENT_SUBMISSIONS / 2) submissions in parallel as described in ":ref:`concurrency`".
#. Running a package installation after another installation has started (it should start after the installation finishes)
    Checks if Envicutor can correctly block package installations while another one is running as described in ":ref:`concurrency`".
#. Getting the available runtimes while an installation is running (should not be blocked)

**stress.js**

#. Executing 5000 Python submissions in parallel
    This test evaluates the reliability of Envicutor when executing multiple Python submissions in parallel.

    .. code-block:: javascript

        console.log('Executing 5000 Python submissions in parallel');
        const promises = [];
        for (let i = 0; i < 5000; ++i) {
          promises.push(
            sendRequest('POST', `${BASE_URL}/execute`, {
              runtime_id: 2,
              source_code: 'print(input())',
              input: 'Hello world'
            })
          );
        }
        const before = new Date();
        const responses = await Promise.all(promises);
        console.log(`Time taken: ${new Date() - before} ms`);
        for (const res of responses) {
          const text = await res.text();
          assert.equal(res.status, 200);
          const body = JSON.parse(text);
          assert.equal(body.run.stdout, 'Hello world\n');
          assert.equal(body.run.stderr, '');
        }
#. Executing 300 C++ submissions in parallel
    This test evaluates the reliability of Envicutor when executing multiple C++ submissions (a runtime that requires compilation) in parallel.

    .. code-block:: javascript

        console.log('Executing 300 C++ submissions in parallel');
        const promises = [];
        for (let i = 0; i < 300; ++i) {
          promises.push(
            sendRequest('POST', `${BASE_URL}/execute`, {
              runtime_id: 3,
              source_code: `#include <fstream>
                int main() {
                  printf("Hello world\\n");
                  return 0;
                }`
            })
          );
        }
      const before = new Date();
      const responses = await Promise.all(promises);
      console.log(`Time taken: ${new Date() - before} ms`);
      for (const res of responses) {
        const text = await res.text();
        assert.equal(res.status, 200);
        const body = JSON.parse(text);
        assert.equal(body.run.stdout, 'Hello world\n');
        assert.equal(body.run.stderr, '');
      }
