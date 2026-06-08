#!/usr/bin/env python3
import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from simplex.renderer.vbo_manager import VBOManager
from simplex.renderer.opengl_renderer import OpenGLRenderer
from simplex.event.event_system import EventSystem


def _fake_create_vbo(vertices, colors):
    # Return a simple dict representing a GPU handle
    return {"vbo": 123, "vbo_color": 456, "count": len(vertices) // 3}


def _fake_delete_vbo(handle):
    # No-op deletion helper for tests
    handle["deleted"] = True


class _MeshComp:
    def __init__(self, verts=None, cols=None, origin=None):
        self.vertices = verts or [0.0, 0.0, 0.0]
        self.colors = cols or [1.0, 1.0, 1.0, 1.0]
        self.gpu = None
        self.origin = origin


def test_vbo_manager_create_delete():
    helpers = {"create_vbo_for_mesh": _fake_create_vbo, "delete_vbo": _fake_delete_vbo}
    vm = VBOManager(helpers=helpers)

    mesh = _MeshComp(verts=[0.0, 0.0, 0.0] * 10, cols=[1.0, 0.0, 0.0, 1.0] * 10)
    handle = vm.create_vbo(mesh.vertices, mesh.colors)
    assert handle is not None
    assert isinstance(handle, dict)
    # handle should be tracked
    assert handle in vm._handles

    # delete single handle
    vm.delete_vbo(handle)
    assert handle not in vm._handles
    assert handle.get("deleted", False) is True

    # create multiple and delete_all
    h1 = vm.create_vbo(mesh.vertices, mesh.colors)
    h2 = vm.create_vbo(mesh.vertices, mesh.colors)
    assert h1 in vm._handles and h2 in vm._handles
    vm.delete_all()
    assert vm._handles == []


def test_opengl_renderer_uploads_via_vbo_manager():
    renderer = OpenGLRenderer()
    # Attach a fake engine and VBO manager
    fake_engine = type("E", (), {})()
    fake_engine.events = EventSystem()

    helpers = {"create_vbo_for_mesh": _fake_create_vbo, "delete_vbo": _fake_delete_vbo}
    vm = VBOManager(helpers=helpers)
    fake_engine.vbo_manager = vm

    renderer.engine = fake_engine
    renderer.vbo_manager = vm

    mesh = _MeshComp(verts=[0.0, 0.0, 0.0] * 5, cols=[1.0, 1.0, 1.0, 1.0] * 5)
    event = {"entity": "chunk_0_0_0", "mesh": mesh}

    # Call handler directly as if event emitted
    renderer._on_mesh_generated(event)
    assert mesh.gpu is not None
    assert mesh.gpu.get("vbo") == 123


def test_opengl_renderer_falls_back_to_helpers():
    renderer = OpenGLRenderer()
    fake_engine = type("E", (), {})()
    fake_engine.events = EventSystem()
    # No vbo_manager attached, but provide vbo_helpers on engine
    fake_engine.vbo_helpers = {"create_vbo_for_mesh": _fake_create_vbo, "delete_vbo": _fake_delete_vbo}
    renderer.engine = fake_engine

    mesh = _MeshComp(verts=[0.0, 0.0, 0.0] * 4, cols=[1.0, 0.0, 0.0, 1.0] * 4)
    event = {"entity": "chunk_1_0_0", "mesh": mesh}

    renderer._on_mesh_generated(event)
    assert mesh.gpu is not None
    assert mesh.gpu.get("vbo") == 123


def test_render_ecs_meshes_draws_mesh_components():
    from simplex.ecs.ecs import ECS, Entity
    from simplex.ecs.components import MeshComponent

    renderer = OpenGLRenderer()
    ecs = ECS()
    entity = Entity("chunk_0_0_0")
    mesh = MeshComponent(
        vertices=[0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        colors=[1.0, 0.0, 0.0, 1.0] * 3,
        origin=(0, 0, 0),
    )
    entity.add_component(mesh)
    ecs.add_entity(entity)
    renderer.ecs = ecs

    drawn = []
    renderer._draw_mesh = lambda m: drawn.append(m)

    assert renderer._render_ecs_meshes() is True
    assert len(drawn) == 1
    assert drawn[0] is mesh


def test_event_unregister():
    events = EventSystem()
    calls = []

    def listener(data):
        calls.append(data)

    events.register('test_evt', listener)
    events.emit('test_evt', {'v': 1})
    assert len(calls) == 1

    events.unregister('test_evt', listener)
    events.emit('test_evt', {'v': 2})
    assert len(calls) == 1  # no new calls after unregister
