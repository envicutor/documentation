System design diagrams
######################

System component diagram
************************

The following diagram shows the modules :cite:`rust-modules` that are used in Envicutor.

.. figure:: figures/component-diagram.png
  :scale: 80%
  :alt: component diagram

  Envicutor's component diagram

The API module contains the following modules:

- The ``listing`` module contains the handlers :cite:`axum-handler` and functions for listing runtimes
- The ``deletion`` module contains the handlers and functions for deleting runtimes
- The ``execution`` module contains the handlers and functions for executing submissions
- The ``installation`` module contains the handlers and functions for adding runtimes and updating Nix
- The ``common_function`` module contains common functions that are used in handlers
- The ``common_responses`` module contains common API response structs that are used in handlers

The rest of the modules are:

- The ``types`` module contains type aliases and structs that are commonly used
- The ``isolate`` module contains abstractions for using Isolate sandboxes (check ":ref:`isolation_tools`") and ensuring their cleanup
- The ``globals`` module contains global constants that are used in the code
- The ``transaction`` module contains abstractions for simulating SQLite database transaction rollbacks
- The ``strings`` module contains utilities that are used to deal with strings
- The ``temp_dir`` module contains abstractions for creating a temporary directory and ensuring its cleanup
- The ``limits`` module encapsulates logic for verifying a submission's request limits against the configured system limits as described in ":ref:`configuration`"
- The ``fs`` module contains utilities for dealing with the filesystem
- The ``main`` module contains the entry point of the application

Class diagram
*************

Rust provides different ways to implement object-oriented principles compared to typical Java object-oriented code :cite:`rust-oop`. For example, while Rust does not support inheritance, it uses traits to define shared behavior, serving as an alternative to inheritance and polymorphism :cite:`rust-inheritance` :cite:`rust-traits`. Encapsulation is managed via the module system, which controls the visibility of functions, structs, and other items :cite:`rust-encapsulation`.

As a result, using UML class diagrams to represent our Rust codebase can be challenging. For example, how does one represent implementing a local trait for an external struct? How does one represent public/private module functions and constants that are not associated with a struct? Unique aspects of Rust like these require adaptations or extensions to traditional UML diagrams to accurately model the codebase.

As a result we believe the component diagram, along with the explanation of each component, should be sufficient to provide an overview of how the system works. That said, the following are class diagrams that attempt to show a simplified overview of Envicutor's design.

Functions and constants that are not associated with a struct are placed in UML classes called ``mod``. Note that some associations will not be shown in the following class diagrams for simplicity.

.. figure:: figures/class-diagram-api-mod.png
  :alt: api mod class diagram

  A class diagram of the API module and the modules inside of it


.. figure:: figures/class-diagram-root-crate.png
  :alt: root crate class diagram

  A class diagram of the rest of the modules

Sequence diagrams
*****************

Adding a new runtime
====================

The following sequence diagram shows an overview of how a new runtime is added to the system. It also shows how the environment variables from the Nix shell are cached as described in ":ref:`nix_slow_startup`":

.. figure:: figures/add-runtime-sequence.png
  :alt: adding a runtime sequence diagram

  Sequence diagram for adding a new runtime

Listing the available runtimes
==============================

.. figure:: figures/listing-runtimes-sequence.png
  :alt: listing runtimes sequence diagram

  Sequence diagram for listing the available runtimes

Deleting a runtime
==================

.. figure:: figures/deleting-runtime-sequence.png
  :alt: deleting runtime sequence diagram

  Sequence diagram for deleting a runtime

Updating Nix installation
=========================

.. figure:: figures/updating-nix-sequence.png
  :alt: updating nix sequence diagram

  Sequence diagram for updating Nix installation

Executing code
==============

.. figure:: figures/execute-code-sequence.png
  :alt: code execution sequence diagram

  Sequence diagram for executing code (submissions)

OpenAPI specification
*********************

The following OpenAPI specification describes Envicutor's API as of this writing:

.. openapi:: ./api.yml
  :examples:

.. code-block:: yaml

  openapi: 3.0.0
  info:
    title: Envicutor API
    version: 0.0.1
  paths:
    /health:
      get:
        summary: Health check endpoint
        responses:
          '200':
            description: OK
            content:
              text/plain:
                schema:
                  type: string
                  example: "Up and running"

    /runtimes:
      get:
        summary: List all runtimes
        responses:
          '200':
            description: A list of runtimes
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Runtime'

      post:
        summary: Install a new runtime
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AddRuntimeRequest'
        responses:
          '200':
            description: Installation successful
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/InstallationResponse'
          '400':
            description: Bad request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/BadRequestResponse'
          '500':
            description: Internal Server Error
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ErrorMessage'

    /runtimes/{id}:
      delete:
        summary: Delete a runtime
        parameters:
          - name: id
            in: path
            required: true
            schema:
              type: integer
        responses:
          '200':
            description: Deletion successful
          '400':
            description: Bad request
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ErrorMessage'
          '500':
            description: Internal Server Error
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ErrorMessage'

    /update:
      post:
        summary: Update Nix packages
        responses:
          '200':
            description: Update successful
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/InstallationResponse'
          '500':
            description: Internal Server Error
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/InstallationResponse'

    /execute:
      post:
        summary: Execute code using a specified runtime
        parameters:
          - name: is_project
            in: query
            required: false
            schema:
              type: boolean
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExecutionRequest'
        responses:
          '200':
            description: Execution result
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ExecutionResponse'
          '500':
            description: Internal Server Error
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ErrorMessage'

  components:
    schemas:
      AddRuntimeRequest:
        type: object
        properties:
          name:
            type: string
          nix_shell:
            type: string
          compile_script:
            type: string
          run_script:
            type: string
          source_file_name:
            type: string
        required:
          - name
          - nix_shell
          - compile_script
          - run_script
          - source_file_name

      InstallationResponse:
        type: object
        properties:
          stdout:
            type: string
          stderr:
            type: string

      ExecutionRequest:
        type: object
        properties:
          runtime_id:
            type: integer
          source_code:
            type: string
          input:
            type: string
            nullable: true
          compile_limits:
            allOf:
              - $ref: '#/components/schemas/Limits'
            nullable: true
          run_limits:
            allOf:
              - $ref: '#/components/schemas/Limits'
            nullable: true
        required:
          - runtime_id
          - source_code

      ExecutionResponse:
        type: object
        properties:
          extract:
            allOf:
              - $ref: '#/components/schemas/StageResult'
            nullable: true
          compile:
            allOf:
              - $ref: '#/components/schemas/StageResult'
            nullable: true
          run:
            allOf:
              - $ref: '#/components/schemas/StageResult'
            nullable: true

      Runtime:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string

      Limits:
        type: object
        properties:
          wall_time:
            type: integer
            nullable: true
            description: The maximum amount of wall-time that the submission is allowed to take in seconds
          cpu_time:
            type: integer
            nullable: true
            description: The maximum amount of CPU-time that the submission is allowed to take in seconds
          memory:
            type: integer
            nullable: true
            description: The maximum amount of memory that the submission is allowed to consume in kilobytes
          extra_time:
            type: integer
            nullable: true
            description: 'Check extra-time here: https://www.ucw.cz/moe/isolate.1.html'
          max_open_files:
            type: integer
            nullable: true
            description: The maximum number of file descriptors the submission can open
          max_file_size:
            type: integer
            nullable: true
            description: The maximum size of EACH file created/modified by the submission in kilobytes
          max_number_of_processes:
            type: integer
            nullable: true
            description: The maximum number of processes the submission is allowed to run concurrently

      StageResult:
        type: object
        properties:
          memory:
            type: integer
            nullable: true
          exit_code:
            type: integer
            nullable: true
          exit_signal:
            type: integer
            nullable: true
          exit_message:
            type: string
            nullable: true
          exit_status:
            type: string
            nullable: true
          stdout:
            type: string
          stderr:
            type: string
          cpu_time:
            type: integer
            nullable: true
          wall_time:
            type: integer
            nullable: true

      ErrorMessage:
        type: object
        properties:
          message:
            type: string

      BadRequestResponse:
        type: object
        properties:
          stdout:
            type: string
            nullable: true
          stderr:
            type: string
            nullable: true
