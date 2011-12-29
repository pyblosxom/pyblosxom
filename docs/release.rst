=================
 Release process
=================

1. Update the release process

2. Update WHATSNEW

3. Update the version number and date in:

   * Pyblosxom/_version.py
   * docs/conf.py

4. Update AUTHORS::

       git log --pretty=format:%an | sort -u

5. Commit the changes

6. Tag the commit::

       git tag -a vx.y

   e.g. ``v1.5``

7. Run::

       ./maketarball.sh TAG

8. Push everything to ``pyblosxom`` and ``pyblosxom-web`` repositories::

       git push --tags origin master

9. Build the docs::

       cd docs/
       make html

10. Write release blog entry

11. Push docs, tarball and blog entry to website.

12. Update PYPI::

        python setup.py push

13. Send email to pyblosxom-users and pyblosxom-devel.

14. Update version numbers to next version + ``.dev``.
