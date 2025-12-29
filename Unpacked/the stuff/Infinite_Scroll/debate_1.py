from flask import Blueprint, request, jsonify
from src.models.debate import db, Debate, Persona, DebateEntry, InfiniteScroll, Rule, GrossianTruth
import json
import hashlib
from datetime import datetime
import random

debate_bp = Blueprint('debate', __name__)

# Sample personas data for initialization
SAMPLE_PERSONAS = [
    {"name": "The Sage of Eternal Questions", "archetype": "sage", "bias_vector": {"wisdom": 0.9, "patience": 0.8}},
    {"name": "The Trickster of Paradox", "archetype": "trickster", "bias_vector": {"chaos": 0.9, "humor": 0.7}},
    {"name": "The Builder of Systems", "archetype": "builder", "bias_vector": {"structure": 0.9, "logic": 0.8}},
    {"name": "The Dreamer of Possibilities", "archetype": "dreamer", "bias_vector": {"imagination": 0.9, "hope": 0.8}},
    {"name": "The Skeptic of All Things", "archetype": "skeptic", "bias_vector": {"doubt": 0.9, "analysis": 0.8}},
    {"name": "The Artist of Expression", "archetype": "artist", "bias_vector": {"creativity": 0.9, "emotion": 0.8}},
    {"name": "The Revolutionary of Change", "archetype": "revolutionary", "bias_vector": {"rebellion": 0.9, "passion": 0.8}},
    {"name": "The Historian of Memory", "archetype": "historian", "bias_vector": {"memory": 0.9, "preservation": 0.8}},
]

@debate_bp.route('/debates', methods=['GET'])
def get_debates():
    """Get all debates"""
    debates = Debate.query.all()
    return jsonify([debate.to_dict() for debate in debates])

@debate_bp.route('/debates', methods=['POST'])
def create_debate():
    """Create a new debate"""
    data = request.get_json()
    
    debate = Debate(
        title=data.get('title', 'Untitled Debate'),
        status='active'
    )
    
    db.session.add(debate)
    db.session.commit()
    
    # Log to Infinite Scroll
    log_to_scroll('debate_created', {
        'debate_id': debate.id,
        'title': debate.title,
        'architect': 'Justin Conzet'
    })
    
    return jsonify(debate.to_dict()), 201

@debate_bp.route('/debates/<debate_id>', methods=['GET'])
def get_debate(debate_id):
    """Get a specific debate with its entries"""
    debate = Debate.query.get_or_404(debate_id)
    entries = DebateEntry.query.filter_by(debate_id=debate_id).order_by(DebateEntry.timestamp).all()
    
    result = debate.to_dict()
    result['entries'] = [entry.to_dict() for entry in entries]
    
    return jsonify(result)

@debate_bp.route('/debates/<debate_id>/evolve', methods=['PUT'])
def evolve_debate(debate_id):
    """Trigger debate evolution - increase recursion level"""
    debate = Debate.query.get_or_404(debate_id)
    debate.recursion_level += 1
    
    # Calculate new emotional intensity based on entries
    entries = DebateEntry.query.filter_by(debate_id=debate_id).all()
    if entries:
        avg_resonance = sum(entry.emotional_resonance for entry in entries) / len(entries)
        debate.emotional_intensity = min(1.0, avg_resonance * (1 + debate.recursion_level * 0.1))
    
    db.session.commit()
    
    # Log evolution to Infinite Scroll
    log_to_scroll('debate_evolved', {
        'debate_id': debate.id,
        'new_recursion_level': debate.recursion_level,
        'emotional_intensity': debate.emotional_intensity
    })
    
    return jsonify(debate.to_dict())

@debate_bp.route('/personas', methods=['GET'])
def get_personas():
    """Get all personas"""
    personas = Persona.query.all()
    return jsonify([persona.to_dict() for persona in personas])

@debate_bp.route('/personas/initialize', methods=['POST'])
def initialize_personas():
    """Initialize sample personas"""
    created_personas = []
    
    for persona_data in SAMPLE_PERSONAS:
        existing = Persona.query.filter_by(name=persona_data['name']).first()
        if not existing:
            persona = Persona(
                name=persona_data['name'],
                archetype=persona_data['archetype'],
                bias_vector=json.dumps(persona_data['bias_vector']),
                memory_state=json.dumps({}),
                emotional_capacity=json.dumps({"empathy": 0.5, "intensity": 0.7}),
                rhetorical_style=json.dumps({"formality": 0.6, "aggression": 0.3})
            )
            db.session.add(persona)
            created_personas.append(persona)
    
    db.session.commit()
    
    # Log initialization to Infinite Scroll
    log_to_scroll('personas_initialized', {
        'count': len(created_personas),
        'architect': 'Justin Conzet'
    })
    
    return jsonify([persona.to_dict() for persona in created_personas]), 201

@debate_bp.route('/personas/<persona_id>/speak', methods=['POST'])
def persona_speak(persona_id):
    """Generate a persona response in a debate"""
    data = request.get_json()
    debate_id = data.get('debate_id')
    topic = data.get('topic', '')
    
    persona = Persona.query.get_or_404(persona_id)
    debate = Debate.query.get_or_404(debate_id)
    
    # Generate response based on persona archetype
    response = generate_persona_response(persona, topic, debate)
    
    # Calculate metrics
    emotional_resonance = random.uniform(0.3, 0.9)
    paradox_level = random.uniform(0.1, 0.8) if persona.archetype == 'trickster' else random.uniform(0.0, 0.4)
    synthesis_potential = random.uniform(0.2, 0.7)
    
    entry = DebateEntry(
        debate_id=debate_id,
        persona_id=persona_id,
        content=response,
        emotional_resonance=emotional_resonance,
        paradox_level=paradox_level,
        synthesis_potential=synthesis_potential
    )
    
    db.session.add(entry)
    db.session.commit()
    
    # Log to Infinite Scroll
    log_to_scroll('persona_spoke', {
        'persona_name': persona.name,
        'debate_id': debate_id,
        'emotional_resonance': emotional_resonance,
        'paradox_level': paradox_level
    })
    
    return jsonify(entry.to_dict()), 201

@debate_bp.route('/scroll', methods=['GET'])
def get_scroll():
    """Get Infinite Scroll entries"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    entries = InfiniteScroll.query.order_by(InfiniteScroll.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'entries': [entry.to_dict() for entry in entries.items],
        'total': entries.total,
        'page': page,
        'per_page': per_page
    })

@debate_bp.route('/scroll/emotional-peaks', methods=['GET'])
def get_emotional_peaks():
    """Get high emotional resonance moments"""
    high_resonance_entries = DebateEntry.query.filter(
        DebateEntry.emotional_resonance > 0.7
    ).order_by(DebateEntry.emotional_resonance.desc()).limit(10).all()
    
    return jsonify([entry.to_dict() for entry in high_resonance_entries])

@debate_bp.route('/rules', methods=['GET'])
def get_rules():
    """Get current active rules"""
    rules = Rule.query.filter_by(status='active').all()
    return jsonify([rule.to_dict() for rule in rules])

@debate_bp.route('/rules/initialize', methods=['POST'])
def initialize_rules():
    """Initialize fundamental rules"""
    fundamental_rules = [
        "No debate shall ever reach true finality; every conclusion births new questions.",
        "Paradoxes are not flaws but celebrated assets that fuel exploration.",
        "Every utterance, argument, and emotional outburst shall be preserved eternally.",
        "Personas may evolve, merge, divide, and transform in response to emerging chaos.",
        "The Architect's sovereignty over all creative content remains absolute and eternal.",
        "Value emerges instantaneously from every moment, whether intended or accidental.",
        "All breakthrough moments may be designated as Grossian Truths.",
        "The system thrives on intellectual conflict and ceaseless evolution."
    ]
    
    created_rules = []
    for rule_text in fundamental_rules:
        existing = Rule.query.filter_by(rule_text=rule_text).first()
        if not existing:
            rule = Rule(
                rule_text=rule_text,
                created_by='Justin Conzet',
                paradox_rating=random.uniform(0.2, 0.8)
            )
            db.session.add(rule)
            created_rules.append(rule)
    
    db.session.commit()
    
    # Log to Infinite Scroll
    log_to_scroll('rules_initialized', {
        'count': len(created_rules),
        'architect': 'Justin Conzet'
    })
    
    return jsonify([rule.to_dict() for rule in created_rules]), 201

@debate_bp.route('/grossian-truths', methods=['GET'])
def get_grossian_truths():
    """Get all Grossian Truths"""
    truths = GrossianTruth.query.order_by(GrossianTruth.cultural_significance.desc()).all()
    return jsonify([truth.to_dict() for truth in truths])

@debate_bp.route('/synthesis/trigger', methods=['POST'])
def trigger_synthesis():
    """Trigger a Great Synthesis event"""
    data = request.get_json()
    debate_ids = data.get('debate_ids', [])
    
    # Find high synthesis potential entries
    high_potential_entries = DebateEntry.query.filter(
        DebateEntry.debate_id.in_(debate_ids),
        DebateEntry.synthesis_potential > 0.6
    ).all()
    
    if high_potential_entries:
        # Create a Grossian Truth from the synthesis
        synthesis_content = f"Great Synthesis of {len(debate_ids)} debates: "
        synthesis_content += "The convergence of multiple debate streams has revealed a fundamental truth about the nature of discourse itself."
        
        truth = GrossianTruth(
            truth_statement=synthesis_content,
            contributing_debates=json.dumps(debate_ids),
            emotional_impact=random.uniform(0.7, 1.0),
            cultural_significance=random.uniform(0.8, 1.0)
        )
        
        db.session.add(truth)
        db.session.commit()
        
        # Log to Infinite Scroll
        log_to_scroll('great_synthesis', {
            'truth_id': truth.id,
            'contributing_debates': debate_ids,
            'architect': 'Justin Conzet'
        })
        
        return jsonify(truth.to_dict()), 201
    
    return jsonify({'message': 'No synthesis potential found'}), 400

def generate_persona_response(persona, topic, debate):
    """Generate a response based on persona characteristics"""
    archetype_responses = {
        'sage': f"In contemplating {topic}, we must consider the deeper implications that transcend immediate understanding. The wisdom of ages suggests that true insight emerges not from hasty conclusions, but from patient observation of the patterns that govern existence itself.",
        'trickster': f"Ah, but what if {topic} is merely an illusion designed to distract us from the real question? Perhaps the very act of debating this reveals more about our need to categorize reality than about reality itself. *chuckles paradoxically*",
        'builder': f"To properly address {topic}, we must construct a logical framework. First, let us establish the foundational principles, then systematically build upon them to create a robust understanding that can withstand scrutiny.",
        'dreamer': f"Imagine if {topic} could be transformed into something beautiful, something that inspires hope rather than division. What possibilities might emerge if we approached this with wonder rather than judgment?",
        'skeptic': f"I question the very premise underlying our discussion of {topic}. What evidence do we have? What assumptions are we making? Before we proceed, we must rigorously examine the foundations of our beliefs.",
        'artist': f"The beauty in discussing {topic} lies not in reaching a conclusion, but in the dance of ideas, the rhythm of thought, the colors of emotion that emerge when minds meet in creative tension.",
        'revolutionary': f"The established thinking about {topic} must be challenged! We cannot accept the status quo when transformation is possible. Let us tear down the old structures and build something revolutionary!",
        'historian': f"To understand {topic}, we must examine how similar questions have been addressed throughout history. The patterns of the past illuminate the present and guide us toward wisdom."
    }
    
    base_response = archetype_responses.get(persona.archetype, f"Regarding {topic}, I offer my perspective shaped by experience and contemplation.")
    
    # Add emotional depth based on the debate's emotional intensity
    if debate.emotional_intensity > 0.7:
        base_response += " This moment resonates deeply within me, touching the very core of what it means to engage in meaningful discourse."
    
    return base_response

def log_to_scroll(event_type, metadata):
    """Log an event to the Infinite Scroll"""
    content_hash = hashlib.sha256(json.dumps(metadata, sort_keys=True).encode()).hexdigest()
    
    entry = InfiniteScroll(
        event_type=event_type,
        content_hash=content_hash,
        event_metadata=json.dumps(metadata),
        immutable_signature=f"signed_by_architect_{datetime.utcnow().timestamp()}"
    )
    
    db.session.add(entry)
    db.session.commit()

