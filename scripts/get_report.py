import requests

API_URL = "http://localhost:8000/report/"

def get_report(document_id: str):
    """
    Retrieves the plagiarism report for a given document ID.

    :param document_id: Identifier of the document.
    :return: Plagiarism report content.
    """
    response = requests.get(f"{API_URL}{document_id}")
    return response.text

def main():
    document_id = input("Enter the document ID to retrieve the report: ")
    report = get_report(document_id)
    print("Plagiarism Report:\n")
    print(report)

if __name__ == "__main__":
    main()
