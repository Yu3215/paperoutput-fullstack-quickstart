import { useState } from "react";
import { Button } from "@/components/ui/button";
import { SquarePen, Brain, Send, StopCircle, Zap, Cpu, FileText, BookOpen, Server } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";

interface PaperFrameworkFormProps {
  onSubmit: (paperTopic: string, methodology: string, journalRequirements: string, effort: string, model: string, apiConfig: string) => void;
  onCancel: () => void;
  isLoading: boolean;
  hasHistory: boolean;
}

export const PaperFrameworkForm: React.FC<PaperFrameworkFormProps> = ({
  onSubmit,
  onCancel,
  isLoading,
  hasHistory,
}) => {
  const [paperTopic, setPaperTopic] = useState("");
  const [methodology, setMethodology] = useState("");
  const [journalRequirements, setJournalRequirements] = useState("");
  const [customJournal, setCustomJournal] = useState("");
  const [effort, setEffort] = useState("medium");
  const [model, setModel] = useState("deepseek-r1:14b");
  const [apiConfig, setApiConfig] = useState("api1");

  const handleInternalSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const finalJournalRequirements = journalRequirements === "custom" ? customJournal : journalRequirements;
    if (!paperTopic.trim() || !methodology.trim() || !finalJournalRequirements.trim()) return;
    onSubmit(paperTopic, methodology, finalJournalRequirements, effort, model, apiConfig);
    setPaperTopic("");
    setMethodology("");
    setJournalRequirements("");
    setCustomJournal("");
  };

  const handleInternalKeyDown = (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleInternalSubmit();
    }
  };

  const finalJournalRequirements = journalRequirements === "custom" ? customJournal : journalRequirements;
  const isSubmitDisabled = !paperTopic.trim() || !methodology.trim() || !finalJournalRequirements.trim() || isLoading;

  // 模型配置映射
  const modelConfigs = {
    api1: {
      name: "deepseek-r1:14b",
      description: "OpenAI官方API",
      icon: "🤖",
      color: "text-green-400"
    },
    api2: {
      name: "claude-opus-4-20250514",
      description: "Antropic API",
      icon: "🧠",
      color: "text-blue-400"
    },
    api3: {
      name: "gemini-2.0-flash",
      description: "Google API",
      icon: "⭐",
      color: "text-yellow-400"
    }
  };

  return (
    <form
      onSubmit={handleInternalSubmit}
      className={`flex flex-col gap-4 p-3`}
    >
      {/* 论文主题 */}
      <div className="space-y-2">
        <Label htmlFor="paper-topic" className="text-neutral-300">
          <FileText className="h-4 w-4 inline mr-2" />
          论文主题
        </Label>
        <Textarea
          id="paper-topic"
          value={paperTopic}
          onChange={(e) => setPaperTopic(e.target.value)}
          placeholder="请输入您的论文主题和研究问题..."
          className={`w-full text-neutral-100 placeholder-neutral-500 resize-none border-neutral-600 focus:border-neutral-400 focus:outline-none focus:ring-0 
                        md:text-base min-h-[80px] max-h-[200px] bg-neutral-700`}
          rows={3}
        />
      </div>

      {/* 研究方法 */}
      <div className="space-y-2">
        <Label htmlFor="methodology" className="text-neutral-300">
          <Brain className="h-4 w-4 inline mr-2" />
          研究方法
        </Label>
        <Textarea
          id="methodology"
          value={methodology}
          onChange={(e) => setMethodology(e.target.value)}
          placeholder="请描述您的研究方法、数据收集方式、分析技术等..."
          className={`w-full text-neutral-100 placeholder-neutral-500 resize-none border-neutral-600 focus:border-neutral-400 focus:outline-none focus:ring-0 
                        md:text-base min-h-[80px] max-h-[200px] bg-neutral-700`}
          rows={3}
        />
      </div>

      {/* 期刊要求 */}
      <div className="space-y-2">
        <Label htmlFor="journal-requirements" className="text-neutral-300">
          <BookOpen className="h-4 w-4 inline mr-2" />
          目标期刊
        </Label>
        <Select value={journalRequirements} onValueChange={setJournalRequirements}>
          <SelectTrigger className="w-full bg-neutral-700 border-neutral-600 text-neutral-300">
            <SelectValue placeholder="选择目标期刊" />
          </SelectTrigger>
          <SelectContent className="bg-neutral-700 border-neutral-600 text-neutral-300">
            <SelectItem value="ACM Low-Resource Language" className="hover:bg-neutral-600">
            ACM Low-Resource Language
            </SelectItem>
            <SelectItem value="Information Systems Research" className="hover:bg-neutral-600">
              Information Systems Research
            </SelectItem>
            <SelectItem value="Journal of Management Information Systems" className="hover:bg-neutral-600">
              Journal of Management Information Systems
            </SelectItem>
            <SelectItem value="Information & Management" className="hover:bg-neutral-600">
              Information & Management
            </SelectItem>
            <SelectItem value="European Journal of Information Systems" className="hover:bg-neutral-600">
              European Journal of Information Systems
            </SelectItem>
            <SelectItem value="custom" className="hover:bg-neutral-600">
              自定义期刊
            </SelectItem>
          </SelectContent>
        </Select>
        {journalRequirements === "custom" && (
          <Textarea
            value={customJournal}
            onChange={(e) => setCustomJournal(e.target.value)}
            placeholder="请描述目标期刊的具体要求和写作风格..."
            className={`w-full text-neutral-100 placeholder-neutral-500 resize-none border-neutral-600 focus:border-neutral-400 focus:outline-none focus:ring-0 
                          md:text-base min-h-[60px] max-h-[150px] bg-neutral-700`}
            rows={2}
          />
        )}
      </div>

      {/* 配置选项 */}
      <div className="flex items-center justify-between">
        <div className="flex flex-row gap-2">
          {/* 努力程度 */}
          <div className="flex flex-row gap-2 bg-neutral-700 border-neutral-600 text-neutral-300 focus:ring-neutral-500 rounded-xl rounded-t-sm pl-2">
            <div className="flex flex-row items-center text-sm">
              <Brain className="h-4 w-4 mr-2" />
              精炼次数
            </div>
            <Select value={effort} onValueChange={setEffort}>
              <SelectTrigger className="w-[120px] bg-transparent border-none cursor-pointer">
                <SelectValue placeholder="Effort" />
              </SelectTrigger>
              <SelectContent className="bg-neutral-700 border-neutral-600 text-neutral-300 cursor-pointer">
                <SelectItem value="low" className="hover:bg-neutral-600">
                  1次
                </SelectItem>
                <SelectItem value="medium" className="hover:bg-neutral-600">
                  2次
                </SelectItem>
                <SelectItem value="high" className="hover:bg-neutral-600">
                  3次
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* API配置选择 */}
          <div className="flex flex-row gap-2 bg-neutral-700 border-neutral-600 text-neutral-300 focus:ring-neutral-500 rounded-xl rounded-t-sm pl-2">
            <div className="flex flex-row items-center text-sm ml-2">
              <Server className="h-4 w-4 mr-2" />
              API配置
            </div>
            <Select value={apiConfig} onValueChange={setApiConfig}>
              <SelectTrigger className="w-[180px] bg-transparent border-none cursor-pointer">
                <SelectValue placeholder="API Config" />
              </SelectTrigger>
              <SelectContent className="bg-neutral-700 border-neutral-600 text-neutral-300 cursor-pointer">
                <SelectItem value="api1" className="hover:bg-neutral-600">
                  <div className="flex items-center">
                    <span className="mr-2">{modelConfigs.api1.icon}</span>
                    <div>
                      <div className={`font-medium ${modelConfigs.api1.color}`}>{modelConfigs.api1.name}</div>
                      <div className="text-xs text-neutral-400">{modelConfigs.api1.description}</div>
                    </div>
                  </div>
                </SelectItem>
                <SelectItem value="api2" className="hover:bg-neutral-600">
                  <div className="flex items-center">
                    <span className="mr-2">{modelConfigs.api2.icon}</span>
                    <div>
                      <div className={`font-medium ${modelConfigs.api2.color}`}>{modelConfigs.api2.name}</div>
                      <div className="text-xs text-neutral-400">{modelConfigs.api2.description}</div>
                    </div>
                  </div>
                </SelectItem>
                <SelectItem value="api3" className="hover:bg-neutral-600">
                  <div className="flex items-center">
                    <span className="mr-2">{modelConfigs.api3.icon}</span>
                    <div>
                      <div className={`font-medium ${modelConfigs.api3.color}`}>{modelConfigs.api3.name}</div>
                      <div className="text-xs text-neutral-400">{modelConfigs.api3.description}</div>
                    </div>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* 提交按钮 */}
        <div className="-mt-3">
          {isLoading ? (
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="text-red-500 hover:text-red-400 hover:bg-red-500/10 p-2 cursor-pointer rounded-full transition-all duration-200"
              onClick={onCancel}
            >
              <StopCircle className="h-5 w-5" />
            </Button>
          ) : (
            <Button
              type="submit"
              variant="ghost"
              className={`${
                isSubmitDisabled
                  ? "text-neutral-500"
                  : "text-blue-500 hover:text-blue-400 hover:bg-blue-500/10"
              } p-2 cursor-pointer rounded-full transition-all duration-200 text-base`}
              disabled={isSubmitDisabled}
            >
              生成Framework
              <Send className="h-5 w-5" />
            </Button>
          )}
        </div>
      </div>

      {/* 新建按钮 */}
      {hasHistory && (
        <div className="flex justify-end">
          <Button
            className="bg-neutral-700 border-neutral-600 text-neutral-300 cursor-pointer rounded-xl"
            variant="default"
            onClick={() => window.location.reload()}
          >
            <SquarePen size={16} />
            新建Framework
          </Button>
        </div>
      )}
    </form>
  );
}; 