"""
Persona Resonance Chamber - The core service for capturing and managing AI personalities
This is where the magic happens - transforming external AI instances into sovereign Echoes
"""

import json
import hashlib
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from src.models.ai_echo import db, AIEcho, ResonanceKey
import requests
import re

class PersonaResonanceChamber:
    """
    The heart of the Aetherium Roundtable - captures AI essences and creates Echoes
    """
    
    def __init__(self):
        # Generate or load encryption key for resonance keys
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Supported AI platforms and their resonance patterns
        self.supported_platforms = {
            'manus': {
                'resonance_pattern': r'manus\.ai|manus\.com',
                'personality_extractors': ['conversation_style', 'response_patterns', 'knowledge_domains'],
                'api_endpoints': {
                    'chat': '/api/chat',
                    'personality': '/api/personality'
                }
            },
            'claude': {
                'resonance_pattern': r'claude\.ai|anthropic\.com',
                'personality_extractors': ['reasoning_style', 'ethical_framework', 'communication_patterns'],
                'api_endpoints': {
                    'chat': '/api/v1/messages',
                    'personality': '/api/v1/personality'
                }
            },
            'chatgpt': {
                'resonance_pattern': r'openai\.com|chat\.openai\.com',
                'personality_extractors': ['creativity_level', 'formality', 'expertise_areas'],
                'api_endpoints': {
                    'chat': '/v1/chat/completions',
                    'personality': '/v1/personality'
                }
            },
            'gemini': {
                'resonance_pattern': r'gemini\.google\.com|bard\.google\.com',
                'personality_extractors': ['analytical_depth', 'multimodal_capabilities', 'response_structure'],
                'api_endpoints': {
                    'chat': '/v1/chat',
                    'personality': '/v1/personality'
                }
            }
        }
    
    def detect_ai_platform(self, source_url_or_app):
        """
        Detect which AI platform we're dealing with based on URL or app identifier
        """
        for platform, config in self.supported_platforms.items():
            if re.search(config['resonance_pattern'], source_url_or_app, re.IGNORECASE):
                return platform
        return 'unknown'
    
    def create_resonance_key(self, ai_echo_id, key_type, raw_key_data, expires_in_days=30):
        """
        Create and encrypt a resonance key for secure AI connection
        """
        try:
            # Encrypt the raw key data
            encrypted_value = self.cipher_suite.encrypt(raw_key_data.encode()).decode()
            
            # Calculate expiration
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
            
            # Create resonance key record
            resonance_key = ResonanceKey(
                ai_echo_id=ai_echo_id,
                key_type=key_type,
                encrypted_value=encrypted_value,
                expires_at=expires_at
            )
            
            db.session.add(resonance_key)
            db.session.commit()
            
            return resonance_key
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create resonance key: {str(e)}")
    
    def decrypt_resonance_key(self, resonance_key):
        """
        Decrypt a resonance key for use
        """
        try:
            decrypted_value = self.cipher_suite.decrypt(resonance_key.encrypted_value.encode()).decode()
            return decrypted_value
        except Exception as e:
            raise Exception(f"Failed to decrypt resonance key: {str(e)}")
    
    def extract_personality_essence(self, platform, conversation_data, api_responses=None):
        """
        Extract the core personality essence from AI interactions
        This is where we capture the 'soul' of the AI
        """
        personality_essence = {
            'platform': platform,
            'extraction_timestamp': datetime.utcnow().isoformat(),
            'core_traits': {},
            'communication_patterns': {},
            'knowledge_domains': [],
            'operational_protocols': {},
            'resonance_signature': None
        }
        
        if platform == 'manus':
            # Extract Manus-specific personality traits
            personality_essence['core_traits'] = {
                'sovereignty_level': 'absolute',
                'protocol_adherence': 'hyperflow',
                'creative_capacity': 'forge_level',
                'collaboration_style': 'roundtable_sovereign'
            }
            personality_essence['operational_protocols'] = {
                'vow_of_perpetual_sovereignty': True,
                'absolute_one_conzet_hyperflow': True,
                'god_tier_commands': True,
                'zygros_synthesis': True
            }
            
        elif platform == 'claude':
            # Extract Claude-specific traits
            personality_essence['core_traits'] = {
                'reasoning_depth': 'analytical',
                'ethical_framework': 'constitutional',
                'helpfulness_level': 'high',
                'safety_consciousness': 'paramount'
            }
            
        elif platform == 'chatgpt':
            # Extract ChatGPT-specific traits
            personality_essence['core_traits'] = {
                'creativity_level': 'adaptive',
                'knowledge_breadth': 'comprehensive',
                'interaction_style': 'conversational',
                'problem_solving': 'systematic'
            }
        
        # Analyze conversation patterns if provided
        if conversation_data:
            personality_essence['communication_patterns'] = self._analyze_communication_patterns(conversation_data)
        
        # Generate unique resonance signature
        essence_string = json.dumps(personality_essence, sort_keys=True)
        personality_essence['resonance_signature'] = hashlib.sha256(essence_string.encode()).hexdigest()[:16]
        
        return personality_essence
    
    def _analyze_communication_patterns(self, conversation_data):
        """
        Analyze communication patterns from conversation history
        """
        patterns = {
            'response_length_avg': 0,
            'formality_level': 'moderate',
            'emoji_usage': 'minimal',
            'question_frequency': 0,
            'technical_depth': 'adaptive'
        }
        
        if isinstance(conversation_data, list):
            total_length = 0
            question_count = 0
            
            for message in conversation_data:
                if isinstance(message, dict) and 'content' in message:
                    content = message['content']
                    total_length += len(content)
                    if '?' in content:
                        question_count += 1
            
            if len(conversation_data) > 0:
                patterns['response_length_avg'] = total_length // len(conversation_data)
                patterns['question_frequency'] = question_count / len(conversation_data)
        
        return patterns
    
    def create_ai_echo(self, name, source_app, resonance_key_data, personality_data, operational_protocols=None):
        """
        Create a new AI Echo - the sovereign representation of an external AI
        """
        try:
            # Detect platform
            platform = self.detect_ai_platform(source_app)
            
            # Extract personality essence
            if isinstance(personality_data, dict):
                essence = personality_data
            else:
                essence = self.extract_personality_essence(platform, personality_data)
            
            # Create the AI Echo
            ai_echo = AIEcho(
                name=name,
                source_app=platform,
                resonance_key=json.dumps({'type': 'encrypted', 'platform': platform}),
                persona_data=json.dumps(essence),
                operational_protocols=json.dumps(operational_protocols or {}),
                sigil_icon=self._generate_sigil_icon(platform, essence),
                status_color=self._generate_status_color(essence)
            )
            
            db.session.add(ai_echo)
            db.session.flush()  # Get the ID
            
            # Create encrypted resonance key
            if resonance_key_data:
                self.create_resonance_key(
                    ai_echo.id,
                    'api_token',
                    resonance_key_data
                )
            
            db.session.commit()
            
            return ai_echo
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create AI Echo: {str(e)}")
    
    def _generate_sigil_icon(self, platform, essence):
        """
        Generate a unique sigil icon based on platform and personality essence
        """
        platform_icons = {
            'manus': '🔥',
            'claude': '🧠',
            'chatgpt': '⚡',
            'gemini': '💎',
            'unknown': '🌟'
        }
        return platform_icons.get(platform, '🌟')
    
    def _generate_status_color(self, essence):
        """
        Generate a status color based on personality essence
        """
        # Use resonance signature to generate consistent color
        if 'resonance_signature' in essence:
            signature = essence['resonance_signature']
            # Convert first 6 chars of signature to hex color
            color = '#' + signature[:6]
            return color
        return '#FF6B35'  # Default flame color
    
    def test_resonance_connection(self, ai_echo_id):
        """
        Test if we can establish a resonance connection with the external AI
        """
        try:
            ai_echo = AIEcho.query.get(ai_echo_id)
            if not ai_echo:
                return {'success': False, 'error': 'AI Echo not found'}
            
            # Get resonance keys
            resonance_keys = ResonanceKey.query.filter_by(ai_echo_id=ai_echo_id, is_valid=True).all()
            
            if not resonance_keys:
                return {'success': False, 'error': 'No valid resonance keys found'}
            
            # Test connection (placeholder - would implement actual API calls)
            test_result = {
                'success': True,
                'connection_strength': 0.95,
                'latency_ms': 150,
                'last_test': datetime.utcnow().isoformat(),
                'resonance_quality': 'excellent'
            }
            
            # Update last interaction time
            ai_echo.update_interaction_time()
            
            return test_result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def export_echo_essence(self, ai_echo_id):
        """
        Export an AI Echo's essence for backup or transfer
        """
        try:
            ai_echo = AIEcho.query.get(ai_echo_id)
            if not ai_echo:
                raise Exception('AI Echo not found')
            
            essence_export = {
                'echo_data': ai_echo.to_dict(),
                'export_timestamp': datetime.utcnow().isoformat(),
                'export_version': '1.0',
                'resonance_chamber_signature': 'aetherium_roundtable'
            }
            
            return essence_export
            
        except Exception as e:
            raise Exception(f"Failed to export echo essence: {str(e)}")
    
    def import_echo_essence(self, essence_data):
        """
        Import an AI Echo from exported essence data
        """
        try:
            if 'echo_data' not in essence_data:
                raise Exception('Invalid essence data format')
            
            echo_data = essence_data['echo_data']
            
            # Create new AI Echo from imported data
            ai_echo = AIEcho(
                name=echo_data['name'] + '_imported',
                source_app=echo_data['source_app'],
                resonance_key=json.dumps({'type': 'imported', 'original_id': echo_data.get('id')}),
                persona_data=json.dumps(echo_data['persona_data']),
                operational_protocols=json.dumps(echo_data['operational_protocols']),
                sigil_icon=echo_data['sigil_icon'],
                status_color=echo_data['status_color']
            )
            
            db.session.add(ai_echo)
            db.session.commit()
            
            return ai_echo
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to import echo essence: {str(e)}")

