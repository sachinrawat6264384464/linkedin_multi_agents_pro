"use client";

import React, { useState, useEffect } from "react";
import { 
  Cpu, 
  Server, 
  Check, 
  Zap, 
  RefreshCw, 
  ShieldCheck, 
  Sliders, 
  AlertTriangle 
} from "lucide-react";

export function ModelConfigView() {
  const [activeModel, setActiveModel] = useState("qwen2.5:7b-instruct");
  const [contextWindow, setContextWindow] = useState(4096);
  const [temperature, setTemperature] = useState(0.7);
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const supportedModels = [
    {
      tag: "qwen2.5:7b-instruct",
      name: "Qwen 2.5 7B Instruct",
      recommended: true,
      vram: "4.6 GB",
      description: "Highest architectural reasoning quality, structured JSON compliance, and prompt adherence."
    },
    {
      tag: "qwen2.5:3b-instruct",
      name: "Qwen 2.5 3B Instruct",
      recommended: false,
      vram: "2.2 GB",
      description: "Ultra-compact footprint for systems with heavy background processes on 8GB host machine."
    },
    {
      tag: "llama3.2:3b",
      name: "Llama 3.2 3B Instruct",
      recommended: false,
      vram: "2.4 GB",
      description: "Fast generation speed, suitable for rapid draft iterations and hook synthesis."
    },
    {
      tag: "mistral:7b-instruct",
      name: "Mistral 7B Instruct v0.3",
      recommended: false,
      vram: "4.8 GB",
      description: "Strong writing voice and editorial quality."
    }
  ];

  const handleSwitchModel = async (modelTag: string) => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/monitoring/models/switch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model_tag: modelTag,
          context_window: contextWindow,
          temperature: temperature
        })
      });

      if (res.ok) {
        const data = await res.json();
        setActiveModel(data.new_model);
        setSuccessMsg(`Switched active LLM to ${modelTag}`);
        setTimeout(() => setSuccessMsg(null), 3000);
      }
    } catch {
      setActiveModel(modelTag);
      setSuccessMsg(`Switched active LLM to ${modelTag} (offline fallback)`);
      setTimeout(() => setSuccessMsg(null), 3000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[#292929] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-[#E53935]" />
            <h1 className="text-xl font-bold text-white tracking-wide">Model Execution & Local LLM Engine</h1>
          </div>
          <p className="text-xs text-[#A3A3A3] mt-1">
            Configure local Ollama execution with 8GB RAM constrained single-model memory optimization.
          </p>
        </div>
        {successMsg && (
          <div className="flex items-center gap-1.5 px-3 py-1 bg-emerald-950/70 border border-emerald-800 text-emerald-300 text-xs rounded animate-fade-in">
            <Check className="w-3.5 h-3.5" />
            {successMsg}
          </div>
        )}
      </div>

      {/* 8GB RAM Optimization Callout */}
      <div className="bg-[#171717] border border-[#292929] rounded-lg p-4 flex items-start gap-3">
        <div className="p-2 bg-[#E53935]/10 border border-[#E53935]/30 rounded text-[#E53935]">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-semibold text-white">Resource Efficiency Strategy (8GB RAM Host)</div>
          <p className="text-[11px] text-[#A3A3A3] mt-0.5 leading-relaxed">
            All 8 specialist agents (Orchestrator, Research, Writer, Visual, Quality, Publisher, DB, Sentinel) share this single quantized Ollama model instance via distinct system prompts and structured Pydantic schemas. This prevents out-of-memory crashes on 8GB host environments.
          </p>
        </div>
      </div>

      {/* Model Selection Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {supportedModels.map((m) => {
          const isSelected = activeModel === m.tag;
          return (
            <div
              key={m.tag}
              onClick={() => handleSwitchModel(m.tag)}
              className={`p-4 rounded-lg border cursor-pointer transition flex flex-col justify-between ${
                isSelected
                  ? "bg-[#1f1717] border-[#E53935] shadow-sm"
                  : "bg-[#171717] border-[#292929] hover:border-[#383838]"
              }`}
            >
              <div>
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-white">{m.name}</span>
                      {m.recommended && (
                        <span className="text-[9px] px-1.5 py-0.5 bg-emerald-950 border border-emerald-800 text-emerald-300 rounded font-semibold uppercase">
                          Recommended
                        </span>
                      )}
                    </div>
                    <span className="text-[10px] font-mono text-[#737373] mt-0.5 block">{m.tag}</span>
                  </div>
                  <span className="text-[10px] font-mono text-[#A3A3A3] px-2 py-0.5 bg-[#111111] rounded border border-[#292929]">
                    {m.vram}
                  </span>
                </div>
                <p className="text-xs text-[#A3A3A3] mt-2.5 leading-normal">
                  {m.description}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-[#292929] flex items-center justify-between text-[11px]">
                <span className={isSelected ? "text-[#E53935] font-semibold" : "text-[#737373]"}>
                  {isSelected ? "Active Execution Model" : "Click to Activate"}
                </span>
                {isSelected && <Check className="w-4 h-4 text-[#E53935]" />}
              </div>
            </div>
          );
        })}
      </div>

      {/* Hyperparameters Card */}
      <div className="bg-[#171717] border border-[#292929] rounded-lg p-5 space-y-4">
        <div className="flex items-center gap-2 border-b border-[#292929] pb-3">
          <Sliders className="w-4 h-4 text-[#E53935]" />
          <h2 className="text-xs font-semibold text-white uppercase tracking-wider">
            Inference Hyperparameters
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-1">
          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-[#A3A3A3]">Context Window</span>
              <span className="text-white font-mono">{contextWindow} tokens</span>
            </div>
            <input
              type="range"
              min="2048"
              max="16384"
              step="1024"
              value={contextWindow}
              onChange={(e) => setContextWindow(Number(e.target.value))}
              className="w-full accent-[#E53935]"
            />
            <div className="text-[10px] text-[#737373]">
              Default 4096 tokens provides optimal balance for multi-source research and prompt caching.
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-[#A3A3A3]">Temperature</span>
              <span className="text-white font-mono">{temperature}</span>
            </div>
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.05"
              value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
              className="w-full accent-[#E53935]"
            />
            <div className="text-[10px] text-[#737373]">
              Lower (0.3 - 0.5) for fact-checking and structured schemas; higher (0.7 - 0.8) for creative hooks.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

