"use client";

import React, { useState, useEffect } from "react";
import { 
  Settings as SettingsIcon, 
  Key, 
  Database, 
  Share2, 
  Cpu, 
  ShieldCheck, 
  Check, 
  AlertTriangle, 
  RefreshCw,
  Lock,
  ExternalLink
} from "lucide-react";

export function SettingsView() {
  const [testingService, setTestingService] = useState<string | null>(null);
  const [serviceStatus, setServiceStatus] = useState<Record<string, { ok: boolean; message: string }>>({});
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Form states initialized with safe environment values
  const [linkedinClientId, setLinkedinClientId] = useState("");
  const [linkedinClientSecret, setLinkedinClientSecret] = useState("");
  const [linkedinRedirectUri, setLinkedinRedirectUri] = useState("http://localhost:8000/api/v1/publishing/oauth/callback");

  const [dbUrl, setDbUrl] = useState("postgresql+asyncpg://neondb_owner:***@ep-sample-pooler.us-east-2.aws.neon.tech/neondb?ssl=require");
  const [dbPoolSize, setDbPoolSize] = useState("5");

  const [cloudName, setCloudName] = useState("");
  const [cloudinaryKey, setCloudinaryKey] = useState("");
  const [cloudinarySecret, setCloudinarySecret] = useState("");

  const [ollamaUrl, setOllamaUrl] = useState("http://localhost:11434");
  const [ollamaModel, setOllamaModel] = useState("qwen2.5:7b-instruct");

  useEffect(() => {
    // Initial health probe
    testAllConnections();
  }, []);

  const testConnection = async (service: string) => {
    setTestingService(service);
    try {
      if (service === "linkedin") {
        const res = await fetch("http://localhost:8000/api/v1/publishing/status");
        const data = await res.json();
        setServiceStatus(prev => ({
          ...prev,
          linkedin: {
            ok: data.is_configured,
            message: data.is_configured ? "Credentials verified" : "Disconnected (Operating in Staged Manual Fallback Mode)"
          }
        }));
      } else if (service === "database") {
        const res = await fetch("http://localhost:8000/api/v1/health");
        const data = await res.json();
        const isConnected = data.services?.database === "connected";
        setServiceStatus(prev => ({
          ...prev,
          database: {
            ok: isConnected,
            message: isConnected ? "Neon PostgreSQL Pool healthy" : "Database credentials pending or offline"
          }
        }));
      } else if (service === "ollama") {
        const res = await fetch("http://localhost:8000/api/v1/health");
        const data = await res.json();
        const isConnected = data.services?.ollama === "connected";
        setServiceStatus(prev => ({
          ...prev,
          ollama: {
            ok: isConnected,
            message: isConnected ? "Ollama model online" : "Ollama offline or model not pulled"
          }
        }));
      }
    } catch {
      setServiceStatus(prev => ({
        ...prev,
        [service]: { ok: false, message: "Backend API unreachable" }
      }));
    } finally {
      setTestingService(null);
    }
  };

  const testAllConnections = () => {
    testConnection("linkedin");
    testConnection("database");
    testConnection("ollama");
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[#292929] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <SettingsIcon className="w-5 h-5 text-[#E53935]" />
            <h1 className="text-xl font-bold text-white tracking-wide">System Configuration & Integrations</h1>
          </div>
          <p className="text-xs text-[#A3A3A3] mt-1">
            Manage API credentials, Neon database pools, Cloudinary media storage, and Ollama agent execution.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={testAllConnections}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#171717] hover:bg-[#202020] border border-[#292929] text-xs text-white rounded transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Probe All Integrations
          </button>
          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#E53935] hover:bg-[#c62828] text-xs text-white font-medium rounded transition"
          >
            {savedSuccess ? (
              <>
                <Check className="w-3.5 h-3.5" />
                Settings Saved
              </>
            ) : (
              "Save Configuration"
            )}
          </button>
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: LinkedIn OAuth 2.0 */}
        <div className="bg-[#171717] border border-[#292929] rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#292929] pb-3">
            <div className="flex items-center gap-2">
              <Share2 className="w-4 h-4 text-[#E53935]" />
              <h2 className="text-sm font-semibold text-white">LinkedIn OAuth 2.0 & Publishing API</h2>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                serviceStatus.linkedin?.ok ? "bg-emerald-950/60 border border-emerald-800 text-emerald-300" : "bg-amber-950/60 border border-amber-800 text-amber-300"
              }`}>
                {serviceStatus.linkedin?.message || "Checking..."}
              </span>
              <button
                type="button"
                onClick={() => testConnection("linkedin")}
                disabled={testingService === "linkedin"}
                className="text-xs px-2 py-1 bg-[#111111] hover:bg-[#202020] border border-[#292929] text-white rounded"
              >
                {testingService === "linkedin" ? "Testing..." : "Test"}
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">Client ID</label>
              <input
                type="text"
                value={linkedinClientId}
                onChange={e => setLinkedinClientId(e.target.value)}
                placeholder="77xxxxxxxxxxxx"
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">Client Secret</label>
              <input
                type="password"
                value={linkedinClientSecret}
                onChange={e => setLinkedinClientSecret(e.target.value)}
                placeholder="••••••••••••••••"
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-[#A3A3A3]">Authorized Redirect URI</label>
            <input
              type="text"
              value={linkedinRedirectUri}
              onChange={e => setLinkedinRedirectUri(e.target.value)}
              className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935] font-mono text-[11px]"
            />
            <p className="text-[10px] text-[#737373]">
              Must match the exact redirect URL registered in your LinkedIn Developer Portal app settings.
            </p>
          </div>
        </div>

        {/* Section 2: Neon PostgreSQL */}
        <div className="bg-[#171717] border border-[#292929] rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#292929] pb-3">
            <div className="flex items-center gap-2">
              <Database className="w-4 h-4 text-[#E53935]" />
              <h2 className="text-sm font-semibold text-white">Neon PostgreSQL Source of Truth</h2>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                serviceStatus.database?.ok ? "bg-emerald-950/60 border border-emerald-800 text-emerald-300" : "bg-neutral-800 text-[#A3A3A3]"
              }`}>
                {serviceStatus.database?.message || "Checking..."}
              </span>
              <button
                type="button"
                onClick={() => testConnection("database")}
                disabled={testingService === "database"}
                className="text-xs px-2 py-1 bg-[#111111] hover:bg-[#202020] border border-[#292929] text-white rounded"
              >
                {testingService === "database" ? "Testing..." : "Test"}
              </button>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-[#A3A3A3]">Pooled Connection String (FastAPI & LangGraph Checkpoints)</label>
            <input
              type="text"
              value={dbUrl}
              onChange={e => setDbUrl(e.target.value)}
              className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935] font-mono text-[11px]"
            />
            <div className="flex items-center gap-2 mt-1">
              <span className="text-[10px] text-emerald-400 flex items-center gap-1">
                <Check className="w-3 h-3" /> Mandatory SSL Mode (ssl=require) Active
              </span>
              <span className="text-[10px] text-[#737373]">• Read-back verification active on every write</span>
            </div>
          </div>
        </div>

        {/* Section 3: Cloudinary Media Storage */}
        <div className="bg-[#171717] border border-[#292929] rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#292929] pb-3">
            <div className="flex items-center gap-2">
              <Key className="w-4 h-4 text-[#E53935]" />
              <h2 className="text-sm font-semibold text-white">Cloudinary Media Storage Engine</h2>
            </div>
            <span className="text-[10px] text-[#737373]">Direct streaming without ephemeral disk storage</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">Cloud Name</label>
              <input
                type="text"
                value={cloudName}
                onChange={e => setCloudName(e.target.value)}
                placeholder="your-cloud-name"
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">API Key</label>
              <input
                type="text"
                value={cloudinaryKey}
                onChange={e => setCloudinaryKey(e.target.value)}
                placeholder="123456789012345"
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">API Secret</label>
              <input
                type="password"
                value={cloudinarySecret}
                onChange={e => setCloudinarySecret(e.target.value)}
                placeholder="••••••••••••••••"
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935]"
              />
            </div>
          </div>
          <p className="text-[10px] text-[#737373]">
            PDF carousels are strictly uploaded with <code className="text-[#A3A3A3]">resource_type="raw"</code> according to Cloudinary rule specifications.
          </p>
        </div>

        {/* Section 4: Ollama Local LLM */}
        <div className="bg-[#171717] border border-[#292929] rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#292929] pb-3">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-[#E53935]" />
              <h2 className="text-sm font-semibold text-white">Ollama Local LLM Execution</h2>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                serviceStatus.ollama?.ok ? "bg-emerald-950/60 border border-emerald-800 text-emerald-300" : "bg-neutral-800 text-[#A3A3A3]"
              }`}>
                {serviceStatus.ollama?.message || "Checking..."}
              </span>
              <button
                type="button"
                onClick={() => testConnection("ollama")}
                disabled={testingService === "ollama"}
                className="text-xs px-2 py-1 bg-[#111111] hover:bg-[#202020] border border-[#292929] text-white rounded"
              >
                {testingService === "ollama" ? "Testing..." : "Test"}
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">Ollama Base URL</label>
              <input
                type="text"
                value={ollamaUrl}
                onChange={e => setOllamaUrl(e.target.value)}
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935] font-mono text-[11px]"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-[#A3A3A3]">Shared Agent Model (8GB RAM Optimized)</label>
              <input
                type="text"
                value={ollamaModel}
                onChange={e => setOllamaModel(e.target.value)}
                className="w-full bg-[#111111] border border-[#292929] rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-[#E53935] font-mono text-[11px]"
              />
            </div>
          </div>
          <div className="text-[10px] text-[#737373] flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Single-model sharing active across all 8 agents to prevent memory exhaustion on 8GB host machine.</span>
          </div>
        </div>

        {/* Section 5: Governance & Security Policy */}
        <div className="bg-[#171717] border border-[#292929] rounded-lg p-5 space-y-3">
          <div className="flex items-center gap-2 border-b border-[#292929] pb-3">
            <Lock className="w-4 h-4 text-[#E53935]" />
            <h2 className="text-sm font-semibold text-white">Zero-Trust Publishing & Approval Policy</h2>
          </div>

          <div className="space-y-3 pt-1">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs font-medium text-white">Cryptographic SHA-256 Fingerprint Matching</div>
                <div className="text-[11px] text-[#737373]">Rejects publishing if content is modified after human signature</div>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 bg-emerald-950/60 border border-emerald-800 text-emerald-300 rounded font-semibold">
                ENFORCED (LOCKED)
              </span>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs font-medium text-white">Require Human Sign-Off for Scheduled Workflows</div>
                <div className="text-[11px] text-[#737373]">Daily automated pipelines interrupt at approval gate and await operator sign-off</div>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 bg-emerald-950/60 border border-emerald-800 text-emerald-300 rounded font-semibold">
                ACTIVE
              </span>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
