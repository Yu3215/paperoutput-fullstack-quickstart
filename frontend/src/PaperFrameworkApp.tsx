import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";
import { useState, useEffect, useRef, useCallback } from "react";
import { ProcessedEvent } from "@/components/ActivityTimeline";
import { PaperFrameworkWelcomeScreen } from "@/components/PaperFrameworkWelcomeScreen";
import { ChatMessagesView } from "@/components/ChatMessagesView";

export default function PaperFrameworkApp() {
  const [processedEventsTimeline, setProcessedEventsTimeline] = useState<
    ProcessedEvent[]
  >([]);
  const [historicalActivities, setHistoricalActivities] = useState<
    Record<string, ProcessedEvent[]>
  >({});
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const hasFinalizeEventOccurredRef = useRef(false);

  const thread = useStream<{
    messages: Message[];
    paper_topic: string;
    methodology: string;
    journal_requirements: string;
    framework_refinement_loops: number;
    framework_model: string;
    api_config: string;
  }>({
    apiUrl: import.meta.env.DEV
      ? "http://localhost:2024"
      : "http://localhost:8123",
    assistantId: "agent",
    messagesKey: "messages",
    onFinish: (event: any) => {
      console.log("Framework generation completed:", event);
    },
    onUpdateEvent: (event: any) => {
      let processedEvent: ProcessedEvent | null = null;
      if (event.generate_framework) {
        processedEvent = {
          title: "生成理论框架",
          data: "正在基于您的研究主题和方法生成理论框架...",
        };
      } else if (event.refine_framework) {
        processedEvent = {
          title: "精炼框架内容",
          data: "正在优化框架的逻辑结构和学术表达...",
        };
      } else if (event.validate_framework) {
        processedEvent = {
          title: "验证框架质量",
          data: "正在验证框架的学术标准和期刊合规性...",
        };
      }
      if (processedEvent) {
        setProcessedEventsTimeline((prevEvents) => [
          ...prevEvents,
          processedEvent!,
        ]);
      }
    },
  });

  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollViewport = scrollAreaRef.current.querySelector(
        "[data-radix-scroll-area-viewport]"
      );
      if (scrollViewport) {
        scrollViewport.scrollTop = scrollViewport.scrollHeight;
      }
    }
  }, [thread.messages]);

  useEffect(() => {
    if (
      hasFinalizeEventOccurredRef.current &&
      !thread.isLoading &&
      thread.messages.length > 0
    ) {
      const lastMessage = thread.messages[thread.messages.length - 1];
      if (lastMessage && lastMessage.type === "ai" && lastMessage.id) {
        setHistoricalActivities((prev) => ({
          ...prev,
          [lastMessage.id!]: [...processedEventsTimeline],
        }));
      }
      hasFinalizeEventOccurredRef.current = false;
    }
  }, [thread.messages, thread.isLoading, processedEventsTimeline]);

  const handleSubmit = useCallback(
    (paperTopic: string, methodology: string, journalRequirements: string, effort: string, model: string, apiConfig: string) => {
      if (!paperTopic.trim() || !methodology.trim() || !journalRequirements.trim()) return;
      setProcessedEventsTimeline([]);
      hasFinalizeEventOccurredRef.current = false;

      // 转换努力程度为精炼次数
      let framework_refinement_loops = 1;
      switch (effort) {
        case "low":
          framework_refinement_loops = 1;
          break;
        case "medium":
          framework_refinement_loops = 2;
          break;
        case "high":
          framework_refinement_loops = 3;
          break;
      }

      const newMessages: Message[] = [
        ...(thread.messages || []),
        {
          type: "human",
          content: `论文主题: ${paperTopic}\n研究方法: ${methodology}\n目标期刊: ${journalRequirements}`,
          id: Date.now().toString(),
        },
      ];
      
      thread.submit({
        messages: newMessages,
        paper_topic: paperTopic,
        methodology: methodology,
        journal_requirements: journalRequirements,
        framework_refinement_loops: framework_refinement_loops,
        framework_model: model,
        api_config: apiConfig,
      });
    },
    [thread]
  );

  const handleCancel = useCallback(() => {
    thread.stop();
    window.location.reload();
  }, [thread]);

  return (
    <div className="flex h-screen bg-neutral-800 text-neutral-100 font-sans antialiased">
      <main className="flex-1 flex flex-col overflow-hidden max-w-6xl mx-auto w-full">
        <div
          className={`flex-1 overflow-y-auto ${
            thread.messages.length === 0 ? "flex" : ""
          }`}
        >
          {thread.messages.length === 0 ? (
            <PaperFrameworkWelcomeScreen
              handleSubmit={handleSubmit}
              isLoading={thread.isLoading}
              onCancel={handleCancel}
            />
          ) : (
            <ChatMessagesView
              messages={thread.messages}
              isLoading={thread.isLoading}
              scrollAreaRef={scrollAreaRef}
              onSubmit={(inputValue, effort, model) => {
                // 这里可以添加后续的交互功能
                console.log("Additional input:", inputValue, effort, model);
              }}
              onCancel={handleCancel}
              liveActivityEvents={processedEventsTimeline}
              historicalActivities={historicalActivities}
            />
          )}
        </div>
      </main>
    </div>
  );
} 