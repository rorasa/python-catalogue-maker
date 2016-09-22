# Python-catalogue-maker

This is a utility function to create physical (printed) catalog pages for display automatically from the predefined template and stylesheet.
It is mainly used to create corresponding catalogue pages that correspond to the contents of https://collections.wattanit.info , and thus its earliest version is built for this specific workflow.

The future version is planned to support a generic input templating, allowing for flexible templates with various input requests.

## Dependencies

Python-catalogue-maker uses [WeasyPrints](http://weasyprint.org/) to render the html template into a pdf output.

To install WeasyPrint, follow the instructions on http://weasyprint.readthedocs.io/en/latest/install.html .

## Templates

There are two components of the template:
* `template.html` stores the document structure and contents,
* `template.css` stores the style of the document.

Web page of any length can be rendered into pdf file using Python-catalogue-maker. 
Inside of the `template.html` also contains the template markups (like `{{title}}`). 
Python-catalogue-maker will ask the user what the value of each markup should be and substitute it in accordingly.

The style of the document can be customised using `template.css`. 
The infomation on how to customise a page using CSS can be fould easily on the internet. 
It is advise to specify most units in the stylesheet using a physical unit like `cm`—which is more suitable for paper—rather than screen-based units such as `px` or `%`.
