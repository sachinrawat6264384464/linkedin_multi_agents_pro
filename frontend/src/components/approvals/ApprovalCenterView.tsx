"use client";

import React, { useState, useEffect } from "react";
import { ShieldAlert, CheckCircle2, XCircle, AlertTriangle, MessageSquare, Clock, Fingerprint } from "lucide-react";
import { api } from "@/lib/api-client";

interface ApprovalTicket {
  id: string;
  task_id: string;
  title: string;
  content_version_id: string;
  version_checksum: string;
  approval_type: string;
  status: string;
  reviewer_notes?: string;
  created_at: number;
}

export const ApprovalCenterView: React.FC = () => {
  const [tickets, setTickets] = useState<ApprovalTicket[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<ApprovalTicket | null>(null);
  const [notes, setNotes] = useState<string>("");
  const [actionLoading, setActionLoading] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  async function loadApprovals() {
    try {
      const data = await api.get<ApprovalTicket[]>("/api/v1/approvals/pending");
      setTickets(data);
      if (data.length > 0) {
        setSelectedTicket(data[0]);
      }
    } catch (err) {
      console.error("Failed to load approvals:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadApprovals();
  }, []);

  const handleDecision = async (decision: "APPROVED" | "REJECTED" | "REVISION_REQUESTED") => {
    if (!selectedTicket) return;
    setActionLoading(true);

    try {
      await api.post(`/api/v1/approvals/${selectedTicket.id}/sign`, {
        decision,
        reviewer_notes: notes,
      });
      // Remove from pending list
      setTickets(prev => prev.filter(t => t.id !== selectedTicket.id));
      setSelectedTicket(null);
      setNotes("");
    } catch (err) {
      console.error("Failed to sign approval:", err);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl bg-[#141414] border border-[#262626] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 flex items-center justify-center text-[#E53935]">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Human Approval Center</h1>
            <p className="text-xs text-[#A3A3A3]">
              Zero-Trust Gatekeeper • Cryptographic SHA-256 Signature Verification
            </p>
          </div>
        </div>

        <div className="px-3 py-1 rounded-full bg-[#1c1c1c] border border-[#2b2b2b] text-[11px] font-mono text-amber-400">
          {tickets.length} Pending Approvals
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Pending Tickets List */}
        <div className="space-y-3">
          <h2 className="text-xs font-mono uppercase tracking-wider text-[#A3A3A3] mb-1">
            Pending Approval Queue
          </h2>

          {tickets.length === 0 && (
            <div className="p-8 rounded-xl bg-[#141414] border border-[#262626] text-center text-xs text-[#737373]">
              No posts awaiting review. All current drafts have been approved or dispatched.
            </div>
          )}

          {tickets.map((ticket) => {
            const isSelected = selectedTicket?.id === ticket.id;
            return (
              <div
                key={ticket.id}
                onClick={() => setSelectedTicket(ticket)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#1c1c1c] border-[#E53935] shadow-lg shadow-[#E53935]/10"
                    : "bg-[#141414] border-[#262626] hover:border-[#383838]"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    {ticket.approval_type}
                  </span>
                  <span className="text-[10px] font-mono text-[#737373] flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>Awaiting Review</span>
                  </span>
                </div>

                <h3 className="text-xs font-semibold text-white mt-2 leading-snug">{ticket.title}</h3>
                <div className="mt-2 text-[10px] font-mono text-[#737373] flex items-center gap-1 truncate">
                  <Fingerprint className="w-3 h-3 text-[#E53935]" />
                  <span>SHA-256: {ticket.version_checksum.slice(0, 16)}...</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Ticket Review & Sign Pane */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-[#141414] border border-[#262626] flex flex-col justify-between">
          {selectedTicket ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-[#242424]">
                <div>
                  <h2 className="text-sm font-bold text-white">{selectedTicket.title}</h2>
                  <p className="text-xs text-[#A3A3A3] mt-0.5">
                    Ticket ID: {selectedTicket.id} • Target: LinkedIn Feed
                  </p>
                </div>
                <div className="text-[11px] font-mono px-2.5 py-1 rounded bg-[#1f1f1f] text-emerald-400 border border-[#2d2d2d] flex items-center gap-1.5">
                  <Fingerprint className="w-3.5 h-3.5 text-[#E53935]" />
                  <span>Version Checksum Verified</span>
                </div>
              </div>

              {/* Immutable Hash Warning */}
              <div className="p-3 rounded-lg bg-[#E53935]/10 border border-[#E53935]/20 text-[11px] text-[#ff6b6b] flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0 text-[#E53935]" />
                <span>
                  By signing this ticket, you authorize the LinkedIn Publisher Agent to publish this exact
                  immutable version. Any subsequent code or text edit will invalidate this signature.
                </span>
              </div>

              {/* Reviewer Notes Field */}
              <div>
                <label className="text-[11px] font-mono text-[#A3A3A3] block mb-1.5">
                  Reviewer Feedback / Revision Notes
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Optional notes or revision instructions for the Content Writer Agent..."
                  rows={3}
                  className="w-full bg-[#0d0d0d] border border-[#292929] rounded-lg p-2.5 text-xs text-white placeholder-[#737373] focus:outline-none focus:border-[#E53935] resize-none"
                />
              </div>

              {/* Action Buttons */}
              <div className="pt-3 border-t border-[#242424] flex items-center justify-end gap-3">
                <button
                  onClick={() => handleDecision("REJECTED")}
                  disabled={actionLoading}
                  className="px-4 py-2 rounded-lg bg-[#1f1f1f] hover:bg-[#2a2a2a] text-zinc-300 text-xs font-medium border border-[#333333] transition-colors"
                >
                  Reject Post
                </button>

                <button
                  onClick={() => handleDecision("REVISION_REQUESTED")}
                  disabled={actionLoading}
                  className="px-4 py-2 rounded-lg bg-[#242424] hover:bg-[#303030] text-amber-400 text-xs font-medium border border-amber-500/20 transition-colors"
                >
                  Request Revision
                </button>

                <button
                  onClick={() => handleDecision("APPROVED")}
                  disabled={actionLoading}
                  className="px-5 py-2 rounded-lg bg-[#E53935] hover:bg-[#d32f2f] text-white text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-[#E53935]/20 transition-all hover:scale-[1.02]"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Approve & Sign Checksum</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-xs text-[#737373]">
              Select an approval ticket from the queue to review and sign
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
