wagtail2docx
================================================================================
wagtail plugin to convert page to Microsoft Word docx document

warning
  This plugin is under development

Installation
--------------------------------------------------------------------------------

- add git+https://github.com/olopost/wagtail2docx.gi to your ``requirements.txt`` file of your wagtail project

- add wagtail2docx in your settings file

  .. code-block:: python

   INSTALLED_APPS = [
    'wagtail2docx',

- after deployment launch ``python manage.py`` and after launch the following command:

  * ``makemigrations``
  * ``migrate``

Overview
--------------------------------------------------------------------------------

+------------------------------------------+------------------------------------+
| Example of original html page in wagtail | .. image::  media/original_html.png|
+------------------------------------------+------------------------------------+
| The same generated in doc                | .. image::  media/word_page.png    |
+------------------------------------------+------------------------------------+
| Create a word document                   | .. image::  media/settings.png     |
+------------------------------------------+------------------------------------+

