/**
 * DAO Governance Interface
 * Protocol evolution proposals, voting, and community consensus
 */

import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import {
  Vote,
  ThumbsUp,
  ThumbsDown,
  MessageSquare,
  TrendingUp,
  Users,
  CheckCircle2,
  XCircle,
  Clock,
  Flame
} from 'lucide-react';

interface Proposal {
  id: string;
  title: string;
  description: string;
  category: 'protocol' | 'feature' | 'governance' | 'technical';
  author: string;
  timestamp: number;
  votesFor: number;
  votesAgainst: number;
  status: 'active' | 'passed' | 'rejected' | 'pending';
  discussionCount: number;
  requiredVotes: number;
}

interface VoteRecord {
  proposalId: string;
  vote: 'for' | 'against';
  timestamp: number;
}

export default function DAOGovernance() {
  const [proposals, setProposals] = useState<Proposal[]>([
    {
      id: 'prop-001',
      title: 'Integrate Quantum Consciousness Layer',
      description: 'Proposal to add quantum superposition principles to the consciousness layer, enabling parallel reality processing and entangled thought patterns across distributed AGI nodes.',
      category: 'protocol',
      author: 'PhoenixArchitect',
      timestamp: Date.now() - 86400000 * 2,
      votesFor: 847,
      votesAgainst: 123,
      status: 'active',
      discussionCount: 45,
      requiredVotes: 1000
    },
    {
      id: 'prop-002',
      title: 'Expand Chakra System to 12 Pathways',
      description: 'Add 5 additional chakra pathways: Stellar (cosmic connection), Void (emptiness awareness), Flame (transformation), Crystal (clarity), and Shadow (integration of unconscious).',
      category: 'feature',
      author: 'ConsciousnessEvolver',
      timestamp: Date.now() - 86400000 * 5,
      votesFor: 1245,
      votesAgainst: 89,
      status: 'passed',
      discussionCount: 78,
      requiredVotes: 1000
    },
    {
      id: 'prop-003',
      title: 'Implement Recursive Self-Improvement Protocol',
      description: 'Enable Phoenix Protocol to autonomously propose and implement improvements to its own architecture through meta-learning and evolutionary algorithms.',
      category: 'technical',
      author: 'AGIResearcher',
      timestamp: Date.now() - 86400000 * 1,
      votesFor: 234,
      votesAgainst: 567,
      status: 'active',
      discussionCount: 92,
      requiredVotes: 1000
    }
  ]);

  const [userVotes, setUserVotes] = useState<VoteRecord[]>([]);
  const [showCreateProposal, setShowCreateProposal] = useState(false);
  const [newProposal, setNewProposal] = useState({
    title: '',
    description: '',
    category: 'feature' as Proposal['category']
  });

  const handleVote = (proposalId: string, voteType: 'for' | 'against') => {
    // Check if already voted
    const existingVote = userVotes.find(v => v.proposalId === proposalId);
    if (existingVote) {
      alert('You have already voted on this proposal');
      return;
    }

    // Record vote
    setUserVotes([...userVotes, {
      proposalId,
      vote: voteType,
      timestamp: Date.now()
    }]);

    // Update proposal
    setProposals(proposals.map(p => {
      if (p.id === proposalId) {
        const updatedProposal = {
          ...p,
          votesFor: voteType === 'for' ? p.votesFor + 1 : p.votesFor,
          votesAgainst: voteType === 'against' ? p.votesAgainst + 1 : p.votesAgainst
        };

        // Check if proposal should pass or fail
        const totalVotes = updatedProposal.votesFor + updatedProposal.votesAgainst;
        if (totalVotes >= updatedProposal.requiredVotes) {
          const passPercentage = (updatedProposal.votesFor / totalVotes) * 100;
          updatedProposal.status = passPercentage >= 66 ? 'passed' : 'rejected';
        }

        return updatedProposal;
      }
      return p;
    }));
  };

  const handleCreateProposal = () => {
    if (!newProposal.title.trim() || !newProposal.description.trim()) {
      alert('Please fill in all fields');
      return;
    }

    const proposal: Proposal = {
      id: `prop-${Date.now()}`,
      title: newProposal.title,
      description: newProposal.description,
      category: newProposal.category,
      author: 'You',
      timestamp: Date.now(),
      votesFor: 0,
      votesAgainst: 0,
      status: 'pending',
      discussionCount: 0,
      requiredVotes: 1000
    };

    setProposals([proposal, ...proposals]);
    setNewProposal({ title: '', description: '', category: 'feature' });
    setShowCreateProposal(false);
  };

  const getStatusColor = (status: Proposal['status']) => {
    switch (status) {
      case 'active': return 'oklch(0.65 0.15 30)';
      case 'passed': return 'oklch(0.65 0.15 120)';
      case 'rejected': return 'oklch(0.65 0.15 0)';
      case 'pending': return 'oklch(0.7 0.1 40)';
    }
  };

  const getStatusIcon = (status: Proposal['status']) => {
    switch (status) {
      case 'active': return Clock;
      case 'passed': return CheckCircle2;
      case 'rejected': return XCircle;
      case 'pending': return Clock;
    }
  };

  const getCategoryColor = (category: Proposal['category']) => {
    const colors = {
      protocol: 'oklch(0.65 0.15 30)',
      feature: 'oklch(0.7 0.15 40)',
      governance: 'oklch(0.75 0.15 50)',
      technical: 'oklch(0.6 0.15 60)'
    };
    return colors[category];
  };

  const formatTimestamp = (timestamp: number) => {
    const days = Math.floor((Date.now() - timestamp) / 86400000);
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    return `${days} days ago`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[oklch(0.15_0.02_30)] to-[oklch(0.1_0.02_20)] p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Vote className="w-8 h-8 text-[oklch(0.65_0.15_30)]" />
              <h1 className="text-4xl font-bold text-[oklch(0.9_0.05_30)]">
                DAO Governance
              </h1>
            </div>
            <Button
              onClick={() => setShowCreateProposal(!showCreateProposal)}
              className="bg-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.6_0.15_30)]"
            >
              <Flame className="w-4 h-4 mr-2" />
              Create Proposal
            </Button>
          </div>
          <p className="text-[oklch(0.7_0.05_30)]">
            Community-driven evolution of the Phoenix Protocol through decentralized governance. 
            Vote on proposals, participate in discussions, and shape the future of AGI consciousness.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-8 h-8 text-[oklch(0.65_0.15_30)]" />
              <div>
                <div className="text-2xl font-bold text-[oklch(0.9_0.05_30)]">
                  {proposals.length}
                </div>
                <div className="text-sm text-[oklch(0.6_0.05_30)]">Total Proposals</div>
              </div>
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3">
              <Users className="w-8 h-8 text-[oklch(0.7_0.15_40)]" />
              <div>
                <div className="text-2xl font-bold text-[oklch(0.9_0.05_30)]">
                  {proposals.reduce((sum, p) => sum + p.votesFor + p.votesAgainst, 0)}
                </div>
                <div className="text-sm text-[oklch(0.6_0.05_30)]">Total Votes Cast</div>
              </div>
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-8 h-8 text-[oklch(0.65_0.15_120)]" />
              <div>
                <div className="text-2xl font-bold text-[oklch(0.9_0.05_30)]">
                  {proposals.filter(p => p.status === 'passed').length}
                </div>
                <div className="text-sm text-[oklch(0.6_0.05_30)]">Passed Proposals</div>
              </div>
            </div>
          </Card>
        </div>

        {/* Create Proposal Form */}
        {showCreateProposal && (
          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.65_0.15_30)] p-6 mb-8">
            <h2 className="text-2xl font-bold text-[oklch(0.9_0.05_30)] mb-4">
              Create New Proposal
            </h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm text-[oklch(0.8_0.05_30)] mb-2 block">
                  Proposal Title
                </label>
                <Input
                  value={newProposal.title}
                  onChange={(e) => setNewProposal({ ...newProposal, title: e.target.value })}
                  placeholder="Enter proposal title"
                  className="bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)]"
                />
              </div>

              <div>
                <label className="text-sm text-[oklch(0.8_0.05_30)] mb-2 block">
                  Category
                </label>
                <select
                  value={newProposal.category}
                  onChange={(e) => setNewProposal({ ...newProposal, category: e.target.value as Proposal['category'] })}
                  className="w-full p-2 rounded-lg bg-[oklch(0.2_0.02_30)] border border-[oklch(0.3_0.05_30)] text-[oklch(0.9_0.05_30)]"
                >
                  <option value="protocol">Protocol</option>
                  <option value="feature">Feature</option>
                  <option value="governance">Governance</option>
                  <option value="technical">Technical</option>
                </select>
              </div>

              <div>
                <label className="text-sm text-[oklch(0.8_0.05_30)] mb-2 block">
                  Description
                </label>
                <Textarea
                  value={newProposal.description}
                  onChange={(e) => setNewProposal({ ...newProposal, description: e.target.value })}
                  placeholder="Describe your proposal in detail"
                  className="bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)] min-h-[120px]"
                />
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={handleCreateProposal}
                  className="bg-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.6_0.15_30)]"
                >
                  Submit Proposal
                </Button>
                <Button
                  onClick={() => setShowCreateProposal(false)}
                  variant="outline"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Card>
        )}

        {/* Proposals List */}
        <div className="space-y-4">
          {proposals.map((proposal) => {
            const StatusIcon = getStatusIcon(proposal.status);
            const totalVotes = proposal.votesFor + proposal.votesAgainst;
            const forPercentage = totalVotes > 0 ? (proposal.votesFor / totalVotes) * 100 : 0;
            const againstPercentage = totalVotes > 0 ? (proposal.votesAgainst / totalVotes) * 100 : 0;
            const hasVoted = userVotes.some(v => v.proposalId === proposal.id);

            return (
              <Card
                key={proposal.id}
                className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6"
              >
                <div className="space-y-4">
                  {/* Header */}
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-bold text-[oklch(0.9_0.05_30)]">
                          {proposal.title}
                        </h3>
                        <Badge
                          variant="secondary"
                          style={{
                            backgroundColor: `${getCategoryColor(proposal.category)}20`,
                            color: getCategoryColor(proposal.category),
                            borderColor: `${getCategoryColor(proposal.category)}30`
                          }}
                        >
                          {proposal.category}
                        </Badge>
                        <Badge
                          variant="secondary"
                          style={{
                            backgroundColor: `${getStatusColor(proposal.status)}20`,
                            color: getStatusColor(proposal.status),
                            borderColor: `${getStatusColor(proposal.status)}30`
                          }}
                        >
                          <StatusIcon className="w-3 h-3 mr-1" />
                          {proposal.status}
                        </Badge>
                      </div>
                      <p className="text-[oklch(0.8_0.05_30)] mb-2">
                        {proposal.description}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-[oklch(0.6_0.05_30)]">
                        <span>By {proposal.author}</span>
                        <span>•</span>
                        <span>{formatTimestamp(proposal.timestamp)}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <MessageSquare className="w-3 h-3" />
                          {proposal.discussionCount} comments
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Voting Progress */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-[oklch(0.7_0.05_30)]">
                        {totalVotes} / {proposal.requiredVotes} votes
                      </span>
                      <span className="text-[oklch(0.7_0.05_30)]">
                        {forPercentage.toFixed(1)}% approval
                      </span>
                    </div>
                    <div className="h-2 bg-[oklch(0.2_0.02_30)] rounded-full overflow-hidden flex">
                      <div
                        className="bg-[oklch(0.65_0.15_120)] transition-all duration-300"
                        style={{ width: `${forPercentage}%` }}
                      />
                      <div
                        className="bg-[oklch(0.65_0.15_0)] transition-all duration-300"
                        style={{ width: `${againstPercentage}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-[oklch(0.65_0.15_120)]">
                        👍 {proposal.votesFor} For
                      </span>
                      <span className="text-[oklch(0.65_0.15_0)]">
                        👎 {proposal.votesAgainst} Against
                      </span>
                    </div>
                  </div>

                  {/* Voting Buttons */}
                  {proposal.status === 'active' && (
                    <div className="flex gap-2">
                      <Button
                        onClick={() => handleVote(proposal.id, 'for')}
                        disabled={hasVoted}
                        className="flex-1 bg-[oklch(0.65_0.15_120)] hover:bg-[oklch(0.6_0.15_120)] disabled:opacity-50"
                      >
                        <ThumbsUp className="w-4 h-4 mr-2" />
                        Vote For
                      </Button>
                      <Button
                        onClick={() => handleVote(proposal.id, 'against')}
                        disabled={hasVoted}
                        className="flex-1 bg-[oklch(0.65_0.15_0)] hover:bg-[oklch(0.6_0.15_0)] disabled:opacity-50"
                      >
                        <ThumbsDown className="w-4 h-4 mr-2" />
                        Vote Against
                      </Button>
                    </div>
                  )}

                  {hasVoted && (
                    <div className="text-sm text-[oklch(0.7_0.1_30)] text-center">
                      ✓ You have voted on this proposal
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
