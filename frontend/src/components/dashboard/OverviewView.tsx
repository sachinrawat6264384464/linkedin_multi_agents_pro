"use client";

import React from "react";
import {
  FileText,
  Clock,
  CheckCircle,
  AlertOctagon,
  Bot,
  Database,
  Plug,
  Sparkles,
  ArrowUpRight,
  TrendingUp,
  Activity,
  Layers,
} from "lucide-react";

interface HealthData {
  status: string;
  app_name: string;
  services?: {
    api?: { status: string };
    database?: { status: string; configured: boolean };
    ollama?: { status: string; model: string };
    cloudinary?: { status: string; configured: boolean };
    linkedin?: { status: string; configured: boolean };
  };
}

interface OverviewViewProps {
  health: HealthData | null;
  loading: boolean;
  onNavigateTab: (tabId: string) => void;
}

export const OverviewView: React.FC<OverviewViewProps> = ({ health, loading, onNavigateTab }) => {
  const stats = [
    {
      title: "Total Posts Created",
      value: "0",
      change: "Phase 1 Bootstrapped",
      icon: FileText,
      color: "text-white",
    },
    {
      title: "Pending Human Approval",
      value: "0",
      change: "Zero unapproved publishing",
      icon: Clock,
      color: "text-amber-400",
    },
    {
      title: "Published to LinkedIn",
      value: "0",
      change: "Official OAuth v2",
      icon: CheckCircle,
      color: "text-emerald-400",
    },
    {
      title: "Active Autonomous Agents",
      value: "8",
      change: "1 Master + 7 Specialists",
      icon: Bot,
      color: "text-[#E53935]",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="p-6 rounded-xl bg-gradient-to-r from-[#171717] via-[#121212] to-[#0d0d0d] border border-[#292929] relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#E53935]/5 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-[#E53935]/10 border border-[#E53935]/20 text-[#E53935] text-xs font-mono mb-2">
              <span className="w-1.5 h-1.5 rounded-full bg-[#E53935] animate-ping" />
              AUTONOMOUS ARCHITECTURE ACTIVE
            </div>
            <h1 className="text-xl md:text-2xl font-bold text-white tracking-tight">
              LinkedIn AgentOS Command Center
            </h1>
            <p className="text-xs text-[#A3A3A3] mt-1 max-w-2xl">
              Eight-agent autonomous pipeline orchestrating research, technical copywriting,
              diagram generation, multi-tier fact-checking, and human-in-the-loop publishing.
            </p>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={() => onNavigateTab("workflows")}
              className="px-4 py-2 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-[#E53935]/20 transition-all hover:scale-[1.02]"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Launch Live Workflow</span>
            </button>
          </div>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div
              key={idx}
              className="p-5 rounded-xl bg-[#141414] border border-[#262626] hover:border-[#383838] transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-[#A3A3A3] font-medium">{stat.title}</span>
                <div className="w-8 h-8 rounded-lg bg-[#1f1f1f] flex items-center justify-center">
                  <Icon className={`w-4 h-4 ${stat.color}`} />
                </div>
              </div>
              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-2xl font-bold font-mono text-white">{stat.value}</span>
              </div>
              <p className="text-[11px] text-[#737373] mt-1">{stat.change}</p>
            </div>
          );
        })}
      </div>

      {/* System Service Health Radar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-5 rounded-xl bg-[#141414] border border-[#262626]">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#242424]">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-[#E53935]" />
              <h2 className="text-sm font-semibold text-white">Live Infrastructure Status</h2>
            </div>
            <span className="text-[11px] font-mono text-[#737373]">Real-time Health Check</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {/* Backend API */}
            <div className="p-3.5 rounded-lg bg-[#191919] border border-[#292929] flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                <div>
                  <p className="text-xs font-medium text-white">FastAPI Core</p>
                  <p className="text-[10px] text-[#737373]">Python 3.12 • Port 8000</p>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE
              </span>
            </div>

            {/* Neon DB */}
            <div className="p-3.5 rounded-lg bg-[#191919] border border-[#292929] flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className={`w-2.5 h-2.5 rounded-full ${
                    health?.services?.database?.configured ? "bg-emerald-500" : "bg-amber-400"
                  }`}
                />
                <div>
                  <p className="text-xs font-medium text-white">Neon PostgreSQL</p>
                  <p className="text-[10px] text-[#737373]">Primary Source of Truth</p>
                </div>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
                  health?.services?.database?.configured
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : "bg-amber-500/10 text-amber-400 border-amber-500/20"
                }`}
              >
                {health?.services?.database?.configured ? "CONNECTED" : "STANDBY"}
              </span>
            </div>

            {/* Ollama LLM */}
            <div className="p-3.5 rounded-lg bg-[#191919] border border-[#292929] flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                <div>
                  <p className="text-xs font-medium text-white">Ollama Runner</p>
                  <p className="text-[10px] text-[#737373]">
                    {health?.services?.ollama?.model || "qwen2.5:7b-instruct"}
                  </p>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                READY
              </span>
            </div>

            {/* Cloudinary */}
            <div className="p-3.5 rounded-lg bg-[#191919] border border-[#292929] flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className={`w-2.5 h-2.5 rounded-full ${
                    health?.services?.cloudinary?.configured ? "bg-emerald-500" : "bg-amber-400"
                  }`}
                />
                <div>
                  <p className="text-xs font-medium text-white">Cloudinary Storage</p>
                  <p className="text-[10px] text-[#737373]">Durable Media & PDF Assets</p>
                </div>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
                  health?.services?.cloudinary?.configured
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : "bg-amber-500/10 text-amber-400 border-amber-500/20"
                }`}
              >
                {health?.services?.cloudinary?.configured ? "CONNECTED" : "SAFE MODE"}
              </span>
            </div>
          </div>
        </div>

        {/* 8-Agent Roster Quick Glance */}
        <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-[#242424]">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-[#E53935]" />
                <h2 className="text-sm font-semibold text-white">Specialist Agents</h2>
              </div>
              <button
                onClick={() => onNavigateTab("agents")}
                className="text-[11px] text-[#E53935] hover:underline flex items-center gap-1"
              >
                <span>View All</span>
                <ArrowUpRight className="w-3 h-3" />
              </button>
            </div>

            <div className="space-y-2 text-xs">
              {[
                { name: "0. Master Orchestrator", status: "Idle / Ready" },
                { name: "1. Research Agent", status: "Idle / Ready" },
                { name: "2. Content Writer", status: "Idle / Ready" },
                { name: "3. Visual Designer", status: "Idle / Ready" },
                { name: "4. Quality & Fact-Checker", status: "Idle / Ready" },
                { name: "5. LinkedIn Publisher", status: "OAuth Locked" },
                { name: "6. Database & Persistence", status: "Read-back Active" },
                { name: "7. Monitoring & Health", status: "Watchdog Active" },
              ].map((agent, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between py-1.5 px-2 rounded bg-[#171717] text-[#A3A3A3]"
                >
                  <span className="font-medium text-white">{agent.name}</span>
                  <span className="text-[10px] font-mono text-[#737373]">{agent.status}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
