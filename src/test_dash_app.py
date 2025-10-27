import pytest
from dash_app_region import app  

def test_header_present():
    header = app.layout.children[0]  
    assert "Pink Morsel Sales Visualiser" in header.children

def test_graph_present():
    graph = app.layout.children[1]  
    assert graph is not None

def test_region_picker_present():
    
    radio_div = next((c for c in app.layout.children if getattr(c, 'id', None) == 'region-selector'), None)
    assert radio_div is not None
