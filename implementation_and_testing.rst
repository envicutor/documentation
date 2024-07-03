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

* Developed JavaScript scripts to perform comprehensive API testing, covering all endpoints and typical usage scenarios.

* Conducted automated tests to ensure the API handles valid and invalid requests appropriately.

* Evaluated the API's performance under concurrent access conditions.

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
