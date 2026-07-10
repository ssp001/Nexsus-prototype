from pageindex import PageIndexClient, PageIndexAPIError
from config import settings
import polling2
import logfire


class DocumentProcessing:
    def __init__(self):
        self.client = PageIndexClient(api_key=settings.pageindex_api_key)
        self.logging = logfire.configure(service_name=__name__)

    def process_the_document(self, document_path: str) -> None:
        """
        Process the document using PageIndexClient.

        Args:
            document_path (str): The path to the document to be processed.

        Returns:
            None
        """
        try:
            # Assuming there's a method in PageIndexClient to process documents
            pageindex_result = self.client.submit_document(
                file_path=document_path)
            document_id = pageindex_result.get("doc_id")
            # try to pool the the process status form the pageindex api
            polling2.poll(
                target=lambda: self.client.get_document(document_id)["status"],
                step=5,
                timeout=20,
                check_success=lambda status: status == "completed"
            )
            self.logging.info(
                f"Successfully processed document: {document_path}")
            return document_id
        except Exception as e:
            self.logging.error(
                f"Error processing document {document_path}: {e}")
            raise PageIndexAPIError("pageindex api error:", e)

    async def retrive_answer(self, doc_id, query: str):
        """
        Retrieve an answer from the processed document using PageIndexClient.

        Args:
            query (str): The query to retrieve the answer for.
        returns:
            str
        """
        try:
            self.logging.info("retriver component has started")
            response = self.client.chat_completions(
                messages=[{"role": "user", "content": query}],
                doc_id=doc_id,
                stream=False,
            )
            if isinstance(response, dict):
                choices = response.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    if isinstance(message, dict):
                        content = message.get("content")
                        if isinstance(content, str):
                            return content
            return str(response)
        except Exception as error:
            self.logging.error(
                f"Error retrieving answer for query '{query}': {error}"
            )
            raise PageIndexAPIError("errro in retriving data") from error
