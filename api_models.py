#!/usr/bin/env python3
"""
API Models - модели данных для API
Следует принципам POM
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Incident:
    """Модель инцидента"""
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Incident':
        """Создать инцидент из словаря"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            status=data.get('status'),
            category=data.get('category'),
            priority=data.get('priority'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )


@dataclass
class IncidentListResponse:
    """Модель ответа со списком инцидентов"""
    data: List[Incident]
    total: int
    page: int
    limit: int
    success: bool
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IncidentListResponse':
        """Создать ответ из словаря"""
        incidents = []
        if 'data' in data and isinstance(data['data'], list):
            incidents = [Incident.from_dict(item) for item in data['data']]
        
        return cls(
            data=incidents,
            total=data.get('total', 0),
            page=data.get('page', 1),
            limit=data.get('limit', 10),
            success=data.get('success', False)
        )


@dataclass
class APIResponse:
    """Общая модель API ответа"""
    status_code: int
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None
    
    @classmethod
    def from_response(cls, response) -> 'APIResponse':
        """Создать ответ из requests.Response"""
        try:
            json_data = response.json()
        except:
            json_data = {}
        
        return cls(
            status_code=response.status_code,
            success=response.status_code in [200, 201],
            data=json_data.get('data'),
            error=json_data.get('error'),
            message=json_data.get('message')
        )
