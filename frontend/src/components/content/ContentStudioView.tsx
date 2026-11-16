"use client";

import React, { useState } from "react";
import { PenTool, Sparkles, Save, Eye, Hash, Send, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api-client";

export const ContentStudioView: React.FC = () => {
  const [topic, setTopic] = useState<string>("State Checkpointing in Multi-Agent LangGraph Systems");
  const [hook, setHook] = useState<string>("Why 90% of autonomous AI agent architectures break down in production.");
  const [body, setBody] = useState<string>(
    "Building an agent prototype with an LLM is a weekend project.\n\n" +
    "Building a production agent system that survives server restarts, recovers from dropped network sockets, and guarantees database ACID consistency is where software engineering begins.\n\n" +
    "Here are 3 architectural rules we enforce:\n" +
    "1. Neon PostgreSQL as the durable source of truth (zero in-memory permanent state)\n" +
    "2. Model Context Protocol (MCP) tool execution with strict least-privilege\n" +
    "3. Cryptographic human-in-the-loop approval signatures before publishing"
  );
  const [cta, setCta] = useState<string>("How do you handle state recovery in your agent workflows?");
  const [hashtags, setHashtags] = useState<string>("#AIEngineering #SystemDesign #SoftwareArchitecture #LangGraph");
  const [saving, setSaving] = useState<boolean>(false);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);
  const [generating, setGenerating] = useState<boolean>(false);

  const fullPostText = `${hook}\n\n${body}\n\n${cta}\n\n${hashtags}`;
  const charCount = fullPostText.length;

  const handleGenerateVariations = async () => {
    setGenerating(true);
    try {
      const res = await api.post("/api/v1/content/generate", {
        topic,
        category: "AI Engineering",
      });
      if (res.variations && res.variations.length > 0) {
        const first = res.variations[0];
        setHook(first.hook || hook);
        setBody(first.main_body || body);
        setCta(first.cta || cta);
        if (first.hashtags) {
          setHashtags(first.hashtags.join(" "));
        }
      }
    } catch (err) {
      console.error("Failed to generate variations:", err);
    } finally {
      setGenerating(false);
    }
  };

  const handleSaveDraft = async () => {
    setSaving(true);
    setSavedSuccess(false);
    try {
      await api.post("/api/v1/content/drafts", {
        title: topic,
        topic,
        category: "AI Engineering",
        hook,
        main_body: body,
        cta,
        hashtags: hashtags.split(" ").filter(t => t.startsWith("#")),
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error("Failed to save draft:", err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Studio Header */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <PenTool className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Content Studio & Post Editor</h1>
            <p className="text-xs text-[#A3A3A3]">
              High-Signal Technical Copywriting • Immutable Versioning • Live LinkedIn Feed Preview
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleGenerateVariations}
            disabled={generating}
            className="px-3.5 py-1.5 rounded-lg bg-[#1f1f1f] hover:bg-[#2a2a2a] text-white text-xs font-medium flex items-center gap-1.5 border border-[#333333] transition-colors"
          >
            <Sparkles className={`w-3.5 h-3.5 text-[#E53935] ${generating ? "animate-spin" : ""}`} />
            <span>{generating ? "Generating..." : "Generate AI Variations"}</span>
          </button>

          <button
            onClick={handleSaveDraft}
            disabled={saving}
            className="px-4 py-1.5 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-[#E53935]/20 transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{saving ? "Saving..." : savedSuccess ? "Saved!" : "Save Version"}</span>
          </button>
        </div>
      </div>

      {/* Editor & Preview Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Editor Pane */}
        <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#242424]">
            <span className="text-xs font-mono uppercase tracking-wider text-[#A3A3A3]">
              Technical Content Editor
            </span>
            <div className="text-[11px] font-mono text-[#737373]">
              {charCount} / 3000 chars
            </div>
          </div>

          <div>
            <label className="text-[11px] font-mono text-[#A3A3A3] block mb-1">Topic</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
            />
          </div>

          <div>
            <label className="text-[11px] font-mono text-[#A3A3A3] block mb-1">Opening Hook</label>
            <textarea
              value={hook}
              onChange={(e) => setHook(e.target.value)}
              rows={2}
              className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg p-2.5 text-xs font-medium text-white focus:outline-none focus:border-[#E53935] resize-none"
            />
          </div>

          <div>
            <label className="text-[11px] font-mono text-[#A3A3A3] block mb-1">Main Body Paragraphs</label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={8}
              className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg p-2.5 text-xs text-[#d1d1d1] leading-relaxed focus:outline-none focus:border-[#E53935] resize-none"
            />
          </div>

          <div>
            <label className="text-[11px] font-mono text-[#A3A3A3] block mb-1">Closing CTA</label>
            <input
              type="text"
              value={cta}
              onChange={(e) => setCta(e.target.value)}
              className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
            />
          </div>

          <div>
            <label className="text-[11px] font-mono text-[#A3A3A3] block mb-1">Hashtags</label>
            <input
              type="text"
              value={hashtags}
              onChange={(e) => setHashtags(e.target.value)}
              className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg px-3 py-1.5 text-xs font-mono text-[#A3A3A3] focus:outline-none focus:border-[#E53935]"
            />
          </div>
        </div>

        {/* Live LinkedIn Feed Preview */}
        <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col">
          <div className="flex items-center justify-between pb-3 border-b border-[#242424] mb-4">
            <div className="flex items-center gap-2">
              <Eye className="w-3.5 h-3.5 text-[#E53935]" />
              <span className="text-xs font-mono uppercase tracking-wider text-white font-medium">
                LinkedIn Feed Preview
              </span>
            </div>
            <span className="text-[10px] font-mono text-emerald-400">Desktop View</span>
          </div>

          {/* LinkedIn Simulated Post Card */}
          <div className="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-3 flex-1 flex flex-col justify-between">
            <div>
              {/* Post Author Bar */}
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-full bg-[#242424] border border-[#333333] flex items-center justify-center font-bold text-white text-xs">
                  SA
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white leading-tight">Lead Software Architect</h4>
                  <p className="text-[10px] text-[#A3A3A3]">Principal AI & System Design Engineer</p>
                  <p className="text-[9px] text-[#737373]">Now • 🌐 Public</p>
                </div>
              </div>

              {/* Post Body */}
              <div className="text-xs text-[#e0e0e0] space-y-2 whitespace-pre-line leading-relaxed font-sans">
                <p className="font-semibold text-white">{hook}</p>
                <p className="text-[#cccccc]">{body}</p>
                <p className="text-white font-medium">{cta}</p>
                <p className="text-blue-400 font-mono text-[11px]">{hashtags}</p>
              </div>
            </div>

            {/* LinkedIn Footer Metrics */}
            <div className="pt-3 border-t border-[#262626] flex items-center justify-between text-[11px] text-[#737373]">
              <span>👍 428 Reactions</span>
              <span>💬 87 Comments • 14 Reposts</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

