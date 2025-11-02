from flask import Blueprint, request, jsonify
from models.schemas import ExplainRequest, ExplainResponse

bp = Blueprint('explain', __name__)

@bp.route('/', methods=['POST'])
def explain_law():
    """Explain a legal clause or concept"""
    try:
        from services.retrieval import KnowledgeRetrieval
        from services.generator import ContractGenerator
        
        data = request.json
        req = ExplainRequest(**data)
        
        # Retrieve relevant sections from knowledge base
        retrieval = KnowledgeRetrieval()
        relevant_sections = retrieval.search(req.text, jurisdiction=req.jurisdiction, limit=3)
        
        # Generate explanation using LLM with RAG context
        generator = ContractGenerator()
        explanation = generator.explain_clause(
            text=req.text,
            context=relevant_sections,
            language=req.language,
            jurisdiction=req.jurisdiction
        )
        
        # Extract references
        refs = [s.get('section_code', '') for s in relevant_sections if s.get('section_code')]
        
        return jsonify({
            'explanation': explanation,
            'refs': refs
        }), 200
        
    except ImportError as e:
        return jsonify({'error': f'Service not available: {str(e)}'}), 503
    except Exception as e:
        import traceback
        return jsonify({'error': f'{str(e)}\n{traceback.format_exc()}'}), 400


