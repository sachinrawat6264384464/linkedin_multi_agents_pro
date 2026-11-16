"use client";

import React, { useState } from "react";
import {
  LayoutDashboard,
  Bot,
  Workflow,
  CheckSquare,
  ShieldAlert,
  PenTool,
  Image as ImageIcon,
  Library,
  Calendar,
  History,
  Database,
  Plug,
  Activity,
  Cpu,
  Settings,
  ChevronLeft,
  ChevronRight,
  Radio,
} from "lucide-react";
import { cn } from "@/lib/utils";

export interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

export const NAV_ITEMS: NavItem[] = [
  { id: "overview", label: "Overview", icon: LayoutDashboard },
  { id: "agents", label: "AI Agents", icon: Bot },
  { id: "workflows", label: "Live Workflow", icon: Workflow },
  { id: "tasks", label: "Task Center", icon: CheckSquare },
  { id: "approvals", label: "Approval Center", icon: ShieldAlert },
  { id: "content", label: "Content Studio", icon: PenTool },
  { id: "media", label: "Media Studio", icon: ImageIcon },
  { id: "research", label: "Research Library", icon: Library },
  { id: "calendar", label: "Content Calendar", icon: Calendar },
  { id: "publishing", label: "Publishing History", icon: History },
  { id: "database", label: "Database Center", icon: Database },
  { id: "mcp", label: "MCP Integrations", icon: Plug },
  { id: "monitoring", label: "System Monitoring", icon: Activity },
  { id: "models", label: "Model Configuration", icon: Cpu },
  { id: "settings", label: "Settings", icon: Settings },
];

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  backendOnline: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, backendOnline }) => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "h-screen bg-[#0d0d0d] border-r border-[#292929] flex flex-col transition-all duration-300 z-30 select-none",
        collapsed ? "w-20" : "w-64"
      )}
    >
      {/* Brand Header */}
      <div className="h-16 px-4 border-b border-[#292929] flex items-center justify-between">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#E53935] to-[#A61B1B] flex items-center justify-center shrink-0 shadow-lg shadow-[#E53935]/20">
            <Radio className="w-4 h-4 text-white animate-pulse" />
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="font-bold tracking-tight text-white text-sm">AgentOS</span>
              <span className="text-[10px] text-[#A3A3A3] uppercase tracking-wider font-mono">LinkedIn Autonomous</span>
            </div>
          )}
        </div>
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-md hover:bg-[#1f1f1f] text-[#A3A3A3] hover:text-white transition-colors"
          title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto px-2 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all duration-150 group relative",
                isActive
                  ? "bg-[#1f1f1f] text-white border-l-2 border-[#E53935]"
                  : "text-[#A3A3A3] hover:text-white hover:bg-[#141414]"
              )}
            >
              <Icon
                className={cn(
                  "w-4 h-4 shrink-0 transition-colors",
                  isActive ? "text-[#E53935]" : "text-[#737373] group-hover:text-white"
                )}
              />
              {!collapsed && <span className="truncate">{item.label}</span>}
              {collapsed && (
                <div className="absolute left-full ml-3 px-2 py-1 bg-[#171717] border border-[#292929] text-white text-xs rounded-md shadow-xl whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50">
                  {item.label}
                </div>
              )}
            </button>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="p-3 border-t border-[#292929] bg-[#090909]">
        <div className="flex items-center gap-2 px-2 py-1.5 rounded-md bg-[#141414] border border-[#222222]">
          <div
            className={cn(
              "w-2 h-2 rounded-full",
              backendOnline ? "bg-emerald-500 animate-pulse" : "bg-[#E53935]"
            )}
          />
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-[11px] font-mono font-medium text-white truncate">
                {backendOnline ? "BACKEND ONLINE" : "DISCONNECTED"}
              </p>
              <p className="text-[9px] text-[#737373] truncate">Port 8000 • FastAPI</p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};
