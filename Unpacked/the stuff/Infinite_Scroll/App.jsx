import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { MessageCircle, Users, Scroll, Lightbulb, Infinity, Crown } from 'lucide-react'
import './App.css'

const API_BASE = '/api'

function App() {
  const [debates, setDebates] = useState([])
  const [personas, setPersonas] = useState([])
  const [scrollEntries, setScrollEntries] = useState([])
  const [grossianTruths, setGrossianTruths] = useState([])
  const [selectedDebate, setSelectedDebate] = useState(null)
  const [newDebateTitle, setNewDebateTitle] = useState('')
  const [isInitialized, setIsInitialized] = useState(false)

  useEffect(() => {
    initializeSystem()
  }, [])

  const initializeSystem = async () => {
    try {
      // Initialize personas and rules
      await fetch(`${API_BASE}/personas/initialize`, { method: 'POST' })
      await fetch(`${API_BASE}/rules/initialize`, { method: 'POST' })
      
      // Load initial data
      await Promise.all([
        loadDebates(),
        loadPersonas(),
        loadScrollEntries(),
        loadGrossianTruths()
      ])
      
      setIsInitialized(true)
    } catch (error) {
      console.error('Failed to initialize system:', error)
    }
  }

  const loadDebates = async () => {
    try {
      const response = await fetch(`${API_BASE}/debates`)
      const data = await response.json()
      setDebates(data)
    } catch (error) {
      console.error('Failed to load debates:', error)
    }
  }

  const loadPersonas = async () => {
    try {
      const response = await fetch(`${API_BASE}/personas`)
      const data = await response.json()
      setPersonas(data)
    } catch (error) {
      console.error('Failed to load personas:', error)
    }
  }

  const loadScrollEntries = async () => {
    try {
      const response = await fetch(`${API_BASE}/scroll`)
      const data = await response.json()
      setScrollEntries(data.entries || [])
    } catch (error) {
      console.error('Failed to load scroll entries:', error)
    }
  }

  const loadGrossianTruths = async () => {
    try {
      const response = await fetch(`${API_BASE}/grossian-truths`)
      const data = await response.json()
      setGrossianTruths(data)
    } catch (error) {
      console.error('Failed to load Grossian truths:', error)
    }
  }

  const createDebate = async () => {
    if (!newDebateTitle.trim()) return

    try {
      const response = await fetch(`${API_BASE}/debates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newDebateTitle })
      })
      
      if (response.ok) {
        setNewDebateTitle('')
        await loadDebates()
        await loadScrollEntries()
      }
    } catch (error) {
      console.error('Failed to create debate:', error)
    }
  }

  const loadDebateDetails = async (debateId) => {
    try {
      const response = await fetch(`${API_BASE}/debates/${debateId}`)
      const data = await response.json()
      setSelectedDebate(data)
    } catch (error) {
      console.error('Failed to load debate details:', error)
    }
  }

  const triggerPersonaResponse = async (personaId, debateId, topic) => {
    try {
      const response = await fetch(`${API_BASE}/personas/${personaId}/speak`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ debate_id: debateId, topic })
      })
      
      if (response.ok) {
        await loadDebateDetails(debateId)
        await loadScrollEntries()
      }
    } catch (error) {
      console.error('Failed to trigger persona response:', error)
    }
  }

  const evolveDebate = async (debateId) => {
    try {
      const response = await fetch(`${API_BASE}/debates/${debateId}/evolve`, {
        method: 'PUT'
      })
      
      if (response.ok) {
        await loadDebates()
        await loadDebateDetails(debateId)
        await loadScrollEntries()
      }
    } catch (error) {
      console.error('Failed to evolve debate:', error)
    }
  }

  const triggerSynthesis = async () => {
    const debateIds = debates.map(d => d.id)
    
    try {
      const response = await fetch(`${API_BASE}/synthesis/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ debate_ids: debateIds })
      })
      
      if (response.ok) {
        await loadGrossianTruths()
        await loadScrollEntries()
      }
    } catch (error) {
      console.error('Failed to trigger synthesis:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Crown className="h-12 w-12 text-yellow-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-yellow-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
              The Infinite Debate Engine
            </h1>
            <Infinity className="h-12 w-12 text-blue-400" />
          </div>
          <p className="text-xl text-gray-300 mb-2">
            Architected, Orchestrated, and Forever Enshrined by <span className="text-yellow-400 font-bold">Justin Conzet</span>
          </p>
          <p className="text-lg text-gray-400">
            A Metaphysical Operating System for Eternal Discourse
          </p>
          {!isInitialized && (
            <div className="mt-4 text-yellow-400">
              Initializing the Infinite Black Box...
            </div>
          )}
        </div>

        {isInitialized && (
          <Tabs defaultValue="debates" className="w-full">
            <TabsList className="grid w-full grid-cols-4 bg-black/20">
              <TabsTrigger value="debates" className="flex items-center gap-2">
                <MessageCircle className="h-4 w-4" />
                Debates
              </TabsTrigger>
              <TabsTrigger value="personas" className="flex items-center gap-2">
                <Users className="h-4 w-4" />
                Personas
              </TabsTrigger>
              <TabsTrigger value="scroll" className="flex items-center gap-2">
                <Scroll className="h-4 w-4" />
                Infinite Scroll
              </TabsTrigger>
              <TabsTrigger value="truths" className="flex items-center gap-2">
                <Lightbulb className="h-4 w-4" />
                Grossian Truths
              </TabsTrigger>
            </TabsList>

            {/* Debates Tab */}
            <TabsContent value="debates" className="space-y-6">
              <Card className="bg-black/20 border-purple-500/30">
                <CardHeader>
                  <CardTitle className="text-2xl text-yellow-400">Create New Debate</CardTitle>
                  <CardDescription className="text-gray-300">
                    Birth a new thread in the infinite tapestry of discourse
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Input
                    placeholder="Enter debate title..."
                    value={newDebateTitle}
                    onChange={(e) => setNewDebateTitle(e.target.value)}
                    className="bg-black/30 border-purple-500/50 text-white placeholder-gray-400"
                  />
                  <Button onClick={createDebate} className="bg-purple-600 hover:bg-purple-700">
                    Create Debate
                  </Button>
                </CardContent>
              </Card>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Debates List */}
                <Card className="bg-black/20 border-blue-500/30">
                  <CardHeader>
                    <CardTitle className="text-xl text-blue-400">Active Debates</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ScrollArea className="h-96">
                      {debates.map((debate) => (
                        <div key={debate.id} className="mb-4 p-4 bg-black/30 rounded-lg">
                          <h3 className="font-semibold text-white mb-2">{debate.title}</h3>
                          <div className="flex flex-wrap gap-2 mb-3">
                            <Badge variant="outline" className="text-purple-400 border-purple-400">
                              Level {debate.recursion_level}
                            </Badge>
                            <Badge variant="outline" className="text-blue-400 border-blue-400">
                              {debate.status}
                            </Badge>
                            <Badge variant="outline" className="text-yellow-400 border-yellow-400">
                              Intensity: {(debate.emotional_intensity * 100).toFixed(0)}%
                            </Badge>
                          </div>
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              onClick={() => loadDebateDetails(debate.id)}
                              className="bg-blue-600 hover:bg-blue-700"
                            >
                              View
                            </Button>
                            <Button
                              size="sm"
                              onClick={() => evolveDebate(debate.id)}
                              className="bg-purple-600 hover:bg-purple-700"
                            >
                              Evolve
                            </Button>
                          </div>
                        </div>
                      ))}
                    </ScrollArea>
                  </CardContent>
                </Card>

                {/* Debate Details */}
                <Card className="bg-black/20 border-green-500/30">
                  <CardHeader>
                    <CardTitle className="text-xl text-green-400">Debate Details</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {selectedDebate ? (
                      <div>
                        <h3 className="text-lg font-semibold text-white mb-4">{selectedDebate.title}</h3>
                        <ScrollArea className="h-80 mb-4">
                          {selectedDebate.entries?.map((entry) => {
                            const persona = personas.find(p => p.id === entry.persona_id)
                            return (
                              <div key={entry.id} className="mb-4 p-3 bg-black/30 rounded-lg">
                                <div className="flex items-center gap-2 mb-2">
                                  <Badge className="bg-purple-600">{persona?.name || 'Unknown'}</Badge>
                                  <Badge variant="outline" className="text-yellow-400 border-yellow-400">
                                    {(entry.emotional_resonance * 100).toFixed(0)}% resonance
                                  </Badge>
                                </div>
                                <p className="text-gray-300 text-sm">{entry.content}</p>
                              </div>
                            )
                          })}
                        </ScrollArea>
                        <div className="flex gap-2 flex-wrap">
                          {personas.slice(0, 4).map((persona) => (
                            <Button
                              key={persona.id}
                              size="sm"
                              onClick={() => triggerPersonaResponse(persona.id, selectedDebate.id, selectedDebate.title)}
                              className="bg-indigo-600 hover:bg-indigo-700"
                            >
                              {persona.name.split(' ')[1] || persona.name}
                            </Button>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <p className="text-gray-400">Select a debate to view details</p>
                    )}
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Personas Tab */}
            <TabsContent value="personas" className="space-y-6">
              <Card className="bg-black/20 border-purple-500/30">
                <CardHeader>
                  <CardTitle className="text-2xl text-purple-400">Council of Personas</CardTitle>
                  <CardDescription className="text-gray-300">
                    The 420+ voices that populate the infinite discourse
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {personas.map((persona) => (
                      <Card key={persona.id} className="bg-black/30 border-gray-600">
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm text-white">{persona.name}</CardTitle>
                          <Badge className="w-fit bg-purple-600">{persona.archetype}</Badge>
                        </CardHeader>
                        <CardContent className="pt-2">
                          <div className="text-xs text-gray-400">
                            <p>Evolution Stage: {persona.evolution_stage}</p>
                            <p>Bias Vector: {Object.keys(persona.bias_vector || {}).join(', ')}</p>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Infinite Scroll Tab */}
            <TabsContent value="scroll" className="space-y-6">
              <Card className="bg-black/20 border-blue-500/30">
                <CardHeader>
                  <CardTitle className="text-2xl text-blue-400">The Infinite Scroll</CardTitle>
                  <CardDescription className="text-gray-300">
                    The immutable archive of all events and moments
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-96">
                    {scrollEntries.map((entry) => (
                      <div key={entry.id} className="mb-3 p-3 bg-black/30 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge className="bg-blue-600">{entry.event_type}</Badge>
                          <span className="text-xs text-gray-400">
                            {new Date(entry.timestamp).toLocaleString()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-300">
                          Hash: {entry.content_hash.substring(0, 16)}...
                        </p>
                      </div>
                    ))}
                  </ScrollArea>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Grossian Truths Tab */}
            <TabsContent value="truths" className="space-y-6">
              <Card className="bg-black/20 border-yellow-500/30">
                <CardHeader>
                  <CardTitle className="text-2xl text-yellow-400">Grossian Truths</CardTitle>
                  <CardDescription className="text-gray-300">
                    Breakthrough moments of synthesis and revelation
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button onClick={triggerSynthesis} className="bg-yellow-600 hover:bg-yellow-700">
                    Trigger Great Synthesis
                  </Button>
                  <ScrollArea className="h-80">
                    {grossianTruths.map((truth) => (
                      <Card key={truth.id} className="mb-4 bg-black/30 border-yellow-500/50">
                        <CardContent className="p-4">
                          <p className="text-white mb-2">{truth.truth_statement}</p>
                          <div className="flex gap-2">
                            <Badge variant="outline" className="text-yellow-400 border-yellow-400">
                              Impact: {(truth.emotional_impact * 100).toFixed(0)}%
                            </Badge>
                            <Badge variant="outline" className="text-purple-400 border-purple-400">
                              Significance: {(truth.cultural_significance * 100).toFixed(0)}%
                            </Badge>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </ScrollArea>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}

        {/* Footer */}
        <div className="mt-12 text-center text-gray-400">
          <Separator className="mb-4 bg-gray-600" />
          <p className="text-sm">
            "Every utterance, every argument, every emotional outburst is preserved eternally in the Infinite Scroll"
          </p>
          <p className="text-xs mt-2">
            © Forever and without contest - Justin Conzet, The Architect
          </p>
        </div>
      </div>
    </div>
  )
}

export default App

