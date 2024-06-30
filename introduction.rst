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

We define isolation as the ability of the code execution system to make different submissions unaware of each other, unable to tamper with each other, and unable to tamper with the underlying system. Throughout this report, we discuss suboptimal isolation methods that are used by some code execution systems and how Envicutor handles isolation.

Execution limits
----------------

We define execution limits as the constraints that a submission is subject to; these include: CPU time, wall (real) time, memory usage, and other constraints. We discuss suboptimal ways some code execution systems use to impose such constraints and how Envicutor imposes them.

Execution metrics
-----------------

We define execution metrics as quantitative and qualitative metrics that provide insights into the behavior and outcomes of a submission. These metrics include: CPU time, wall (real) time, memory usage, exit code, exit signal, standard output, standard error and other metrics.

Package management
------------------

In order to execute a submission written in one or more programming languages, the compilers, the interpreters, and the libraries that are required to run code written in these languages shall exist on the system. We refer to such dependencies as "packages", and to environments containing these dependencies as "runtimes". We discuss how some package management methods that some code execution systems use can be problematic and we introduce a flexible way to manage packages and runtimes.
