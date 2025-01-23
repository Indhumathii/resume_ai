import traceback
from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import JSONResponse
from generic import save_uploaded_file, load_document, process_text, run_chain, retrieve_relevant_chunks, process_resume
from constant import Technical_prompt, Stack_prompt, Experience_level_prompt, Prompt_template

app=FastAPI()

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), query:str=None):
    """Handles file upload and processes the resume."""
    try:
        # Step 1: Save the uploaded file
        uploaded_path, file_extension = save_uploaded_file(file)
        # Step 2: Load the document content
        data = load_document(file_path=uploaded_path, file_extension=file_extension)
        # Step 3: Process the text into chunks and embeddings
        all_splits, docsearch, content_list = process_text(data)
        if query:
            context = retrieve_relevant_chunks(query, docsearch)
            answer = run_chain(context,Prompt_template, query)
        return {
            "message": "File uploaded and processed successfully.",
            "chunks_count": len(all_splits),
            "final_response": answer
        }
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': 'Something went wrong, Try again later'},
        )
    

@app.post("/extract-skills/")
async def extract_skills(file: UploadFile = File(...)):
    """Extracts technical and soft skills from the resume."""
    try:
        result = process_resume(file, Technical_prompt)
        return {"skills": result}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"An error occurred: {str(e)}"},
        )
    

@app.post("/identify-stack/")
async def identify_stack(file: UploadFile = File(...)):
    """Identifies the technology stack from the resume."""
    try:
        result = process_resume(file, Stack_prompt)
        return {"technology_stack": result}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    

@app.post("/analyze-experience/")
async def analyze_experience(file: UploadFile = File(...)):
    """Analyzes the experience level for skills listed in the resume."""
    try:
        result = process_resume(file, Experience_level_prompt)
        return {"experience_analysis": result}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    


