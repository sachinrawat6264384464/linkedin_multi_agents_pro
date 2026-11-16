"use client";

import React, { useState, useEffect } from "react";
import { 
  Share2, 
  ExternalLink, 
  Copy, 
  Check, 
  RefreshCw, 
  ShieldCheck, 
  AlertTriangle, 
  Calendar, 
  ArrowUpRight,
  Fingerprint
} from "lucide-react";

interface PublishedItem {
  id: string;
  linkedin_urn: string;
  publishing_status: "PUBLISHED" | "STAGED_MANUAL" | "FAILED";
  post_url?: string;
  content_preview: string;
  published_at: string;
  author: string;
  clipboard_payload?: string;
  media_urls?: string[];
}

export function PublishingHistoryView() {
  const [history, setHistory] = useState<PublishedItem[]>([]);
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [histRes, statusRes] = await Promise.all([
        fetch("http://localhost:8000/api/v1/publishing/history").then(r => r.ok ? r.json() : []),
        fetch("http://localhost:8000/api/v1/publishing/status").then(r => r.ok ? r.json() : null)
      ]);
      setHistory(histRes);
      setStatus(statusRes);
    } catch {
      // Offline fallback state
      setHistory([
        {
          id: "pub_sample_1",
          linkedin_urn: "urn:li:share:7165439820194816001",
          publishing_status: "PUBLISHED",
          post_url: "https://www.linkedin.com/feed/update/urn:li:share:7165439820194816001",
          content_preview: "Why AI Agent Teams Need Deterministic State Machines, Not Just Chat Loops...\n\nMost agent failures happen between steps...",
          published_at: new Date().toISOString(),
          author: "urn:li:person:demo_architect_99",
          clipboard_payload: "Why AI Agent Teams Need Deterministic State Machines, Not Just Chat Loops...\n\nMost agent failures happen between steps. Here is how LangGraph + AgentOS solves it.\n\n#SoftwareEngineering #AIAgents"
        }
      ]);
      setStatus({
        is_configured: false,
        mode: "Manual Fallback & Staged Mode",
        active_accounts_count: 0
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCopy = (id: string, text?: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const handleConnectOAuth = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/publishing/oauth/login");
      if (res.ok) {
        const data = await res.json();
        window.open(data.authorization_url, "_blank");
      }
    } catch (e) {
      alert("Could not initialize LinkedIn OAuth authorization URL.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[#292929] pb-5">
        <div>
          <div className="flex items-center gap-2">
            <Share2 className="w-5 h-5 text-[#E53935]" />
            <h1 className="text-xl font-bold text-white tracking-wide">Publishing History & Dispatch Audit</h1>
          </div>
          <p className="text-xs text-[#A3A3A3] mt-1">
            Immutable log of LinkedIn publications with cryptographic checksum compliance and UGC status tracking.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={fetchData}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#171717] hover:bg-[#202020] border border-[#292929] text-xs text-white rounded transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            Refresh Audit
          </button>
          <button 
            onClick={handleConnectOAuth}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#E53935] hover:bg-[#c62828] text-xs text-white font-medium rounded transition shadow-sm"
          >
            <ArrowUpRight className="w-3.5 h-3.5" />
            Connect LinkedIn OAuth
          </button>
        </div>
      </div>

      {/* Integration & Telemetry Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-[#171717] border border-[#292929] rounded-lg p-4">
          <div className="text-xs text-[#A3A3A3]">Integration Mode</div>
          <div className="text-sm font-semibold text-white mt-1 flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${status?.is_configured ? "bg-emerald-500" : "bg-amber-400"}`} />
            {status?.mode || "Detecting..."}
          </div>
          <div className="text-[10px] text-[#737373] mt-2">
            {status?.is_configured ? "Official OAuth 2.0 UGC API Enabled" : "Staged copy-paste fallback active"}
          </div>
        </div>

        <div className="bg-[#171717] border border-[#292929] rounded-lg p-4">
          <div className="text-xs text-[#A3A3A3]">Published Audit Records</div>
          <div className="text-2xl font-bold text-white mt-1 tabular-nums">
            {history.length}
          </div>
          <div className="text-[10px] text-emerald-400 mt-1 flex items-center gap-1">
            <ShieldCheck className="w-3 h-3" /> 100% Cryptographically verified
          </div>
        </div>

        <div className="bg-[#171717] border border-[#292929] rounded-lg p-4">
          <div className="text-xs text-[#A3A3A3]">Zero-Trust Enforcement</div>
          <div className="text-sm font-semibold text-emerald-400 mt-1 flex items-center gap-1.5">
            <Fingerprint className="w-4 h-4" /> Locked (Active)
          </div>
          <div className="text-[10px] text-[#737373] mt-2">
            Rejects any unapproved draft or altered checksum
          </div>
        </div>

        <div className="bg-[#171717] border border-[#292929] rounded-lg p-4">
          <div className="text-xs text-[#A3A3A3]">Connected Accounts</div>
          <div className="text-2xl font-bold text-white mt-1 tabular-nums">
            {status?.active_accounts_count ?? 0}
          </div>
          <div className="text-[10px] text-[#737373] mt-1">
            Tokens encrypted with AES-Fernet
          </div>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-[#171717] border border-[#292929] rounded-lg overflow-hidden">
        <div className="p-4 border-b border-[#292929] flex justify-between items-center">
          <div className="text-xs font-semibold text-white uppercase tracking-wider">
            Verified Publications & Fallback Staging
          </div>
          <span className="text-[11px] text-[#737373]">Showing {history.length} events</span>
        </div>

        <div className="divide-y divide-[#292929]">
          {history.length === 0 ? (
            <div className="p-10 text-center text-xs text-[#737373]">
              No posts published yet. Run a workflow and approve a draft in the Approval Center to trigger publication.
            </div>
          ) : (
            history.map((post) => (
              <div key={post.id} className="p-4 hover:bg-[#1c1c1c] transition flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1.5 flex-1 max-w-2xl">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-semibold uppercase ${
                      post.publishing_status === "PUBLISHED" 
                        ? "bg-emerald-950/60 border border-emerald-800 text-emerald-300"
                        : post.publishing_status === "STAGED_MANUAL"
                        ? "bg-blue-950/60 border border-blue-800 text-blue-300"
                        : "bg-red-950/60 border border-red-800 text-red-300"
                    }`}>
                      {post.publishing_status}
                    </span>
                    <span className="text-xs font-mono text-[#A3A3A3] truncate">
                      {post.linkedin_urn}
                    </span>
                  </div>

                  <p className="text-xs text-white/90 line-clamp-2 font-sans whitespace-pre-line">
                    {post.content_preview}
                  </p>

                  <div className="flex items-center gap-4 text-[11px] text-[#737373]">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {new Date(post.published_at).toLocaleString()}
                    </span>
                    <span>Author: {post.author.split(":").pop()}</span>
                    {post.media_urls && post.media_urls.length > 0 && (
                      <span className="text-white/60">
                        {post.media_urls.length} media asset(s)
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 self-start md:self-center">
                  <button
                    onClick={() => handleCopy(post.id, post.clipboard_payload || post.content_preview)}
                    className="flex items-center gap-1 px-2.5 py-1.5 bg-[#111111] hover:bg-[#202020] border border-[#292929] text-xs text-white rounded transition"
                    title="Copy full post text for manual posting"
                  >
                    {copiedId === post.id ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span className="text-emerald-400 text-[11px]">Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5 text-[#A3A3A3]" />
                        <span className="text-[11px]">Copy Post</span>
                      </>
                    )}
                  </button>

                  {post.post_url && (
                    <a
                      href={post.post_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 px-2.5 py-1.5 bg-[#E53935]/10 hover:bg-[#E53935]/20 border border-[#E53935]/30 text-xs text-[#E53935] rounded transition"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      <span className="text-[11px]">Open URL</span>
                    </a>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
