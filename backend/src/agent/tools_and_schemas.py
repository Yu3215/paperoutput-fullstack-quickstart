from typing import List
from pydantic import BaseModel, Field


class SearchQueryList(BaseModel):
    query: List[str] = Field(
        description="A list of search queries to be used for web research."
    )
    rationale: str = Field(
        description="A brief explanation of why these queries are relevant to the research topic."
    )


class Reflection(BaseModel):
    is_sufficient: bool = Field(
        description="Whether the provided summaries are sufficient to answer the user's question."
    )
    knowledge_gap: str = Field(
        description="A description of what information is missing or needs clarification."
    )
    follow_up_queries: List[str] = Field(
        description="A list of follow-up queries to address the knowledge gap."
    )


# 新增论文Framework相关模式
class FrameworkSection(BaseModel):
    section_name: str = Field(description="Name of the framework section")
    content: str = Field(description="Content of the framework section")
    key_points: List[str] = Field(description="Key points covered in this section")


class FrameworkOutput(BaseModel):
    framework_content: str = Field(description="Complete framework content")
    sections: List[FrameworkSection] = Field(description="Breakdown of framework sections")
    methodology_alignment: str = Field(description="How the framework aligns with the methodology")
    journal_compliance: str = Field(description="Compliance with journal requirements")


def get_journal_examples(journal_name: str) -> str:
    """获取期刊的few-shot示例"""
    journal_examples = {
        "ACM Low-Resource Language ": """
        示例：
        '3 Model
The overall architecture of the model is shown in Figure 1. We utilize triples as additional knowledge inputs and apply the question type classifier proposed by Sun et al. [31] to predict the question type. After question type prediction and key sentence identifying, the prediction, the knowledge triple, and the paragraph containing key sentence identification will be integrated into a question generator to guide question generation. Our question generator is based on a two-layer Transformer architecture.
3.1 Key Sentence Embedding
We define the sentence containing an answer as the key sentence, which provides key information for question generation. Integrating key sentence embedding enables our model to differentiate the key sentence from other sentences, then the model will pay more attention to the key sentence. This method aims to strengthen local attention and adjust the attention weights by incorporating key sentence embeddings. We employ the following three identification methods, respectively, and example of a specific identification is shown in Figure 2:
—Exact key: To obtain surrounding information for answers and avoid interference caused by duplicate identification, we locate the exact position of the answer in the context and identify the sentence as the key sentence.
—All key: To obtain more key information related to an answer, we identify all sentences where the answer appears as the key sentence.
—Pre key: To obtain key information that is distant from the answer, we identify the sentence containing the answer and the preceding sentence as the key sentence.
3.2 Distance Information Obtained from the Knowledge Graph
3.2.1 Construction of the Knowledge Graph.
Introducing structured knowledge into the input of a model can significantly enhance its capabilities in text analysis and comprehension. However, the Tibetan knowledge graph is currently sparse, characterized by limited data and a lack of rich content. To address this challenge, we propose to expand and enrich the Tibetan knowledge graph by leveraging co-reference relationships among entities within Tibetan triples, and by utilizing extensive knowledge bases and non-textual media resources available in other languages. This strategy not only broadens the coverage and deepens the content of the knowledge graph but also provides a robust data foundation for future research on Tibetan text processing and its applications.
We collected numerous original articles from Tibetan websites such as China Tibetan Online, categorizing them into fields like general knowledge, tourism, law, and geography. Following the analysis of Tibetan sentence structures by Gao and Zaxi [8], suitable sentences were selected for triple extraction. Part-of-speech tagging was employed to break these sentences down into components such as subjects, predicates, and objects, leading to the creation of more than 300,000 basic triples. Considering the sparse nature of the existing Tibetan knowledge base, this research has enriched it by leveraging external knowledge bases and non-textual resources. For example, by utilizing the entity-attribute-value triple of “Kado Sangden Eagle Mountain” in Baidu Baike and Wikipedia, such as <Kado Sangden Eagle Mountain, Construction Date, 1706>, and integrating our comprehensive Chinese-Tibetan dictionary with 180,000 entries and a Tibetan-Chinese named entity database comprising 15,387 items, we have significantly enhanced the relationships and attributes of Tibetan entities, effectively addressing the issues of low data volume and sparsity in the Tibetan knowledge base.
3.2.2 Comparison of English and Tibetan Grammatical Structures.
Tibetan, a low-resource language, features a complex grammatical structure that necessitates an understanding of specific contexts and semantics for accurate interpretation. The syntax comparison of English and Tibetan interrogative sentences is detailed in Table 2. Unlike traditional punctuation, Tibetan uses specific marker characters to denote sentence boundaries; the most common end-of-sentence marker is “,” whereas “” marks the beginning of paragraphs. Compared to high-resource languages like English and Chinese, Tibetan exhibits significant grammatical differences. These include variations in word order, particle usage, and the placement of interrogative words. For example, the standard word order in Tibetan is Subject-Object-Verb (SOV), as in “” (I repair the table). In forming questions, the structure remains unchanged, but an interrogative particle, such as “” (is it?), is added at the end to signify a question, resulting in “” (Did I repair the table?). Furthermore, Tibetan places interrogative words like “” (what), “” (where), and “” (how much) typically at or near the end of sentences, contrasting with the English practice of beginning questions with such words. Here we briefly introduce the Tibetan vocabulary. Tibetan vocabulary is categorized into substantive and function words. Substantive words, including nouns, adjectives, and verbs, serve as the main components of sentences and carry specific meanings. In contrast, function words, such as case particles and conjunctions, do not hold meanings independently but help connect substantive words to articulate complete ideas. These function words are further classified into discourse particles and negative particles, with negative particles requiring variant forms based on suffix letters. Examples include ergative and genitive particles. The process of automatically generating Tibetan questions involves two main steps. First, based on the given answers, the system identifies the necessary interrogative pronouns and substantive words. For the question “What books did Dunzhu Tsering write?,” the system first identifies the interrogative pronoun “” (what) and the substantive words “” (write) and “” (book). Then, it selects appropriate function words “” and “” to construct the question effectively, ensuring semantic coherence and grammatical accuracy.
We design a question generation algorithm based on knowledge triples according to the preceding method. For an aligned context containing entity relation and paragraph information, the algorithm is shown in Table 3. The specific question generation template is shown in Figure 3.
In Tibetan, case particles are unique grammatical markers, and there are eight cases. We mainly use the genitive particles and the ergative particles in constructing Tibetan questions. The specific addition rules are shown in Tables 4 and 5. The choice of specific genitive particles or ergative particles mainly depends on the suffix letters.
3.3 Question Generator
Different types of questions have different grammar rules, and choosing an accurate interrogative word according to the type of question is the key to generating high-quality questions. Therefore, we use the question type as an additional input to guide model generation. To obtain a more accurate question type, we divide the datasets according to the objects asked by the question. We use nine categories to express the question patterns, such as “what” to refer to facts, “who” to refer to people, “how” to refer to methods, “when” to refer to time, “which” to refer to choice, “where” to refer to a place, “why” to refer to reason, “whether” to refer to general questions, and “others” to refer to others. Examples of Tibetan questions are shown in Table 6.
To better understand multiple input information and context, our question generator is based on a two-layer Transformer. The input of the question generator consists of three parts:
(1)The question type predicted by the question type classifier.
(2)The paragraph which contains key sentence identification 
(3)	The knowledge triple 
In this work, a special token [SEP] is used to separate paragraphs, [S] is used to identify the start of a key sentence, and [E] is used to identify the end of a key sentence. The overall input sequence X is shown in Equation (1):
The final input embedding 
, where 
 ET is token embedding which contains the passage and answer, 
 ES is segment embedding, 
 EP is position embedding, 
 ETP is question type embedding, 
 EKY is key sentence embedding, and 
 EKN is knowledge embedding.
The encoder of the model consists of two identical encoding layers, with each layer consisting of multi-head self-attention and a fully connected feed-forward network. The sub-layers of the encoder include residual connections and normalization. The final layer outputs context vectors with semantic information and position embedding.
The decoder also consists of two layers, each layer containing the same two sub-layers as the encoder. To ensure that the model’s prediction results depend solely on information from the previous 
 steps, a masking mechanism is added to the self-attention mechanism of the decoder. Additionally, there is another sub-layer that performs multi-head attention calculation on the encoder’s output and provides additional context information to the decoder.
The model achieves the learning of complete key information by incorporating key sentence embedding and knowledge embedding into the computation of attention distribution, as Equations (2) through (5):
where represents the kth state generated by the key sentence from a Transformer layer, and represents the kth state generated by knowledge from a Transformer layer.
3.4 Key Sentence Priority Strategy
When the information in a knowledge graph is incomplete or has accuracy issues, the model automatically adjusts the weight distribution of the information it relies on, particularly by increasing the emphasis on key sentences. This is because key sentences typically contain information directly related to the answer, making them the primary source of information. During the question generation process, the model increases the weights of these key sentences, thus relying more on the information they provide to generate questions. This strategy helps the model extract the most crucial information.'
''
        """,
        "Information Systems Research": """
        Information Systems Research示例框架结构：
        1. 理论背景：基于组织理论和信息系统理论
        2. 研究问题：明确的理论贡献点
        3. 概念框架：多层次的理论模型
        4. 假设发展：基于文献的理论假设
        5. 方法论：严谨的研究设计
        """,
        "Journal of Management Information Systems": """
        Journal of Management Information Systems示例框架结构：
        1. 管理视角：从管理角度分析问题
        2. 技术背景：相关技术发展现状
        3. 理论模型：管理信息系统理论
        4. 研究假设：管理决策相关假设
        5. 实证设计：管理实践验证
        """,
        "Information & Management": """
        Information & Management示例框架结构：
        1. 信息管理视角：信息系统的管理价值
        2. 理论基础：信息管理理论
        3. 概念模型：信息价值创造模型
        4. 研究假设：信息管理效果假设
        5. 研究方法：信息管理实证研究
        """,
        "European Journal of Information Systems": """
        European Journal of Information Systems示例框架结构：
        1. 欧洲视角：欧洲信息系统研究特色
        2. 理论基础：欧洲信息系统理论传统
        3. 概念框架：跨文化信息系统模型
        4. 研究假设：欧洲情境下的假设
        5. 方法论：欧洲研究传统方法
        """
    }
    
    return journal_examples.get(journal_name)
