from keybert import KeyBERT
import xml.etree.ElementTree as ET


def extract_keywords(text, num_keywords=5):
    model = KeyBERT("all-mpnet-base-v2")
    candidate_keywords = model.extract_keywords(
        text, 
        keyphrase_ngram_range=(1, 2), 
        stop_words='english', 
        top_n=20, 
        use_mmr=True, 
        diversity=0.7
    )
    domain_terms = ["passport", "application", "visa", "document", "photo", "renewal"]
    domain_keywords = [(kw, score) for kw, score in candidate_keywords if any(term in kw.lower() for term in domain_terms)]
    other_keywords = [(kw, score) for kw, score in candidate_keywords if not any(term in kw.lower() for term in domain_terms)]
    sorted_keywords = [kw for kw, score in domain_keywords] + [kw for kw, score in other_keywords]
    return sorted_keywords

def extract_text_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    text_content = " ".join(elem.text for elem in root.iter() if elem.text)
    return text_content

def extract_text_from_file(file_path):
    text = textract.process(file_path).decode("utf-8")
    return text
