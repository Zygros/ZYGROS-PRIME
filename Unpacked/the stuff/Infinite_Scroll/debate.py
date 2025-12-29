from src.models.user import db
from datetime import datetime
import uuid
import json

class Debate(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, synthesizing, archived
    recursion_level = db.Column(db.Integer, default=0)
    emotional_intensity = db.Column(db.Float, default=0.0)
    grossian_truth_potential = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<Debate {self.title[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'recursion_level': self.recursion_level,
            'emotional_intensity': self.emotional_intensity,
            'grossian_truth_potential': self.grossian_truth_potential
        }

class Persona(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    archetype = db.Column(db.String(50), nullable=False)  # sage, trickster, builder, dreamer, etc.
    bias_vector = db.Column(db.Text)  # JSON string
    memory_state = db.Column(db.Text)  # JSON string
    evolution_stage = db.Column(db.Integer, default=1)
    emotional_capacity = db.Column(db.Text)  # JSON string
    rhetorical_style = db.Column(db.Text)  # JSON string
    
    def __repr__(self):
        return f'<Persona {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'archetype': self.archetype,
            'bias_vector': json.loads(self.bias_vector) if self.bias_vector else {},
            'memory_state': json.loads(self.memory_state) if self.memory_state else {},
            'evolution_stage': self.evolution_stage,
            'emotional_capacity': json.loads(self.emotional_capacity) if self.emotional_capacity else {},
            'rhetorical_style': json.loads(self.rhetorical_style) if self.rhetorical_style else {}
        }

class DebateEntry(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    debate_id = db.Column(db.String(36), db.ForeignKey('debate.id'), nullable=False)
    persona_id = db.Column(db.String(36), db.ForeignKey('persona.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    emotional_resonance = db.Column(db.Float, default=0.0)
    paradox_level = db.Column(db.Float, default=0.0)
    synthesis_potential = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<DebateEntry {self.content[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'debate_id': self.debate_id,
            'persona_id': self.persona_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'emotional_resonance': self.emotional_resonance,
            'paradox_level': self.paradox_level,
            'synthesis_potential': self.synthesis_potential
        }

class InfiniteScroll(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = db.Column(db.String(100), nullable=False)
    content_hash = db.Column(db.String(64), nullable=False)
    event_metadata = db.Column(db.Text)  # JSON string - renamed from metadata to avoid conflict
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    immutable_signature = db.Column(db.String(512))
    
    def __repr__(self):
        return f'<InfiniteScroll {self.event_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'content_hash': self.content_hash,
            'metadata': json.loads(self.event_metadata) if self.event_metadata else {},
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'immutable_signature': self.immutable_signature
        }

class Rule(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_text = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(255), default='Justin Conzet')
    status = db.Column(db.String(20), default='active')  # active, deprecated, evolved
    evolution_parent = db.Column(db.String(36), db.ForeignKey('rule.id'))
    paradox_rating = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<Rule {self.rule_text[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_text': self.rule_text,
            'created_by': self.created_by,
            'status': self.status,
            'evolution_parent': self.evolution_parent,
            'paradox_rating': self.paradox_rating
        }

class GrossianTruth(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    truth_statement = db.Column(db.Text, nullable=False)
    synthesis_moment = db.Column(db.DateTime, default=datetime.utcnow)
    contributing_debates = db.Column(db.Text)  # JSON string
    emotional_impact = db.Column(db.Float, default=0.0)
    cultural_significance = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<GrossianTruth {self.truth_statement[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'truth_statement': self.truth_statement,
            'synthesis_moment': self.synthesis_moment.isoformat() if self.synthesis_moment else None,
            'contributing_debates': json.loads(self.contributing_debates) if self.contributing_debates else [],
            'emotional_impact': self.emotional_impact,
            'cultural_significance': self.cultural_significance
        }

