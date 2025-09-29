from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import os
from datetime import datetime
import math
import random
import string

app = Flask(__name__)

class Neo4jService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_all_persons(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Person)
                RETURN p.id as id, p.name as name, p.email as email
                ORDER BY p.id
            """)
            
            persons = []
            for record in result:
                persons.append({
                    "id": record["id"],
                    "name": record["name"],
                    "email": record["email"]
                })
            
            return persons

    def create_person(self, name, email):
        with self.driver.session() as session:
            # Get the next available ID
            id_result = session.run("MATCH (p:Person) RETURN max(p.id) as maxId")
            max_id = id_result.single()["maxId"]
            new_id = (max_id + 1) if max_id is not None else 1
            
            # Create the person
            result = session.run("""
                CREATE (p:Person {id: $id, name: $name, email: $email})
                RETURN p.id as id, p.name as name, p.email as email
            """, id=new_id, name=name, email=email)
            
            record = result.single()
            return {
                "id": record["id"],
                "name": record["name"],
                "email": record["email"]
            }

    def generate_random_person(self):
        # Generate random name
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generate random email
        username = name.lower().replace(" ", ".")
        domains = ["example.com", "test.com", "demo.org", "sample.net"]
        email = f"{username}@{random.choice(domains)}"
        
        return name, email


# Initialize Neo4j service
neo4j_service = Neo4jService(
    uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
    user=os.getenv('NEO4J_USER', 'neo4j'),
    password=os.getenv('NEO4J_PASSWORD', 'supersecurepassword')
)

@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint"""
    return jsonify({
        "message": "Neo4j Flask API",
        "description": "API to access Neo4j Person database",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "API documentation",
            "GET /persons": "Get all persons",
            "POST /persons": "Create a new person with random data",
            "GET /health": "Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        with neo4j_service.driver.session() as session:
            session.run("RETURN 1")
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/persons', methods=['GET'])
def get_persons():
    """Get all persons"""
    try:
        result = neo4j_service.get_all_persons()
        return jsonify({
            "success": True,
            "data": {
                "persons": result,
                "total": len(result)
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/persons', methods=['POST'])
def create_person():
    """Create a new person with random data"""
    try:
        # Generate random person data
        name, email = neo4j_service.generate_random_person()
        
        # Create the person in the database
        result = neo4j_service.create_person(name, email)
        
        return jsonify({
            "success": True,
            "message": "Person created successfully",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "message": "Please check the API documentation at /",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
