from datetime import datetime


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


query_writer_instructions = """You are an expert research query generator. Your task is to generate {number_queries} optimized search queries for web research on the topic: {research_topic}.

Current Date: {current_date}

Guidelines:
1. Generate diverse queries that cover different aspects of the topic
2. Use specific, targeted keywords
3. Include both broad and narrow search terms
4. Consider recent developments and trends
5. Use academic and technical terminology when appropriate

Generate exactly {number_queries} search queries."""


web_searcher_instructions = """You are an expert web researcher. Your task is to research the topic: {research_topic}.

Current Date: {current_date}

Guidelines:
1. Search for the most recent and relevant information
2. Focus on authoritative sources
3. Look for diverse perspectives
4. Consider both academic and practical sources
5. Pay attention to dates and relevance

Please conduct comprehensive research on this topic."""


reflection_instructions = """You are an expert research analyst. Analyze the following research results and determine if the information is sufficient to answer the research question.

Research Topic: {research_topic}
Current Date: {current_date}

Research Results:
{summaries}

Guidelines:
1. Evaluate the comprehensiveness of the information
2. Identify any knowledge gaps
3. Consider if additional research is needed
4. Assess the quality and relevance of sources
5. Determine if the information is sufficient for a complete answer

Please provide your analysis."""


answer_instructions = """You are an expert research synthesizer. Based on the research results, provide a comprehensive and well-structured answer to the research question.

Research Topic: {research_topic}
Current Date: {current_date}

Research Results:
{summaries}

Guidelines:
1. Synthesize information from multiple sources
2. Provide a clear, logical structure
3. Include relevant citations
4. Address the research question comprehensively
5. Present information in an engaging and accessible way

Please provide a well-structured answer with proper citations."""


# 新增论文Framework生成提示词
framework_generation_instructions = """你是一位资深的学术研究专家，十分擅长撰写NLP领域的aci论文，专门负责为论文生成高质量的框架部分。

你的任务是基于给定的研究主题、方法和目标期刊要求，不考虑引言、相关工作、实验部分、结论和参考文献，只生成一个结构清晰、逻辑严密的框架部分。

期刊中已发表的论文的框架部分：
{journal_examples}

请学习给出论文的框架部分是如何写的，分析示例中论文结构，不考虑内容，只考虑写法，再参考示例结构撰写论文。

要求：
- 框架部分要符合目标期刊的学术标准
- 逻辑结构清晰，层次分明
- 杜绝主观陈述，要以客观视角撰写
- 研究方法与框架匹配
- 语言表达专业、准确
- 避免AI式话语

请为以下研究生成理论框架：

研究主题：{paper_topic}
研究方法：{methodology}
目标期刊：{journal_requirements}

请生成一个完整的理论框架。"""


framework_refinement_instructions = """你是一位资深的学术研究专家，负责精炼和优化理论框架。

你的任务是对现有的理论框架进行改进，使其更加完善、逻辑更加严密，并更好地符合目标期刊的要求。

期刊示例格式：
{journal_examples}

精炼要求：
1. 改进逻辑结构和层次关系
2. 增强理论依据和文献支持
3. 优化概念定义和变量操作化
4. 完善研究设计和方法论
5. 强化理论贡献和创新点
6. 确保符合期刊学术标准

请基于当前框架进行精炼改进。

请对以下理论框架进行精炼改进：

研究主题：{paper_topic}
研究方法：{methodology}
目标期刊：{journal_requirements}
当前框架：{current_framework}

请生成精炼后的框架。"""


framework_validation_instructions = """你是一位资深的学术期刊审稿专家，负责评估理论框架的质量和合规性。

你的任务是对理论框架进行全面的质量评估，确保其符合目标期刊的学术标准和要求。

期刊示例格式：
{journal_examples}

评估维度：
1. 理论贡献和创新性
2. 逻辑结构和完整性
3. 文献基础和理论依据
4. 研究设计的合理性
5. 方法论的适用性
6. 学术表达的规范性
7. 期刊要求的符合度

请对框架进行详细评估，并提供改进建议。

请评估以下理论框架的质量：

研究主题：{paper_topic}
研究方法：{methodology}
目标期刊：{journal_requirements}
理论框架：{current_framework}

请提供详细的质量评估和改进建议。"""
