import os
import shutil
from fastapi import UploadFile,HTTPException,status
from langchain_community import document_loaders
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from constant import allowed_extensions, UPLOAD_DIR


os.makedirs(UPLOAD_DIR, exist_ok=True)
os.environ['OPENAI_API_KEY']=""

def validate_api_key():
    """Validate that the OpenAI API key is set."""
    if not os.environ['OPENAI_API_KEY']:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

def save_uploaded_file(file: UploadFile) -> tuple:
    """Saves the uploaded file to the uploads directory and returns its path and extension."""
    _, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Only .txt and .pdf files are supported."
        )
    uploaded_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(uploaded_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return uploaded_path, file_extension

def load_document(file_path: str, file_extension: str):
    """Loads the content of a document based on its file extension."""
    if file_extension == ".txt":
        loader = document_loaders.TextLoader(file_path=file_path)
    elif file_extension == ".pdf":
        loader = document_loaders.PyPDFLoader(file_path=file_path)
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Unsupported file type. Please upload a TXT or PDF file."
        )
    return loader.load()

def process_text(data):
    """Splits the document content into chunks and creates embeddings."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    all_splits = text_splitter.split_documents(data)
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_documents(data, embeddings)
    content_list = [split.page_content for split in all_splits]
    
    return all_splits, docsearch, content_list

def retrieve_relevant_chunks(query: str, docsearch: FAISS, top_k=3):
    """Retrieve the most relevant chunks from the vector database."""
    query_embedding = OpenAIEmbeddings().embed_query(query)
    results = docsearch.similarity_search_by_vector(query_embedding, top_k)
    context = "\n".join([result.page_content for result in results])
    return context

def run_chain(context, prompt_template, query=None):
    """Executes an LLM chain using the provided context and prompt template."""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    # Determine input variables based on whether query is provided
    if query is not None:
        input_variables = ["context", "question"]
        inputs = {"context": context, "question": query}
    else:
        input_variables = ["context"]
        inputs = {"context": context}
    # Create the PromptTemplate
    prompt = PromptTemplate(input_variables=input_variables, template=prompt_template)
    # Create and execute the chain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    return chain.run(inputs)

def process_resume(file: UploadFile, prompt: str) -> dict:
    """Process the resume by uploading the file, extracting content, and running the given prompt."""
    # Save uploaded file and extract its content
    uploaded_path, file_extension = save_uploaded_file(file)
    data = load_document(file_path=uploaded_path, file_extension=file_extension)
    context = "\n".join([doc.page_content for doc in data])

    # Run the chain with the provided prompt
    result = run_chain(context, prompt)
    if isinstance(result, str):
        result = result.replace("\n", "").replace(" \ ", "").strip()
    return result
    
