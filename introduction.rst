Introduction
############

Motivation
**********

Why did we create Envicutor?
============================

Having studied multiple open source code execution systems for the past two years, we started to notice the strengths and weaknesses of many of them. We aim to combine the strengths we have observed and avoid the weaknesses while introducing new methods of solving common problems through a new code execution system.

Why a code execution system?
============================

Code executions systems power other systems that make use of remote code execution; such as: online IDEs :cite:`emkc-snippets` :cite:`judge0-ide`, online assignment auto-graders, competitive programming systems :cite:`dmoj` and online interactive programming tutorials. We will refer to these systems as the client systems. By providing an improved code execution system, we can improve the user experience for the developers, the administrators, and the users of the client systems.

Problem definition
******************

Formal definition of a code execution system
============================================

We define a code execution system as a backend system that provides remote code execution capabilities (typically through web technologies) to other systems.

Typical categories of code execution systems and which category Envicutor fits in
=================================================================================

We categorize code execution systems into two types: ones that provide long-lived code execution environments, and ones that handle short-lived code execution submissions that must execute with the least overhead.

The former is used in cloud development environments and online IDEs that need to maintain state while executing code multiple times. Such code execution systems need to provide long-lived code execution environments for the developers even if overhead such as startup time is incurred. An open source example of such system would be the code execution system powering Riju :cite:`riju-github`. Another example is the proprietary code execution system powering Repl.it :cite:`replit-homepage`.

The second category is used in programming competition websites and auto-graders. Such code execution systems need to execute the programmer's code with the least overhead (we refer to such execution as a submission) without worrying about retaining state between different submissions. Two open source examples that fit in this category are: Piston :cite:`piston-repo` and Judge0 :cite:`judge0-repo`.

Envicutor fits in the second category of code execution systems.

The areas Envicutor aims to improve
===================================

Isolation
---------

We define isolation as the ability of the code execution system to make different submissions unaware of each other, unable to tamper with each other, and unable to tamper with the underlying system. Throughout the report, we discuss suboptimal isolation methods that are used by some code execution systems and how Envicutor handles isolation.

Execution limits
----------------

We define execution limits as the constraints that a submission is subject to; these include: CPU time, wall (real) time, memory usage, and other constraints.

Many systems that make use of remote code execution need to impose execution limits on submissions. For example, a competitive programming system needs to ensure the execution time for the competitors' submissions does not exceed the time limit that the judge determined for a certain problem (imposing a CPU-time limit).\ :cite:`codeforces-cpu-time-limit`

We discuss suboptimal ways some code execution systems use to impose such constraints and how Envicutor imposes them.

Execution metrics
-----------------

We define execution metrics as quantitative and qualitative metrics that provide insights into the behavior and outcomes of a submission. These metrics include: CPU time, wall (real) time, memory usage, exit code, exit signal, standard output, standard error and other metrics.

In the competitive programming system example, the system also needs to know the standard output that executing a submission produced to be able to judge the submission against the test cases. Some competitive programming systems even give the competitors' the ability to see how much CPU-time and memory their submissions consumed.\ :cite:`codeforces-metrics`

Package management
------------------

In order to execute a submission written in one or more programming languages, the compilers, the interpreters, and the libraries that are required to run code written in these languages shall exist on the system. We refer to such dependencies as "packages", and to environments containing these dependencies as "runtimes". We discuss how some package management methods that some code execution systems use can be problematic and we introduce a flexible way to manage packages and runtimes.

Project objectives
******************

Isolation, execution limits and execution metrics
==================================================

Envicutor makes use of appropriate tools and methods to ensure submissions execute in a truly isolated sandboxed environment while ensuring a low overhead for executing submissions. It also uses these tools to impose execution limits and report the execution metrics. Throughout the report, we discuss the rationale behind our isolation tool selection and the strategies we employ to mitigate its quirks.

Package management
==================

Envicutor improves the ease with which packages are added to the system and runtimes are set up. Unlike some other code execution systems, a system reboot is not required to add a new runtime, multiple versions of the same package can exist on the system, and packages which have conflicting dependencies can co-exist safely on the same system. We discuss how this is done.

Concurrency
===========

Throughout the report, we discuss several strategies we use to ensure that multiple submissions can run concurrently on the system without exhausting its resources and without starving each other from resources.

Project work plan
*****************

.. list-table:: Work Plan
  :header-rows: 1
  :widths: 50 6
  :class: table-bordered

  * - Task
    - Status

  * - Brainstorm ideas for the project and pick the best idea
    - Done
  * - Analyze similar open source systems (skim the source code and check their github issues)
    - Done
  * - Come up with an abstract idea of the project and the problems it aims to solve
    - Done
  * - Re-analyze the open source systems to verify that the problems aren't already solved
    - Done
  * - Brainstorm the overview of the project
    - Done
  * - Write an initial developers' guide for collaborating on the project
    - Done
  * - Set up continuous integration and deployment (CI/CD) for the documentation of the project
    - Done
  * - Write an initial use-case diagram, component diagram and activity flow
    - Done
  * - Write an initial sequence diagram and an api documentation
    - Done
  * - Come up with different technologies that can be used
    - Done
  * - Experiment with the different technologies to validate feasibility and to choose the most appropriate technologies
    - Done
  * - Update the documentation based on the new findings
    - Done
  * - Write a throwaway prototype for the most crucial parts of the system to check feasibility
    - Done
  * - Update the documentation based on findings from the prototype
    - Done
  * - Write the initial pseudocode and class diagram
    - Done
  * - Work on runtimes management
    - Done
  * - Write runtimes management API tests
    - Done
  * - Work on code execution
    - Done
  * - Write code execution API tests
    - Done
  * - Update the documentation and architecture based on findings from working on the system
    - Done
  * - Work on simulation testing (simulating real contest submissions on Envicutor)
    - Done
  * - Refine the system with more features and optimizations, refine the API tests
    - Done
  * - Work on other demos of the system
    - Done
  * - Re-structure the documentation and write an API documentation for the system
    - Done
  * - Open source the system
    - Future
  * - Work on CI/CD for the system
    - Future
