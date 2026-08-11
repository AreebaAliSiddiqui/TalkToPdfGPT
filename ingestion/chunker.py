from langchain_text_splitters import RecursiveCharacterTextSplitter  



def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size= 2500,
    chunk_overlap= 300,
    length_function= len,
)
    return text_splitter.split_text(text)



