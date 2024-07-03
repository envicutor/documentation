Implementation and Testing
##########################

Introduction
***************

This section outlines the testing methodologies and implementation strategies employed to ensure the robustness and reliability of Envicutor. To validate its effectiveness, a web application simulating a coding contest environment was developed, allowing real-world testing under various conditions including concurrent submissions and handling of malicious inputs.

Testing Methodologies
*********************

Various methodologies were employed to comprehensively evaluate Envicutor's performance and resilience.

Simulation Testing
==================

**Objective**: Validate Envicutor's functionality and performance in a realistic environment.

**Approach**:

* Deployed the web application to simulate a competitive programming contest, replicating real-world usage scenarios.
* Monitored system performance and response times under normal and peak loads.
* Evaluated Envicutor's ability to handle correct solutions, incorrect submissions, and edge cases.
* Conducted tests using a Python script to simulate malicious inputs during the contest, assessing Envicutor's resilience and integrity.

**Screenshots**:

The following screenshot shows a simulated contest's results and the verdicts returned by Envicutor against the original verdicts of their respective submissions on Codeforces, where we gathered our dataset.

.. figure:: figures/contest_result.png
  :alt: Contest Result Page

  Contest Result


.. figure:: figures/add_runtime.png
  :alt: Add Runtime Page

  Adding a runtime environment

.. figure:: figures/runtime_added.png
  :alt: Runtime added

  Runtime Added successfully

.. figure:: figures/runtime_used.png
  :alt: Runtime in use

  Runtime environment being used



API Testing
============

**Objective**: Validate Envicutor's functionality and performance through API interactions.


**Approach**:

* Developed NodeJs scripts to perform comprehensive API testing, covering all endpoints and typical usage scenarios.

* Conducted automated tests to ensure the API handles valid and invalid requests appropriately.

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
    Simple Python code which tests that environment variables are correctly set.
#. Execute C++ with compile error
    Simple C++ code that tests how Envicutor handles code submissions which fail to compile.
#. Execute erroneous Python code
    Simple Python code that tests how Envicutor handles code submissions which contain a syntax error.
#. Install Bash
    A request that tests if Envicutor can handle installation of Bash runtime.
#. Create a directory that can't be removed
    Bash command that tests if Envicutor can create and change permissions of the directory to only be deleted by the owner.
#. Execute over-cpu-time limit Python code
    Simple Python code that tests how Envicutor handles code that exceeds the time limit and asserts that exit status refers to time out.
#. Execute over-memory-limit C++ code
#. Execute under-memory-limit C++ code
#. Execute over-wall-time-limit Python code
#. Execute below-wall-time-limit Python code
#. Execute over-number-of-processes-limit Python code
#. Execute below-number-of-processes-limit Python code
#. Execute above-number-of-processes-limit Python code
#. Execute above-number-of-processes-limit Python code using threads
#. Abort mid-submission (should not cause Envicutor errors)
#. Execute Python code with invalid run wall_time
#. Execute Python code with invalid run cpu_time
#. Execute Python code with invalid run memory
#. Execute Python code with invalid run extra_time
#. Execute Python code with invalid run max_open_files
#. Execute Python code with a higher max_open_files limit (should not be able to open all of them)
#. Execute Python code with a lower max_open_files limit
#. Execute Python code with invalid run max_file_size
#. Execute over-file-size-limit Python code
#. Execute under-file-size-limit Python code
#. Execute Python code with invalid run max_number_of_processes
#. Make a runtime for multi-file Python projects that run through first.py
#. Make a runtime for multi-file C++ projects that run through first.cpp
#. Execute a multi-file Python project
#. Execute a multi-file C++ project

**Concurrency.js**


#. Executing MAX_CONCURRENT_SUBMISSIONS Python submissions in parallel
#. Executing MAX_CONCURRENT_SUBMISSIONS * 2 Python submissions in parallel (the second MAX_CONCURRENT_SUBMISSIONS should be blocked for some time)
#. Executing MAX_CONCURRENT_SUBMISSIONS * 2 C++ submissions in parallel (the second MAX_CONCURRENT_SUBMISSIONS should be blocked for some time)
#. Executing Math.ceil(MAX_CONCURRENT_SUBMISSIONS / 2) submissions after a package installation has started (they should start after the installation)
#. Running a package installation after executing Math.ceil(MAX_CONCURRENT_SUBMISSIONS / 2) submissions has started (it should start after the executions finish)
#. Running a package installation after another installation has started (it should start after the installation finishes)
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
    This test evaluates the performance of Envicutor when executing multiple C++ submissions in parallel.

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

Security Testing
================

**Objective**: Ensure Envicutor's resilience against malicious inputs and maintain system integrity.


**Approach**:

* Injected malicious submissions during contest simulations to test resilience against code injection, infinite loops, and resource exhaustion.


Stress Testing
==============

**Objective**: Evaluate Envicutor's performance under increased workloads.


**Approach**:

* Implemented scripts to submit 5000 concurrent Python and 300 C++ submissions simultaneously.
* Monitored system behavior and performance metrics during stress tests.
