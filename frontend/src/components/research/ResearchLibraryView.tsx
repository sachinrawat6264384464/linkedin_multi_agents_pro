"use client";

import React, { useState, useEffect } from "react";
import { Library, Search, ExternalLink, ShieldCheck, Calendar, BookOpen } from "lucide-react";
import { api } from "@/lib/api-client";

interface SourceItem {
  id?: string;
  url: string;
  title: string;
  summary: string;
  publication_date?: string;
  verification_status?: string;
}

export const ResearchLibraryView: React.FC = () => {
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("Model Context Protocol");
  const [searching, setSearching] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  async function loadDefaultSources() {
    try {
      const data = await api.get<SourceItem[]>("/api/v1/research/sources");
      setSources(data);
    } catch (err) {
      console.error("Failed to load sources:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDefaultSources();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      const res = await api.get(`/api/v1/research/search?query=${encodeURIComponent(searchQuery)}`);
      if (res.results) {
        setSources(res.results);
      }
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setSearching(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <Library className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Technical Research Library</h1>
            <p className="text-xs text-[#A3A3A3]">
              Curated Web Intelligence • Article Summaries • Factual Grounding for Agent 1
            </p>
          </div>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex items-center gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search technology topics..."
            className="w-64 bg-[#0d0d0d] border border-[#292929] rounded-lg px-3 py-1.5 text-xs text-white placeholder-[#737373] focus:outline-none focus:border-[#E53935]"
          />
          <button
            type="submit"
            disabled={searching}
            className="px-3.5 py-1.5 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-medium flex items-center gap-1.5 transition-all shadow-md shadow-[#E53935]/20"
          >
            <Search className={`w-3.5 h-3.5 ${searching ? "animate-spin" : ""}`} />
            <span>{searching ? "Searching..." : "Search"}</span>
          </button>
        </form>
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sources.map((src, idx) => (
          <div
            key={idx}
            className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col justify-between hover:border-[#383838] transition-colors"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="text-sm font-semibold text-white leading-tight">{src.title}</h3>
                <span className="shrink-0 text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" />
                  <span>{src.verification_status || "VERIFIED"}</span>
                </span>
              </div>

              <p className="text-xs text-[#A3A3A3] leading-relaxed mb-4">{src.summary}</p>
            </div>

            <div className="pt-3 border-t border-[#242424] flex items-center justify-between text-[11px] font-mono text-[#737373]">
              <span className="flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                <span>{src.publication_date || "2024-Q4"}</span>
              </span>

              <a
                href={src.url}
                target="_blank"
                rel="noreferrer"
                className="text-[#E53935] hover:underline flex items-center gap-1"
              >
                <span>Read Source</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

