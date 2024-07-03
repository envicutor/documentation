# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Envicutor Project Documentation'
copyright = '2023, Ahmed Wael, Adham Hazem, Omar Brikaa, Mostafa Ahmed, Ali Esmat'
author = 'Ahmed Wael, Adham Hazem, Omar Brikaa, Mostafa Ahmed, Ali Esmat'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinxcontrib.bibtex', 'sphinxcontrib.openapi']
todo_include_todos = True
bibtex_bibfiles = ['refs.bib']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

latex_elements = {
  'maxlistdepth': '99',
  'figure_align': 'H',
  'preamble': r"""
%% --------------------------------------------------
%% |:sec:| add list of figures
%% --------------------------------------------------
\makeatletter
\renewcommand{\sphinxtableofcontents}{%
  %
  % before resetting page counter, let's do the right thing.
  \if@openright\cleardoublepage\else\clearpage\fi
  \pagenumbering{roman}%
  \begingroup
    \parskip \z@skip
    \tableofcontents
  \endgroup
  %
  %% addtional lists
  \if@openright\cleardoublepage\else\clearpage\fi
  \addcontentsline{toc}{chapter}{List of Figures}%
  \listoffigures
  %
  \if@openright\cleardoublepage\else\clearpage\fi
  \pagenumbering{arabic}%
}
\makeatother
\let\cleardoublepage=\clearpage
""",
  'maketitle': r"""
\begin{titlepage}
  \begin{center}
    \includegraphics[width=0.2\textwidth]{../../cu.png}\\
    \large
    Cairo University\\
    Faculty of Computers and Artificial Intelligence\\
    Software Engineering\\
    \vspace{1cm}
    \Huge
    Envicutor\\
    \vspace{1cm}
    \large
    Supervised by\\
    \Large
    Dr. Cherry Ahmed\\
    \vspace{1cm}
    \large
    Implemented by\\
    \Large
    Ahmed Wael Nagy Wanas (20206008)\\
    \Large
    Adham Hazem Fahmy Shafei (20206011)\\
    \Large
    Omar Adel Abdel Hamid Ahmed Brikaa (20206043)\\
    \Large
    Mostafa Ahmed Mohammed Ahmed Ibrahim (20206073)\\
    \Large
    Ali Esmat Ahmed Orfy (20206123)\\
    \vfill
    \large
    Graduation Project\\
    \large
    Academic year 2023 - 2024\\
    \large
    Project Documentation\\

  \end{center}
\end{titlepage}"""
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

rst_epilog = """
.. include:: /include/links.rstinc
"""
numfig = True
