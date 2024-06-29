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

We categorize code execution systems into two types: ones that provide long-lived code execution environments, and ones that handle short-lived submissions that must execute with the least overhead.

The former is used in cloud development environments and online IDEs that need to maintain state while executing code multiple times. Such code execution systems need to provide long-lived code execution environments for the developers even if overhead such as startup time is incurred. An open source example of such system would be the code execution system powering Riju :cite:`riju-github`. Another example is the proprietary code execution system powering Repl.it :cite:`replit-homepage`.

The second category is used in programming competition websites and auto-graders. Such code execution systems need to execute the programmer's code with the least overhead (we refer to such execution as a submission) without worrying about retaining state between different submissions. Two open source examples that fit in this category are: Piston :cite:`piston-repo` and Judge0 :cite:`judge0-repo`.

Envicutor fits in the second category of code execution systems.
