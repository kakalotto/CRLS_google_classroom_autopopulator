
import googleapiclient

from generate_sheets_credential import generate_sheets_credential
from generate_classroom_credential import generate_classroom_credential
from generate_docs_credential import generate_docs_credential

import json

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if text_run:
        text_run.get('content')
        return text_run.get('content')
    else:
        inline_object = element.get('inlineObjectElement')
        if inline_object:
            return 'INLINE OBJECT '
        else:
            return ''


def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text


def main():
    DOCUMENT_ID = '1LaXkQuhYxfh0kMjMKjYzJNO1_KqWFEywpZyGsGnAnSQ'
    service_docs = generate_docs_credential()

    doc = service_docs.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    print(read_strucutural_elements(doc_content))

    print(json.dumps(doc, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()