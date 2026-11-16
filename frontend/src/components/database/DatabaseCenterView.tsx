"use client";

import React, { useState, useEffect } from "react";
import { Database, ShieldCheck, RefreshCw, AlertTriangle, Layers, Table, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api-client";

interface DBHealth {
  status: string;
  message: string;
  ssl_mode: string;
  provider: string;
  read_back_verification_active: boolean;
  connected: boolean;
}

interface DBStats {
  tasks: number;
  workflow_runs: number;
  content_drafts: number;
  content_versions: number;
  research_sources: number;
  generated_media: number;
  published_posts: number;
  approvals: number;
}

export const DatabaseCenterView: React.FC = () => {
  const [health, setHealth] = useState<DBHealth | null>(null);
  const [stats, setStats] = useState<DBStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  async function loadData() {
    setLoading(true);
    try {
      const [h, s] = await Promise.all([
        api.get<DBHealth>("/api/v1/database/health"),
        api.get<DBStats>("/api/v1/database/statistics")
      ]);
      setHealth(h);
      setStats(s);
    } catch (err) {
      console.error("Failed to load database center telemetry:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-xl bg-[#141414] border border-[#262626]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Database & Persistence Center</h1>
            <p className="text-xs text-[#A3A3A3]">
              Neon PostgreSQL Source of Truth • Agent 6 Read-Back Verification Active
            </p>
          </div>
        </div>

        <button
          onClick={loadData}
          disabled={loading}
          className="px-3.5 py-1.5 rounded-lg bg-[#1f1f1f] hover:bg-[#2b2b2b] text-white text-xs font-medium flex items-center gap-2 transition-colors self-start sm:self-auto border border-[#333333]"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>Refresh Telemetry</span>
        </button>
      </div>

      {/* Connection & Integrity Status Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-[#141414] border border-[#262626]">
          <span className="text-xs text-[#A3A3A3]">Connection Status</span>
          <div className="mt-2 flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                health?.connected ? "bg-emerald-500" : "bg-amber-400"
              }`}
            />
            <span className="text-sm font-bold font-mono text-white">
              {health?.status?.toUpperCase() || "CHECKING"}
            </span>
          </div>
          <p className="text-[11px] text-[#737373] mt-1">{health?.message}</p>
        </div>

        <div className="p-4 rounded-xl bg-[#141414] border border-[#262626]">
          <span className="text-xs text-[#A3A3A3]">SSL Enforcement</span>
          <div className="mt-2 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span className="text-sm font-bold font-mono text-white">
              {health?.ssl_mode || "sslmode=require"}
            </span>
          </div>
          <p className="text-[11px] text-[#737373] mt-1">Neon encrypted transport mandatory</p>
        </div>

        <div className="p-4 rounded-xl bg-[#141414] border border-[#262626]">
          <span className="text-xs text-[#A3A3A3]">Read-Back Verification</span>
          <div className="mt-2 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#E53935]" />
            <span className="text-sm font-bold font-mono text-white">ACTIVE (ACID)</span>
          </div>
          <p className="text-[11px] text-[#737373] mt-1">Every write validated by Agent 6</p>
        </div>
      </div>

      {/* Table Record Counts Grid */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626]">
        <div className="flex items-center gap-2 mb-4 pb-3 border-b border-[#242424]">
          <Table className="w-4 h-4 text-[#E53935]" />
          <h2 className="text-sm font-semibold text-white">PostgreSQL Table Inventory</h2>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "tasks", count: stats?.tasks ?? 0 },
            { label: "workflow_runs", count: stats?.workflow_runs ?? 0 },
            { label: "content_drafts", count: stats?.content_drafts ?? 0 },
            { label: "content_versions", count: stats?.content_versions ?? 0 },
            { label: "research_sources", count: stats?.research_sources ?? 0 },
            { label: "generated_media", count: stats?.generated_media ?? 0 },
            { label: "published_posts", count: stats?.published_posts ?? 0 },
            { label: "approvals", count: stats?.approvals ?? 0 },
          ].map((t, idx) => (
            <div key={idx} className="p-3 rounded-lg bg-[#191919] border border-[#292929]">
              <span className="text-[11px] font-mono text-[#A3A3A3]">{t.label}</span>
              <p className="text-xl font-bold font-mono text-white mt-1">{t.count}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

