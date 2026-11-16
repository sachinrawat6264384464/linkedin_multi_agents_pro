"use client";

import React, { useState, useEffect } from "react";
import { Sidebar, NAV_ITEMS } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { OverviewView } from "@/components/dashboard/OverviewView";
import { DatabaseCenterView } from "@/components/database/DatabaseCenterView";
import { AgentsView } from "@/components/agents/AgentsView";
import { WorkflowDagView } from "@/components/workflows/WorkflowDagView";
import { McpIntegrationsView } from "@/components/mcp/McpIntegrationsView";
import { ContentStudioView } from "@/components/content/ContentStudioView";
import { ResearchLibraryView } from "@/components/research/ResearchLibraryView";
import { MediaStudioView } from "@/components/media/MediaStudioView";
import { ApprovalCenterView } from "@/components/approvals/ApprovalCenterView";
import { PublishingHistoryView } from "@/components/publishing/PublishingHistoryView";
import { MonitoringCenterView } from "@/components/monitoring/MonitoringCenterView";
import { ModelConfigView } from "@/components/models/ModelConfigView";
import { SettingsView } from "@/components/settings/SettingsView";
import { api } from "@/lib/api-client";
import { Bot, Workflow, CheckSquare, ShieldAlert, PenTool, Database, Plug, Activity, Settings as SettingsIcon } from "lucide-react";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<string>("overview");
  const [backendOnline, setBackendOnline] = useState<boolean>(false);
  const [healthData, setHealthData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Poll backend health status periodically
  useEffect(() => {
    async function checkHealth() {
      try {
        const data = await api.get("/api/v1/health");
        setHealthData(data);
        setBackendOnline(data.status === "healthy");
      } catch (err) {
        setBackendOnline(false);
      } finally {
        setLoading(false);
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const activeItem = NAV_ITEMS.find((item) => item.id === activeTab) || NAV_ITEMS[0];

  return (
    <div className="flex h-screen bg-[#090909] text-white overflow-hidden">
      {/* Collapsible Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        backendOnline={backendOnline}
      />

      {/* Main Command Center Stage */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Topbar
          activeTabTitle={activeItem.label}
          backendOnline={backendOnline}
          dbConfigured={healthData?.services?.database?.configured || false}
          ollamaReady={healthData?.services?.ollama?.status === "ready"}
        />

        <main className="flex-1 overflow-y-auto p-6">
          {activeTab === "overview" && (
            <OverviewView
              health={healthData}
              loading={loading}
              onNavigateTab={(tab) => setActiveTab(tab)}
            />
          )}

          {activeTab === "agents" && (
            <AgentsView />
          )}

          {activeTab === "workflows" && (
            <WorkflowDagView />
          )}

          {activeTab === "approvals" && (
            <ApprovalCenterView />
          )}

          {activeTab === "content" && (
            <ContentStudioView />
          )}

          {activeTab === "media" && (
            <MediaStudioView />
          )}

          {activeTab === "research" && (
            <ResearchLibraryView />
          )}

          {activeTab === "database" && (
            <DatabaseCenterView />
          )}

          {activeTab === "mcp" && (
            <McpIntegrationsView />
          )}

          {activeTab === "publishing" && (
            <PublishingHistoryView />
          )}

          {activeTab === "monitoring" && (
            <MonitoringCenterView />
          )}

          {activeTab === "models" && (
            <ModelConfigView />
          )}

          {activeTab === "settings" && (
            <SettingsView />
          )}

          {activeTab !== "overview" && 
           activeTab !== "agents" && 
           activeTab !== "workflows" && 
           activeTab !== "tasks" &&
           activeTab !== "approvals" &&
           activeTab !== "content" && 
           activeTab !== "media" &&
           activeTab !== "research" && 
           activeTab !== "calendar" &&
           activeTab !== "publishing" &&
           activeTab !== "database" && 
           activeTab !== "mcp" && 
           activeTab !== "monitoring" && 
           activeTab !== "models" && 
           activeTab !== "settings" && (
            <div className="p-8 rounded-xl bg-[#141414] border border-[#262626] flex flex-col items-center justify-center min-h-[400px] text-center">
              <div className="w-12 h-12 rounded-xl bg-[#1f1f1f] border border-[#2e2e2e] flex items-center justify-center mb-4 text-[#E53935]">
                <activeItem.icon className="w-6 h-6" />
              </div>
              <h2 className="text-lg font-bold text-white">{activeItem.label}</h2>
              <p className="text-xs text-[#A3A3A3] max-w-md mt-1">
                This enterprise module is hooked into the AgentOS architecture and will be fully wired in the upcoming implementation phase.
              </p>
              <div className="mt-4 px-3 py-1 rounded-full bg-[#1c1c1c] border border-[#2b2b2b] text-[11px] font-mono text-[#737373]">
                Module ID: {activeItem.id} • API v1 Route Ready
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
