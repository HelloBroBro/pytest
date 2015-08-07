Changing standard (Python) test discovery
===============================================

Changing directory recursion
-----------------------------------------------------

You can set the :confval:`norecursedirs` option in an ini-file, for example your ``setup.cfg`` in the project root directory::

    # content of setup.cfg
    [pytest]
    norecursedirs = .svn _build tmp*

This would tell ``pytest`` to not recurse into typical subversion or sphinx-build directories or into any ``tmp`` prefixed directory.

.. _`change naming conventions`:

Changing naming conventions
-----------------------------------------------------

You can configure different naming conventions by setting
the :confval:`python_files`, :confval:`python_classes` and
:confval:`python_functions` configuration options.  Example::

    # content of setup.cfg
    # can also be defined in in tox.ini or pytest.ini file
    [pytest]
    python_files=check_*.py
    python_classes=Check
    python_functions=*_check

This would make ``pytest`` look for tests in files that match the ``check_*
.py`` glob-pattern, ``Check`` prefixes in classes, and functions and methods
that match ``*_check``.  For example, if we have::

    # content of check_myapp.py
    class CheckMyApp:
        def simple_check(self):
            pass
        def complex_check(self):
            pass

then the test collection looks like this::

    $ py.test --collect-only
    ======= test session starts ========
    platform linux2 -- Python 2.7.9, pytest-2.8.0.dev4, py-1.4.28, pluggy-0.3.0
    rootdir: $REGENDOC_TMPDIR, inifile: setup.cfg
    collected 2 items
    <Module 'check_myapp.py'>
      <Class 'CheckMyApp'>
        <Instance '()'>
          <Function 'simple_check'>
          <Function 'complex_check'>
    
    =======  in 0.12 seconds ========

.. note::

   the ``python_functions`` and ``python_classes`` options has no effect
   for ``unittest.TestCase`` test discovery because pytest delegates
   detection of test case methods to unittest code.

Interpreting cmdline arguments as Python packages
-----------------------------------------------------

You can use the ``--pyargs`` option to make ``pytest`` try
interpreting arguments as python package names, deriving
their file system path and then running the test. For
example if you have unittest2 installed you can type::

    py.test --pyargs unittest2.test.test_skipping -q

which would run the respective test module.  Like with
other options, through an ini-file and the :confval:`addopts` option you
can make this change more permanently::

    # content of pytest.ini
    [pytest]
    addopts = --pyargs

Now a simple invocation of ``py.test NAME`` will check
if NAME exists as an importable package/module and otherwise
treat it as a filesystem path.

Finding out what is collected
-----------------------------------------------

You can always peek at the collection tree without running tests like this::

    . $ py.test --collect-only pythoncollection.py
    ======= test session starts ========
    platform linux2 -- Python 2.7.9, pytest-2.8.0.dev4, py-1.4.28, pluggy-0.3.0
    rootdir: $PWD/doc/en, inifile: pytest.ini
    collected 3 items
    <Module 'example/pythoncollection.py'>
      <Function 'test_function'>
      <Class 'TestClass'>
        <Instance '()'>
          <Function 'test_method'>
          <Function 'test_anothermethod'>
    
    =======  in 0.12 seconds ========

customizing test collection to find all .py files
---------------------------------------------------------

.. regendoc:wipe

You can easily instruct ``pytest`` to discover tests from every python file::


    # content of pytest.ini
    [pytest]
    python_files = *.py

However, many projects will have a ``setup.py`` which they don't want to be imported. Moreover, there may files only importable by a specific python version.
For such cases you can dynamically define files to be ignored by listing
them in a ``conftest.py`` file::

    # content of conftest.py
    import sys

    collect_ignore = ["setup.py"]
    if sys.version_info[0] > 2:
        collect_ignore.append("pkg/module_py2.py")

And then if you have a module file like this::

    # content of pkg/module_py2.py
    def test_only_on_python2():
        try:
            assert 0
        except Exception, e:
            pass

and a setup.py dummy file like this::

    # content of setup.py
    0/0  # will raise exeption if imported

then a pytest run on python2 will find the one test when run with a python2
interpreters and will leave out the setup.py file::

    $ py.test --collect-only
    ======= test session starts ========
    platform linux2 -- Python 2.7.9, pytest-2.8.0.dev4, py-1.4.28, pluggy-0.3.0
    rootdir: $REGENDOC_TMPDIR, inifile: pytest.ini
    collected 1 items
    <Module 'pkg/module_py2.py'>
      <Function 'test_only_on_python2'>
    
    =======  in 0.12 seconds ========

If you run with a Python3 interpreter the moduled added through the conftest.py file will not be considered for test collection.
