"use client";

import React, { useState, useEffect } from "react";
import { Plug, ShieldCheck, Wrench, Play, CheckCircle2, AlertOctagon } from "lucide-react";
import { api } from "@/lib/api-client";

interface MCPServer {
  id: string;
  name: string;
  description: string;
  status: string;
  tools: MCPTool[];
}

interface MCPTool {
  id: string;
  server_id: string;
  name: string;
  description: string;
  input_schema: any;
  is_dangerous: boolean;
}

export const McpIntegrationsView: React.FC = () => {
  const [servers, setServers] = useState<MCPServer[]>([]);
  const [selectedTool, setSelectedTool] = useState<MCPTool | null>(null);
  const [testAgent, setTestAgent] = useState<string>("research");
  const [executionResult, setExecutionResult] = useState<any>(null);
  const [executing, setExecuting] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadMCP() {
      try {
        const data = await api.get<MCPServer[]>("/api/v1/mcp/servers");
        setServers(data);
        if (data.length > 0 && data[0].tools.length > 0) {
          setSelectedTool(data[0].tools[0]);
        }
      } catch (err) {
        console.error("Failed to load MCP servers:", err);
      } finally {
        setLoading(false);
      }
    }
    loadMCP();
  }, []);

  const handleTestTool = async () => {
    if (!selectedTool) return;
    setExecuting(true);
    setExecutionResult(null);

    try {
      const res = await api.post("/api/v1/mcp/execute", {
        agent_id: testAgent,
        tool_id: selectedTool.id,
        parameters: { query: "Autonomous AI Agents" },
      });
      setExecutionResult(res);
    } catch (err: any) {
      setExecutionResult({
        success: false,
        error: err.message || "Execution error",
      });
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <Plug className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Model Context Protocol (MCP) Hub</h1>
            <p className="text-xs text-[#A3A3A3]">
              Standardized Tool Access Layer • Least-Privilege Authorization Enforcement
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="text-xs font-mono text-emerald-400">7 Registered Servers</span>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Servers & Tools List */}
        <div className="space-y-4">
          {servers.map((server) => (
            <div key={server.id} className="p-4 rounded-xl bg-[#141414] border border-[#262626]">
              <div className="flex items-center justify-between pb-2 border-b border-[#242424]">
                <h3 className="text-xs font-bold text-white">{server.name}</h3>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {server.status}
                </span>
              </div>
              <p className="text-[11px] text-[#737373] mt-2 mb-3">{server.description}</p>

              <div className="space-y-1.5">
                {server.tools.map((tool) => (
                  <button
                    key={tool.id}
                    onClick={() => setSelectedTool(tool)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-xs font-mono flex items-center justify-between transition-all ${
                      selectedTool?.id === tool.id
                        ? "bg-[#1f1f1f] border-l-2 border-[#E53935] text-white"
                        : "bg-[#111111] hover:bg-[#191919] text-[#A3A3A3]"
                    }`}
                  >
                    <span className="truncate">{tool.name}</span>
                    {tool.is_dangerous && (
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-[#E53935]/20 text-[#E53935] font-sans">
                        Sensitive
                      </span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Selected Tool Details & Permission Tester */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col justify-between">
          {selectedTool ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-[#242424]">
                <div>
                  <h2 className="text-sm font-bold font-mono text-white">{selectedTool.id}</h2>
                  <p className="text-xs text-[#A3A3A3] mt-0.5">{selectedTool.description}</p>
                </div>
              </div>

              {/* Input Schema */}
              <div>
                <span className="text-[10px] font-mono uppercase text-[#A3A3A3] block mb-1.5">
                  Input Parameter Schema (JSON)
                </span>
                <pre className="p-3 rounded-lg bg-[#0d0d0d] border border-[#262626] text-[11px] font-mono text-emerald-400 overflow-x-auto">
                  {JSON.stringify(selectedTool.input_schema, null, 2)}
                </pre>
              </div>

              {/* Permission & Test Execution Simulator */}
              <div className="p-4 rounded-xl bg-[#111111] border border-[#242424] space-y-3">
                <span className="text-xs font-semibold text-white block">
                  Least-Privilege Security Tester
                </span>
                <p className="text-[11px] text-[#A3A3A3]">
                  Select an agent role to simulate permission validation and execution.
                </p>

                <div className="flex items-center gap-3">
                  <select
                    value={testAgent}
                    onChange={(e) => setTestAgent(e.target.value)}
                    className="bg-[#1c1c1c] border border-[#2d2d2d] rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
                  >
                    <option value="research">Research Agent</option>
                    <option value="writer">Content Writer</option>
                    <option value="designer">Visual Designer</option>
                    <option value="quality">Quality Checker</option>
                    <option value="publisher">LinkedIn Publisher</option>
                    <option value="database">Database Agent</option>
                    <option value="monitoring">Monitoring Agent</option>
                  </select>

                  <button
                    onClick={handleTestTool}
                    disabled={executing}
                    className="px-3.5 py-1.5 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-medium flex items-center gap-1.5 transition-all shadow-md shadow-[#E53935]/20"
                  >
                    <Play className={`w-3 h-3 ${executing ? "animate-spin" : ""}`} />
                    <span>{executing ? "Testing..." : "Test Tool"}</span>
                  </button>
                </div>

                {executionResult && (
                  <div
                    className={`p-3 rounded-lg border text-xs font-mono mt-3 ${
                      executionResult.success
                        ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                        : "bg-[#E53935]/10 border-[#E53935]/30 text-[#E53935]"
                    }`}
                  >
                    <p className="font-bold">
                      {executionResult.success ? "EXECUTION SUCCESS" : "PERMISSION DENIED / ERROR"}
                    </p>
                    <pre className="mt-1 text-[11px] whitespace-pre-wrap">
                      {JSON.stringify(executionResult.data || executionResult.error, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-xs text-[#737373]">
              Select a tool to inspect schema and test permissions
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
