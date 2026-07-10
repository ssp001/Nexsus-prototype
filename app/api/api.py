from fastapi import FastAPI, File, UploadFile, HTTPException
from ..bucket import DocumentStorageManager
from config import UserClass
from ..document_processing import DocumentProcessing
from utils import RequestFaildRespones
import logfire

app = FastAPI()
storage_servce = DocumentStorageManager()
pageindex_client_service = DocumentProcessing()
logger = logfire.configure(service_name=__name__)


@app.get("/")
def home():
    return {"server is ready to serve"}


@app.post("/pdf_post")
def pdf_post(document: UploadFile = File()):
    try:
        # Document upload process logic
        with logger.span("upload peocees has been started in endpoint"):
            size = document.file.seek(0, 2)
            size = document.file.tell()
            document.file.seek(0)
            storage_servce.post_document(
                document_data=document.file, document_length=size, document_name=document.filename)
            logger.info("document has been uploaded successfully")
            # Document Download process logic
            logger.info("downloading the object from the storage")
            storage_servce.get_document(
                document_name=document.filename, document_length=size)
            # Document Download process logic
            logger.info("document processign has started")
            document_id = pageindex_client_service.process_the_document(
                document_path=f"tmp/{document.filename}.pdf")
            logger.info("all processing has done succefully")
            print(document_id)
            return {
                "message": "Document processed successfully please ask fr questions",
                "doc_id": document_id
            }
    except HTTPException as error:
        logger.exception("buccket stroing opration timout", error)
        raise RequestFaildRespones(
            "can't upload object.uncsucesfull operation please try again later")


@app.post("/retriver_get")
async def retrive_documet(parameter: UserClass):
    try:
        logger.info("retriver process has been started ")
        respones = await pageindex_client_service.retrive_answer(
            doc_id=parameter.doc_id, query=parameter.query)
        logger.info("documentr retrive complete")
        return {"message": respones}
    except TimeoutError as error:
        logger.exception("retriver opration timout", error)
        raise HTTPException(
            status_code=408,
            detail="can't retrive document. uncsucesfull operation please try again later"
        )
