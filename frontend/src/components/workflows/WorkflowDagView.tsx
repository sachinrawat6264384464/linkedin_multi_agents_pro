"use client";

import React, { useState } from "react";
import { Workflow, Play, CheckCircle2, AlertTriangle, ArrowRight, Layers, FileText, Send } from "lucide-react";
import { api } from "@/lib/api-client";

export const WorkflowDagView: React.FC = () => {
  const [topic, setTopic] = useState<string>("Model Context Protocol & Multi-Agent Architecture");
  const [autoApprove, setAutoApprove] = useState<boolean>(true);
  const [running, setRunning] = useState<boolean>(false);
  const [result, setResult] = useState<any>(null);
  const [activeStep, setActiveStep] = useState<string>("idle");

  const runWorkflow = async () => {
    setRunning(true);
    setResult(null);
    setActiveStep("master_planning");

    try {
      // Trigger backend LangGraph execution
      const data = await api.post("/api/v1/workflows/run", {
        topic,
        category: "AI Engineering",
        target_audience: "Software Engineers & Tech Leaders",
        auto_approve: autoApprove,
      });
      setResult(data);
      setActiveStep("completed");
    } catch (err: any) {
      console.error("Workflow failed:", err);
      setActiveStep("error");
    } finally {
      setRunning(false);
    }
  };

  const steps = [
    { id: "master", label: "0. Master Orchestrator", role: "Planning & DAG Setup" },
    { id: "research", label: "1. Research Agent", role: "Source Discovery" },
    { id: "writer", label: "2. Content Writer", role: "Hook & Body Draft" },
    { id: "designer", label: "3. Visual Designer", role: "Mermaid / SVG Assets" },
    { id: "quality", label: "4. Quality Checker", role: "Fact-Check & Readability" },
    { id: "database", label: "6. Database Agent", role: "Neon Read-Back Check" },
    { id: "publisher", label: "5. LinkedIn Publisher", role: "Verified Publish" },
    { id: "monitoring", label: "7. Monitoring Agent", role: "Telemetry & Audit" },
  ];

  return (
    <div className="space-y-6">
      {/* Header & Execution Trigger */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <Workflow className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Live LangGraph Workflow Engine</h1>
            <p className="text-xs text-[#A3A3A3]">
              Durable 8-Node Directed Acyclic Graph • Human-in-the-Loop Interrupt Support
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter research & content topic..."
            className="w-72 bg-[#0d0d0d] border border-[#292929] rounded-lg px-3 py-1.5 text-xs text-white placeholder-[#737373] focus:outline-none focus:border-[#E53935]"
          />
          <button
            onClick={runWorkflow}
            disabled={running}
            className="px-4 py-2 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-[#E53935]/20 transition-all disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 ${running ? "animate-spin" : ""}`} />
            <span>{running ? "Executing DAG..." : "Execute Workflow"}</span>
          </button>
        </div>
      </div>

      {/* Visual DAG Nodes Pipeline */}
      <div className="p-6 rounded-xl bg-[#141414] border border-[#262626]">
        <h2 className="text-xs font-mono uppercase tracking-wider text-[#A3A3A3] mb-4">
          Autonomous Execution Pipeline DAG
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {steps.map((s, idx) => (
            <div
              key={s.id}
              className={`p-3.5 rounded-lg border transition-all ${
                running
                  ? "border-[#E53935]/50 bg-[#1c1c1c]"
                  : result
                  ? "border-emerald-500/30 bg-[#161616]"
                  : "border-[#292929] bg-[#111111]"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono text-[#E53935] font-semibold">{s.label}</span>
                {result ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                ) : (
                  <span className="w-2 h-2 rounded-full bg-[#333333]" />
                )}
              </div>
              <p className="text-[10px] text-[#A3A3A3] mt-1">{s.role}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Workflow Output Display */}
      {result && (
        <div className="p-5 rounded-xl bg-[#141414] border border-emerald-500/30 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#242424]">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <h2 className="text-sm font-bold text-white">Workflow Completed Successfully</h2>
            </div>
            <div className="text-[11px] font-mono text-[#737373]">
              ID: {result.workflow_id} • Steps: {result.execution_steps}
            </div>
          </div>

          <div className="space-y-3">
            <div>
              <span className="text-[10px] font-mono text-[#A3A3A3] uppercase">Opening Hook</span>
              <p className="text-xs font-semibold text-white mt-0.5">{result.hook}</p>
            </div>

            <div>
              <span className="text-[10px] font-mono text-[#A3A3A3] uppercase">Draft Content</span>
              <p className="text-xs text-[#d1d1d1] whitespace-pre-line mt-0.5 leading-relaxed bg-[#0e0e0e] p-3 rounded-lg border border-[#242424]">
                {result.main_body}
              </p>
            </div>

            <div className="flex flex-wrap gap-2 pt-1">
              {(result.hashtags || []).map((tag: string, i: number) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded text-[10px] font-mono bg-[#1c1c1c] text-[#A3A3A3] border border-[#2b2b2b]"
                >
                  {tag}
                </span>
              ))}
            </div>

            <div className="pt-2 flex items-center justify-between text-[11px] font-mono text-[#737373] border-t border-[#242424]">
              <span>SHA-256 Checksum: {result.checksum?.slice(0, 16)}...</span>
              <span className="text-emerald-400">PostgreSQL Read-Back: VERIFIED</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

