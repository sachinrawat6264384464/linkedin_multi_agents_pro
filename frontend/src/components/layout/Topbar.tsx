"use client";

import React from "react";
import { Search, Bell, Database, Cpu, User, CheckCircle2, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

interface TopbarProps {
  activeTabTitle: string;
  backendOnline: boolean;
  dbConfigured: boolean;
  ollamaReady: boolean;
}

export const Topbar: React.FC<TopbarProps> = ({
  activeTabTitle,
  backendOnline,
  dbConfigured,
  ollamaReady,
}) => {
  return (
    <header className="h-16 border-b border-[#292929] bg-[#0c0c0c]/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Breadcrumbs and Title */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-xs text-[#737373]">
          <span>AgentOS</span>
          <span>/</span>
          <span className="text-white font-medium">{activeTabTitle}</span>
        </div>
      </div>

      {/* Global Search */}
      <div className="hidden md:flex items-center relative w-72">
        <Search className="w-3.5 h-3.5 text-[#737373] absolute left-3 pointer-events-none" />
        <input
          type="text"
          placeholder="Search agents, workflows, tasks..."
          className="w-full bg-[#171717] border border-[#292929] rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-[#737373] focus:outline-none focus:border-[#E53935] transition-colors"
        />
      </div>

      {/* Status Badges & User */}
      <div className="flex items-center gap-3">
        {/* Ollama Status Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#171717] border border-[#292929] text-[11px] text-[#A3A3A3]">
          <Cpu className="w-3 h-3 text-[#A3A3A3]" />
          <span>Ollama:</span>
          <span className={cn("font-medium", ollamaReady ? "text-emerald-400" : "text-amber-400")}>
            {ollamaReady ? "Ready" : "Local Standby"}
          </span>
        </div>

        {/* Database Status Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#171717] border border-[#292929] text-[11px] text-[#A3A3A3]">
          <Database className="w-3 h-3 text-[#A3A3A3]" />
          <span>Neon DB:</span>
          <span className={cn("font-medium", dbConfigured ? "text-emerald-400" : "text-amber-400")}>
            {dbConfigured ? "Connected" : "Pending Credentials"}
          </span>
        </div>

        {/* Notifications */}
        <button className="p-2 rounded-lg bg-[#171717] border border-[#292929] text-[#A3A3A3] hover:text-white hover:border-[#3d3d3d] transition-colors relative">
          <Bell className="w-3.5 h-3.5" />
          <span className="w-1.5 h-1.5 rounded-full bg-[#E53935] absolute top-1.5 right-1.5" />
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-2 pl-2 border-l border-[#292929]">
          <div className="w-7 h-7 rounded-full bg-[#242424] border border-[#333333] flex items-center justify-center text-white text-xs font-semibold">
            SA
          </div>
          <div className="hidden xl:flex flex-col text-left">
            <span className="text-xs font-medium text-white leading-tight">Lead Architect</span>
            <span className="text-[10px] text-[#737373]">Admin Role</span>
          </div>
        </div>
      </div>
    </header>
  );
};
