import fitz 
from PIL import Image
import io
import pytesseract  # Import pytesseract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

pdf_path = r"C:\Users\salom\Downloads\tasks\task1 charts.pdf"  
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

def extract_text_from_pdf(pdf_path):
    text_chunks = []
    try:
        with fitz.open(pdf_path) as doc:
            for page_number in range(len(doc)):
                page = doc[page_number]
                text = page.get_text()
            
                if not text:
                    for img_index in range(len(page.get_images(full=True))):
                        xref = page.get_images(full=True)[img_index][0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image = Image.open(io.BytesIO(image_bytes))
                        text += pytesseract.image_to_string(image)
                
                fields = text.split('\n') 
                for field in fields:
                    cleaned_field = field.replace('\n', ' ').strip() 
                    if cleaned_field:  
                        text_chunks.append((page_number + 1, cleaned_field))  
        return text_chunks
    except Exception as e:
        return f"Error: {e}"

def get_text_from_page(text_chunks, page_number):
    return [text for page_num, text in text_chunks if page_num == page_number]

def handle_query(text_chunks, query):
    texts = [text for _, text in text_chunks]

    vectorizer = TfidfVectorizer().fit_transform(texts + [query])
    vectors = vectorizer.toarray()
    
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1])

    most_similar_index = cosine_similarities.argsort()[0][-1]
    return texts[most_similar_index]

print("PDF Text Extraction Tool")
print("Enter a page number (in digits) to extract text, type 'query' to ask a question, or 'quit' to exit.")

text_chunks = extract_text_from_pdf(pdf_path)

while True:
    user_input = input("Enter page number or query: ").strip()
    
    if user_input.lower() == 'quit':
        print("Exiting the program.")
        break
    
    if user_input.lower() == 'query':
        query = input("Enter your question: ").strip()
        response = handle_query(text_chunks, query)
        print(f"\nResponse:\n{response}\n")
        continue
    
    try:
        page_number = int(user_input)
        if page_number < 1 or page_number > len(set(page for page, _ in text_chunks)):
            print(f"Please enter a valid page number between 1 and {len(set(page for page, _ in text_chunks))}.")
            continue
        
        extracted_text = get_text_from_page(text_chunks, page_number)
        
        formatted_text = "\n".join(extracted_text) 
        print(f"\nText from Page {page_number}:\n{formatted_text}\n")
    except ValueError:
        print("Please enter a valid integer for the page number.")
