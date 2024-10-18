import os

# Define the path to the reports folder
REPORTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'reports')

def get_report(document_id: str) -> str:
    """
    Retrieves the plagiarism report for a given document ID.

    :param document_id: Identifier of the document.
    :return: Content of the report.
    """
    report_file = os.path.join(REPORTS_PATH, f"{document_id}_report.txt")
    if not os.path.exists(report_file):
        return "Report not available yet."
    with open(report_file, 'r', encoding='utf-8') as f:
        return f.read()
