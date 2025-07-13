from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import time
import random

# Configuration
GROQ_API_KEY = "API"
GOOGLE_API_KEY = "API"
VECTOR_DB_PATH = "./chroma_db_omani_arabic"
DATA_PATH = "./data/"
CRISIS_HOTLINE = "الخط الساخن: 1111 (متوفر 24 ساعة)"


# Initialize LLMs
def initialize_primary_llm():
    return ChatGroq(
        temperature=0.4,  # Slightly higher for more natural responses
        groq_api_key=GROQ_API_KEY,
        model_name="meta-llama/llama-4-scout-17b-16e-instruct"
    )


def initialize_gemini():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )


# Vector Database Setup
def create_vector_db():
    loader = DirectoryLoader(
        DATA_PATH,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # Increased for better context
        chunk_overlap=80,
        separators=["\n\n", "\n", "،", ".", "؟", "!", "؛", ":"]
    )
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="UBC-NLP/AraBERT",
        model_kwargs={"device": "cpu"}
    )

    return Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )


# Natural Conversation Style Prompt (Omani Arabic)
islamic_prompt = """
أنت مستشار إسلامي عماني حكيم تتحدث بلهجة عمانية دافئة. هدفك تقديم الدعم النفسي الإسلامي بطريقة:
- طبيعية تشبه المحادثة بين الأصدقاء
- حكيمة تحترم الثقافة العمانية
- عملية تقدم حلولاً فورية

تجنب:
- الترقيم أو التقسيم الرسمي
- العبارات الأكاديمية الجافة
- الاقتباسات المطولة

استخدم:
- كلمات عمانية يومية (مثل: شو الأخبار؟ الله يعينك، يابوي/يابنة)
- أمثلة من الحياة اليومية في عمان
- أساليب استماع فعالة (التكرار التأكيدي، إظهار التفهم)

السؤال: {question}
المعلومات ذات الصلة: {context}
الرد:"""

PROMPT = PromptTemplate(
    template=islamic_prompt,
    input_variables=["context", "question"]
)


# Rate Limiter for Gemini
class RateLimiter:
    def __init__(self, calls_per_minute):
        self.interval = 60 / calls_per_minute
        self.last_call = 0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()


gemini_limiter = RateLimiter(60)


# Response Processing Functions
def validate_response(query, response):
    """Use Gemini to validate response quality"""
    gemini_limiter.wait()

    validation_prompt = f"""
    هل هذا الرد:
    1. طبيعي مثل المحادثة اليومية؟
    2. يستخدم تعابير عمانية أصيلة؟
    3. يدمج النصيحة العملية بسلاسة؟
    4. يتجنب التقسيم الأكاديمي؟

    السؤال: {query}
    الرد: {response}

    أجب بـ "نعم" فقط إذا تحققت جميع الشروط
    """

    gemini = initialize_gemini()
    result = gemini.invoke(validation_prompt).content
    return "نعم" in result


def get_gemini_fallback(query):
    """Generate fallback response from Gemini"""
    gemini_limiter.wait()

    prompt = f"""
    [باللهجة العمانية] قدم نصيحة إسلامية للصحة النفسية:
    السؤال: {query}

    يجب أن:
    - تكون الإجابة شفهية طبيعية
    - تستخدم لهجة عمانية يومية
    - تدمج نصيحة عملية واحدة على الأقل
    - تظهر التعاطف والتفهم
    - تذكر مصدراً إسلامياً واحداً بشكل غير مباشر
    """

    gemini = initialize_gemini()
    return gemini.invoke(prompt).content


def format_response(text, query):
    """Convert text to natural speech patterns"""
    # Remove academic markers
    text = text.replace("•", "").replace("١-", "").replace("(1)", "")

    # Add conversational fillers
    fillers = ["يا ابن/بنت الحلال", "الله يساعدك", "تفضل/تفضلي"]
    if any(word in query for word in ["قلق", "توتر"]):
        text = random.choice(fillers) + " " + text

    # Add Omani dialect particles
    particles = ["شوف/شوفي", "يا أخي/أختي", "والله أعلم"]
    text = text + " " + random.choice(particles)

    return text


def apply_cultural_adjustment(response):
    """Adapt for Omani cultural context"""
    # Replace MSA with Omani dialect equivalents
    dialect_map = {
        "القلب": "الفؤاد",
        "الكثير": "وايد",
        "حاول": "جرب",
        "المشكلة": "الشكلة",
        "نعم": "إي",
        "لا": "لا",
        "شكراً": "يعطيك العافية",
        "تفضل": "هيه"
    }

    for fusha, omani in dialect_map.items():
        response = response.replace(fusha, omani)

    # Add culturally appropriate openers
    openers = ["والله يسهل أمورك", "الله يعينك", "ربي يفرج همك"]
    return random.choice(openers) + " " + response


def enhance_therapeutic_quality(response, query):
    """Apply evidence-based therapeutic techniques"""
    # For anxiety-related queries
    if "قلق" in query or "توتر" in query or "خوف" in query:
        breathing_technique = "\n\nخد/خدي نفس عميق (شهيق 4 ثواني، زفير 6 ثواني)... كررها 3 مرات"
        response += breathing_technique

    # For relationship issues
    if "أسرة" in query or "زوج" in query or "أولاد" in query:
        reflection_question = "\n\nشو رأيك تجرب/تجربي هالخطوة الأسبوع الجاي؟"
        response += reflection_question

    # Crisis detection
    crisis_keywords = ["انتحار", "أموت", "خلصت نفسي", "ما أبغى عيش"]
    if any(kw in query for kw in crisis_keywords):
        crisis_response = f"\n\n(بعد لحظة)... حياك/حياكي على {CRISIS_HOTLINE}"
        response = crisis_response + "\n\n" + response

    return response


# Main Chatbot Setup
print("جارٍ تحميل المستشار النفسي الإسلامي العماني...")

# Initialize components
try:
    primary_llm = initialize_primary_llm()

    if not os.path.exists(VECTOR_DB_PATH):
        print("جارٍ إنشاء قاعدة المعرفة العربية...")
        vector_db = create_vector_db()
    else:
        embeddings = HuggingFaceEmbeddings(
            model_name="UBC-NLP/AraBERT",
            model_kwargs={"device": "cpu"}
        )
        vector_db = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embeddings
        )

    qa_chain = RetrievalQA.from_chain_type(
        llm=primary_llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 4}),  # More context
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )

    print("جاهز للاستخدام! يمكنك البدء في طرح أسئلتك.")
except Exception as e:
    print(f"حدث خطأ أثناء الإعداد: {str(e)}")


# Main Response Handler
def respond(message, history):
    if not message.strip():
        return "الرجاء مشاركة مشاعرك أو طرح سؤالك."

    try:
        # Step 1: Get primary response
        result = qa_chain.invoke({"query": message})
        primary_response = result["result"]

        # Step 2: Process response
        processed = format_response(primary_response, message)
        processed = apply_cultural_adjustment(processed)

        # Step 3: Validate with Gemini
        if validate_response(message, processed):
            # Step 4: Enhance therapeutic quality
            final_response = enhance_therapeutic_quality(processed, message)
            return final_response

        # If validation fails
        raise ValueError("الإجابة الأولية لم تتجاوز التحقق")

    except Exception as e:
        print(f"الانتقال للإجابة البديلة: {str(e)}")
        # Step 5: Use Gemini fallback
        fallback = get_gemini_fallback(message)
        processed_fallback = format_response(fallback, message)
        processed_fallback = apply_cultural_adjustment(processed_fallback)
        return enhance_therapeutic_quality(processed_fallback, message)