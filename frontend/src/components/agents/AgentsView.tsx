"use client";

import React, { useState, useEffect } from "react";
import { Bot, Cpu, CheckCircle2, Sliders, Edit3, Save } from "lucide-react";
import { api } from "@/lib/api-client";

interface AgentItem {
  id: string;
  name: string;
  role: string;
  description: string;
  model_name: string;
  system_prompt: string;
}

export const AgentsView: React.FC = () => {
  const [agents, setAgents] = useState<AgentItem[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<AgentItem | null>(null);
  const [editedPrompt, setEditedPrompt] = useState<string>("");
  const [saving, setSaving] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadAgents() {
      try {
        const data = await api.get<AgentItem[]>("/api/v1/agents");
        setAgents(data);
        if (data.length > 0) {
          setSelectedAgent(data[0]);
          setEditedPrompt(data[0].system_prompt);
        }
      } catch (err) {
        console.error("Failed to load agents:", err);
      } finally {
        setLoading(false);
      }
    }
    loadAgents();
  }, []);

  const handleSelect = (agent: AgentItem) => {
    setSelectedAgent(agent);
    setEditedPrompt(agent.system_prompt);
  };

  const handleSavePrompt = async () => {
    if (!selectedAgent) return;
    setSaving(true);
    try {
      await api.put(`/api/v1/agents/${selectedAgent.id}/config`, {
        system_prompt: editedPrompt,
      });
      // Update local state
      setAgents(prev => prev.map(a => a.id === selectedAgent.id ? { ...a, system_prompt: editedPrompt } : a));
    } catch (err) {
      console.error("Failed to save agent prompt:", err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Autonomous Agent Roster</h1>
            <p className="text-xs text-[#A3A3A3]">
              8 Specialized Autonomous Agents • Shared Quantized Ollama Runner
            </p>
          </div>
        </div>
        <div className="px-3 py-1 rounded-full bg-[#1c1c1c] border border-[#2b2b2b] text-[11px] font-mono text-emerald-400">
          8/8 Active
        </div>
      </div>

      {/* Main Grid: Roster & Prompt Editor */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Cards */}
        <div className="space-y-3">
          {agents.map((agent) => {
            const isSelected = selectedAgent?.id === agent.id;
            return (
              <div
                key={agent.id}
                onClick={() => handleSelect(agent)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#1c1c1c] border-[#E53935] shadow-lg shadow-[#E53935]/10"
                    : "bg-[#141414] border-[#262626] hover:border-[#383838]"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-[#E53935]">
                      {agent.id.toUpperCase()}
                    </span>
                    <h3 className="text-xs font-semibold text-white">{agent.name}</h3>
                  </div>
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                </div>
                <p className="text-[11px] text-[#A3A3A3] mt-1">{agent.role}</p>
                <div className="mt-3 flex items-center gap-2 text-[10px] font-mono text-[#737373]">
                  <Cpu className="w-3 h-3 text-[#A3A3A3]" />
                  <span>{agent.model_name}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Agent Details & System Prompt Editor */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col">
          {selectedAgent ? (
            <div className="flex-1 flex flex-col space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-[#242424]">
                <div>
                  <h2 className="text-sm font-bold text-white">{selectedAgent.name}</h2>
                  <p className="text-xs text-[#A3A3A3]">{selectedAgent.description}</p>
                </div>
                <button
                  onClick={handleSavePrompt}
                  disabled={saving}
                  className="px-3.5 py-1.5 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-medium flex items-center gap-2 shadow-lg shadow-[#E53935]/20 transition-all"
                >
                  <Save className="w-3.5 h-3.5" />
                  <span>{saving ? "Saving..." : "Save Prompt"}</span>
                </button>
              </div>

              <div>
                <label className="text-[11px] font-mono text-[#A3A3A3] uppercase tracking-wider block mb-2">
                  System Prompt Template (Editable)
                </label>
                <textarea
                  value={editedPrompt}
                  onChange={(e) => setEditedPrompt(e.target.value)}
                  rows={14}
                  className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg p-3 text-xs font-mono text-white placeholder-[#737373] focus:outline-none focus:border-[#E53935] transition-colors resize-none"
                />
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-xs text-[#737373]">
              Select an agent to view and configure prompts
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
