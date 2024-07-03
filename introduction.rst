Introduction
############

Motivation
**********

Why did we create Envicutor?
============================

Having studied multiple open source code execution systems for the past three years, we started to notice the strengths and weaknesses of many of them. We aim to combine the strengths we have observed and avoid the weaknesses while introducing new methods of solving common problems through a new code execution system.

Why a code execution system?
============================

Code execution systems power other systems that make use of remote code execution; such as: online IDEs :cite:`emkc-snippets` :cite:`judge0-ide`, online assignment auto-graders, competitive programming systems :cite:`dmoj` and online interactive programming tutorials. We will refer to these systems as the client systems. By providing an improved code execution system, we can improve the user experience for the developers, the administrators, and the users of the client systems.

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

.. _improvement_areas:

The areas Envicutor aims to improve
===================================

Isolation
---------

We define isolation as the ability of the code execution system to make different submissions unaware of each other, unable to tamper with each other, and unable to tamper with the underlying system. Throughout the report, we discuss suboptimal isolation methods that are used by some code execution systems and how Envicutor handles isolation.

Execution limits
----------------

We define execution limits as the constraints that a submission is subject to; these include: CPU time, wall (real) time, memory usage, and other constraints.

Many systems that make use of remote code execution need to impose execution limits on submissions. For example, a competitive programming system needs to ensure the execution time for the competitors' submissions does not exceed the time limit that the judge determined for a certain problem (imposing a CPU-time limit) :cite:`codeforces-cpu-time-limit`.

We discuss suboptimal ways some code execution systems use to impose such constraints and how Envicutor imposes them.

Execution metrics
-----------------

We define execution metrics as quantitative and qualitative metrics that provide insights into the behavior and outcomes of a submission. These metrics include: CPU time, wall (real) time, memory usage, exit code, exit signal, standard output, standard error and other metrics.

In the competitive programming system example, the system also needs to know the standard output that executing a submission produced to be able to judge the submission against the test cases. Some competitive programming systems even give the competitors the ability to see how much CPU-time and memory their submissions consumed :cite:`codeforces-metrics`.

Package management
------------------

In order to execute a submission written in one or more programming languages, the compilers, the interpreters, and the libraries that are required to run code written in these languages shall exist on the system. We refer to such dependencies as "packages", and to environments containing these dependencies as "runtimes". We discuss how some package management methods that some code execution systems use can be problematic and we introduce a flexible way to manage packages and runtimes.

.. _objectives:

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

In order to ensure that all submissions get their fair share of system resources within the specified limits, only a certain number of submissions shall be allowed to run at a time. Otherwise, the system resources (as memory) can be exhausted and some submissions might not be able to make use of them.

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

Development methodology
***********************

Our development methodology is grounded in an iterative process of optimizing architecture and design through experimentation and prototyping. This approach is necessitated by the fact that Envicutor is based on integration with the operating system and various external tools.

Relying solely on a pre-implementation design phase is insufficient to guarantee system robustness, as the interaction with these external factors—such as the operating system and diverse tools—introduces variables that can impact the system's functionality, reliability, performance and security. Therefore, continuous experimentation and design refinement are essential to address and mitigate these external influences. Such experimentation and refinement are illustrated throughout the report.

During the initial phases of the project, our team adopted a collaborative approach characterized by design meetings and mob programming :cite:`mob-programming`. This strategy ensured that all team members worked on the same task simultaneously, fostering consensus on various design decisions and promoting a comprehensive understanding of the entire system among all participants.

In the later phases of the project, we transitioned to a more autonomous workflow by regularly posting GitHub issues detailing the tasks that needed to be completed. Our team operated in a self-organizing manner, with each member selecting and assigning themselves to the issues they felt most comfortable and skilled at addressing. This approach optimized task distribution based on individual expertise and preference.

Used tools
**********

Programming languages
=====================

We chose to write Envicutor in Rust :cite:`rust-homepage`. Rust has powerful concurrency APIs that helps us in managing different concurrency scenarios in submissions as we will discuss throughout the report. Moreover, it provides extensive compile-time checks that ensure correctness in multiple concurrency scenarios. This greatly improves productivity and boosts confidence in the quality of the software.

From Rust's networking page :cite:`rust-networking-page`:

  Concurrent at scale

  Use any mixture of concurrency approaches that works for you. Rust will make sure you don’t accidentally share state between threads or tasks. It empowers you to squeeze every last bit of scaling, fearlessly.

Our API tests, simulation tests, and demos are written in Node.js because these assets do not require the strict compile-time checks (or compilation in general) provided by Rust.

.. _isolation_tools:

Handling Isolation, execution limits and execution metrics
==========================================================

We use Isolate :cite:`isolate-repo` to execute submissions in an isolated sandbox, to impose limits on the submissions and to get the execution metrics. It is used in the International Olympiad in Informatics Contest Management System (IOI CMS) :cite:`cms-homepage` and in code execution systems like Judge0 :cite:`judge0-paper`.

From Isolate's GitHub repository README:

  Isolate is a sandbox built to safely run untrusted executables, like programs submitted by competitors in a programming contest. Isolate gives them a limited-access environment, preventing them from affecting the host system. It takes advantage of features specific to the Linux kernel, like namespaces and control groups.

.. _nix_package_management:

Package management
==================

We use Nix :cite:`nix-homepage` as our package manager. Nix has an approach to package management which ensures that multiple versions of the same package can exist on the system, and packages which have conflicting dependencies can co-exist safely on the system :cite:`nix-phd`. From Nix's homepage:

  Nix builds packages in isolation from each other. This ensures that they are reproducible and don’t have undeclared dependencies

Managing runtimes data
======================

We use SQLite :cite:`sqlite-homepage` to manage runtime data. Runtime data is local to every Envicutor node and doesn't typically have concurrent writers. This makes SQLite, rather than a client-server database, a good fit. From SQLite's "when to use" page :cite:`sqlite-when-to-use`:

  For device-local storage with low writer concurrency and less than a terabyte of content, SQLite is almost always a better solution. SQLite is fast and reliable and it requires no configuration or maintenance. It keeps things simple. SQLite "just works".

Containerization and reproducible deployments
=============================================

We use Docker :cite:`docker-homepage` to ensure we can spin up a reproducible environment that works seamlessly with Nix and Isolate.

Report organization
*******************

Chapter 2 discusses how different systems handle problems discussed in ":ref:`improvement_areas`" and their similarities and differences with Envicutor. It also highlights some challenges we faced while developing Envicutor and how we overcame them.

Chapter 3 answers the question: "what would a client system need in a code execution system" through illustrating the functional and non-functional requirements of Envicutor and its use case diagram.

Chapter 4 discusses the architecture and design of Envicutor and why certain design decisions were made.

Chapter 5 discusses how we maintain and test Envicutor.
