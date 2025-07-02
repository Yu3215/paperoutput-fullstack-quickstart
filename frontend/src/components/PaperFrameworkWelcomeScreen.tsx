import { PaperFrameworkForm } from "./PaperFrameworkForm";

interface PaperFrameworkWelcomeScreenProps {
  handleSubmit: (
    paperTopic: string,
    methodology: string,
    journalRequirements: string,
    effort: string,
    model: string,
    apiConfig: string
  ) => void;
  onCancel: () => void;
  isLoading: boolean;
}

export const PaperFrameworkWelcomeScreen: React.FC<PaperFrameworkWelcomeScreenProps> = ({
  handleSubmit,
  onCancel,
  isLoading,
}) => (
  <div className="flex flex-col items-center justify-center text-center px-4 flex-1 w-full max-w-4xl mx-auto gap-6">
    <div>
      <h1 className="text-5xl md:text-6xl font-semibold text-neutral-100 mb-3">
        论文Framework生成器
      </h1>
      <p className="text-xl md:text-2xl text-neutral-400 mb-4">
        基于您的研究主题和方法，生成符合期刊要求的理论框架
      </p>
      <div className="text-lg text-neutral-500 space-y-2">
        <p>✨ 智能生成理论框架和概念模型</p>
        <p>📚 支持多种顶级期刊格式</p>
        <p>🔬 基于您的研究方法优化内容</p>
        <p>📝 仅生成Framework部分，专注理论贡献</p>
      </div>
    </div>
    
    <div className="w-full max-w-3xl">
      <PaperFrameworkForm
        onSubmit={handleSubmit}
        isLoading={isLoading}
        onCancel={onCancel}
        hasHistory={false}
      />
    </div>
    
    <div className="text-sm text-neutral-500 space-y-1">
      <p>Powered by OpenAI and LangChain LangGraph.</p>
      <p>专注于生成高质量的学术理论框架，不包含Introduction、Related Work、Experiment和Conclusion部分。</p>
    </div>
  </div>
); 