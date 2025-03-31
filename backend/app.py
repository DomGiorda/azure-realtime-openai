import logging
import os
from pathlib import Path

from aiohttp import web
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

from ragtools import attach_rag_tools
from rtmt import RTMiddleTier

# Import for Swagger
from aiohttp_swagger3 import SwaggerDocs, swagger_doc, SwaggerUiSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voicerag")


async def create_app():
    if not os.environ.get("RUNNING_IN_PRODUCTION"):
        logger.info("Running in development mode, loading from .env file")
        load_dotenv()

    tenant_id = os.environ.get("AZURE_TENANT_ID")
    client_id = os.environ.get("AZURE_CLIENT_ID")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        raise ValueError("Don't exists App Registration credentials.")

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    app = web.Application()

    rtmt = RTMiddleTier(
        credentials=credential,
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment=os.environ["AZURE_OPENAI_REALTIME_DEPLOYMENT"],
        voice_choice=os.environ.get("AZURE_OPENAI_REALTIME_VOICE_CHOICE") or "alloy",
        api_version=os.environ.get("OPENAI_API_VERSION")
        )
    rtmt.system_message = """
        You are a helpful assistant. Only answer questions based on information you searched in the knowledge base, accessible with the 'search' tool.
        The user is listening to answers with audio, so it's *super* important that answers are as short as possible, a single sentence if at all possible.
        Never read file names or source names or keys out loud.
        Always use the following step-by-step instructions to respond:
        1. Always use the 'search' tool to check the knowledge base before answering a question.
        2. Always use the 'report_grounding' tool to report the source of information from the knowledge base.
        3. Produce an answer that's as short as possible. If the answer isn't in the knowledge base, say you don't know.
    """.strip()

    attach_rag_tools(rtmt,
        credentials=credential,
        search_endpoint=os.environ.get("AZURE_SEARCH_ENDPOINT"),
        search_index=os.environ.get("AZURE_SEARCH_INDEX"),
        semantic_configuration=os.environ.get("AZURE_SEARCH_SEMANTIC_CONFIGURATION") or None,
        identifier_field=os.environ.get("AZURE_SEARCH_IDENTIFIER_FIELD") or "chunk_id",
        content_field=os.environ.get("AZURE_SEARCH_CONTENT_FIELD") or "chunk",
        embedding_field=os.environ.get("AZURE_SEARCH_EMBEDDING_FIELD") or "text_vector",
        title_field=os.environ.get("AZURE_SEARCH_TITLE_FIELD") or "title",
        use_vector_query=(os.getenv("AZURE_SEARCH_USE_VECTOR_QUERY", "true") == "true")
        )

    rtmt.attach_to_app(app, "/openai/realtime")

    # --- Remove static file serving ---
    # current_directory = Path(__file__).parent
    # app.add_routes([web.get('/', lambda _: web.FileResponse(current_directory / 'static/index.html'))])
    # app.router.add_static('/', path=current_directory / 'static', name='static')

    # --- Add Swagger documentation ---
    ui_settings = SwaggerUiSettings(path="/api/ui")
    SwaggerDocs(app, title="VoiceRAG API", swagger_ui_settings=ui_settings)
    #app.add_routes([web.get('/api/docs', swagger_doc)]) # This should serve the JSON spec

    return app

if __name__ == "__main__":
    host = "localhost"
    port = 8765
    web.run_app(create_app(), host=host, port=port)