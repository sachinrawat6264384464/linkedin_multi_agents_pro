"use client";

import React, { useState, useEffect } from "react";
import { Image as ImageIcon, Sparkles, FileText, Download, ExternalLink, Layers, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api-client";

interface MediaAsset {
  id: string;
  media_type: string;
  title: string;
  syntax?: string;
  format: string;
  cloudinary_url: string;
  public_id: string;
  resource_type: string;
  slides_count?: number;
}

export const MediaStudioView: React.FC = () => {
  const [assets, setAssets] = useState<MediaAsset[]>([]);
  const [generatingDiagram, setGeneratingDiagram] = useState<boolean>(false);
  const [generatingCarousel, setGeneratingCarousel] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<MediaAsset | null>(null);

  async function loadAssets() {
    try {
      const data = await api.get<MediaAsset[]>("/api/v1/media/assets");
      setAssets(data);
      if (data.length > 0 && !selectedAsset) {
        setSelectedAsset(data[0]);
      }
    } catch (err) {
      console.error("Failed to load media assets:", err);
    }
  }

  useEffect(() => {
    loadAssets();
  }, []);

  const handleCreateDiagram = async () => {
    setGeneratingDiagram(true);
    try {
      const res = await api.post("/api/v1/media/diagram", {
        topic: "Durable Multi-Agent Architecture",
        flow_type: "architecture",
      });
      setAssets(prev => [res, ...prev]);
      setSelectedAsset(res);
    } catch (err) {
      console.error("Failed to generate diagram:", err);
    } finally {
      setGeneratingDiagram(false);
    }
  };

  const handleCreateCarousel = async () => {
    setGeneratingCarousel(true);
    try {
      const res = await api.post("/api/v1/media/carousel", {
        title: "3 Architecture Rules for Autonomous LinkedIn Agents",
      });
      setAssets(prev => [res, ...prev]);
      setSelectedAsset(res);
    } catch (err) {
      console.error("Failed to generate carousel:", err);
    } finally {
      setGeneratingCarousel(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Studio Header */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <ImageIcon className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Media Studio & Asset Pipeline</h1>
            <p className="text-xs text-[#A3A3A3]">
              Cloudinary Streamed Storage • ReportLab PDF Carousels • High-Contrast Mermaid SVGs
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleCreateDiagram}
            disabled={generatingDiagram}
            className="px-3.5 py-1.5 rounded-lg bg-[#1f1f1f] hover:bg-[#2b2b2b] text-white text-xs font-medium flex items-center gap-1.5 border border-[#333333] transition-colors"
          >
            <Sparkles className={`w-3.5 h-3.5 text-[#E53935] ${generatingDiagram ? "animate-spin" : ""}`} />
            <span>{generatingDiagram ? "Rendering..." : "Generate Diagram"}</span>
          </button>

          <button
            onClick={handleCreateCarousel}
            disabled={generatingCarousel}
            className="px-4 py-1.5 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-[#E53935]/20 transition-all"
          >
            <FileText className={`w-3.5 h-3.5 ${generatingCarousel ? "animate-spin" : ""}`} />
            <span>{generatingCarousel ? "Building PDF..." : "Generate PDF Carousel"}</span>
          </button>
        </div>
      </div>

      {/* Main Asset Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Asset Library List */}
        <div className="space-y-3">
          <h2 className="text-xs font-mono uppercase tracking-wider text-[#A3A3A3] mb-1">
            Generated Asset Roster ({assets.length})
          </h2>

          {assets.length === 0 && (
            <div className="p-8 rounded-xl bg-[#141414] border border-[#262626] text-center text-xs text-[#737373]">
              No media assets generated yet. Click above to generate an architecture diagram or PDF carousel.
            </div>
          )}

          {assets.map((asset) => {
            const isSelected = selectedAsset?.id === asset.id;
            return (
              <div
                key={asset.id}
                onClick={() => setSelectedAsset(asset)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#1c1c1c] border-[#E53935] shadow-lg shadow-[#E53935]/10"
                    : "bg-[#141414] border-[#262626] hover:border-[#383838]"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#242424] text-white">
                    {asset.media_type}
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400">
                    {asset.format.toUpperCase()}
                  </span>
                </div>
                <h3 className="text-xs font-semibold text-white mt-2 truncate">{asset.title}</h3>
                <p className="text-[11px] font-mono text-[#737373] mt-1 truncate">
                  Cloudinary: {asset.public_id}
                </p>
              </div>
            );
          })}
        </div>

        {/* Selected Asset Preview Pane */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col justify-between">
          {selectedAsset ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-[#242424]">
                <div>
                  <h2 className="text-sm font-bold text-white">{selectedAsset.title}</h2>
                  <p className="text-xs text-[#A3A3A3] mt-0.5">
                    Type: {selectedAsset.media_type} • Resource Type: {selectedAsset.resource_type}
                  </p>
                </div>

                <a
                  href={selectedAsset.cloudinary_url}
                  target="_blank"
                  rel="noreferrer"
                  className="px-3 py-1 rounded-lg bg-[#1f1f1f] hover:bg-[#2b2b2b] text-white text-xs font-medium flex items-center gap-1.5 border border-[#333333] transition-colors"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  <span>Open URL</span>
                </a>
              </div>

              {/* Diagram / Syntax Preview */}
              {selectedAsset.syntax ? (
                <div>
                  <span className="text-[10px] font-mono uppercase text-[#A3A3A3] block mb-1.5">
                    Mermaid Flowchart Syntax
                  </span>
                  <pre className="p-4 rounded-lg bg-[#0d0d0d] border border-[#262626] text-xs font-mono text-emerald-400 overflow-x-auto">
                    {selectedAsset.syntax}
                  </pre>
                </div>
              ) : (
                <div className="p-8 rounded-lg bg-[#0d0d0d] border border-[#262626] flex flex-col items-center justify-center text-center">
                  <FileText className="w-12 h-12 text-[#E53935] mb-3" />
                  <h3 className="text-xs font-bold text-white">1080x1080 LinkedIn PDF Carousel</h3>
                  <p className="text-[11px] text-[#A3A3A3] max-w-sm mt-1">
                    Multi-slide formatted PDF compiled in memory and streamed directly to Cloudinary storage.
                  </p>
                </div>
              )}

              {/* Cloudinary Metadata Summary */}
              <div className="p-3 rounded-lg bg-[#191919] border border-[#292929] flex items-center justify-between text-[11px] font-mono text-[#A3A3A3]">
                <span>Public ID: {selectedAsset.public_id}</span>
                <span className="text-emerald-400">Streamed to Cloudinary</span>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-xs text-[#737373]">
              Select or generate a media asset to inspect preview
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

