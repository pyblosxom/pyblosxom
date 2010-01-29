==========
 Glossary
==========

.. glossary::
   :sorted:

   flavour
      A flavour is a group of templates for a specifc output like
      html, xhtml, xml, atom, rss, etc.

      A flavour consists of at least the following templates:

      * **content_type** - holds the content type of the flavour
      * **head** - holds everything before all the entries
      * **story** - holds a single entry
      * **foot** - holds everything after all the entries
      * **date_head** - shows at the start of a date
      * **date_foot** - shows at the end of a date

      See :ref:`Flavours and Templates <flavours-and-templates>` for
      more details.

   template
      A template specifies a specific portion of the output.

      For example, here's a **head** template for an html flavour::

         <html>
         <head>
           <title>My blog</title>
         </head>
         <body>

      See :ref:`Flavours and Templates <flavours-and-templates>` for
      more details.
