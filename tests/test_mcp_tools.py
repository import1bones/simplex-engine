import json
import unittest
from unittest.mock import patch

from simplex.mcp import tools
from simplex.mcp.server import smoke_check


class McpToolsTests(unittest.TestCase):
    def test_project_status_has_root(self):
        status = tools.project_status()
        self.assertEqual(status["name"], "simplex-engine")
        self.assertTrue((tools.repo_root() / "simplex").is_dir())

    def test_list_demos_nonempty(self):
        demos = tools.list_demos()
        self.assertGreaterEqual(len(demos), 2)
        self.assertTrue(all("path" in d for d in demos))

    def test_engine_capabilities_json_serializable(self):
        caps = tools.engine_capabilities()
        json.dumps(caps)
        self.assertIn("world", caps)

    def test_world_probe_loads_chunks(self):
        probe = tools.world_probe(x=0, y=8, z=0, radius=1)
        self.assertGreaterEqual(probe["loaded_count"], 1)
        self.assertEqual(probe["stream_center"][1], 0)

    def test_read_resource_todo(self):
        text = tools.read_resource("docs/todo/todo.md")
        self.assertIn("TODO", text)

    def test_read_resource_rejects_escape(self):
        with self.assertRaises(ValueError):
            tools.read_resource("../../etc/passwd")

    def test_smoke_check_exits_zero(self):
        with patch("builtins.print"):
            self.assertEqual(smoke_check(), 0)

    def test_agent_instructions(self):
        info = tools.agent_instructions()
        self.assertEqual(info["agents_md"], "AGENTS.md")
        self.assertIn("health_check", info["mcp_tools"])

    def test_demo_instructions_known_demo(self):
        demo = tools.demo_instructions("minecraft_player")
        self.assertIn("run", demo)
        self.assertIn("WASD", demo["controls"])

    def test_good_first_issues_content(self):
        text = tools.good_first_issues()
        self.assertIn("Block place", text)

    def test_read_agents_md(self):
        text = tools.read_resource("AGENTS.md")
        self.assertIn("MCP", text)


if __name__ == "__main__":
    unittest.main()
