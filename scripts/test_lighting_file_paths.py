"""Lighting contract regression: file paths are not Blender display names."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from lighting_workflow_addon import contract


class LightingPaths(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name) / ("a" * 75) / ("b" * 75)
        root.mkdir(parents=True)
        self.src, self.hdr = root / "source.blend", root / "sky.exr"
        for path in (self.src, self.hdr):
            path.touch()
            self.assertGreater(len(str(path)), 160)
        self.inputs = dict(file=str(self.src), expected_sha256="0" * 64,
                           resources=[dict(file=str(self.hdr), expected_sha256="1" * 64)])
        self.manifest = dict(version="1.0", scene="Scene", view_layer="ViewLayer",
                             rig_id="Test", action="create", mode="adapt", anchor="world",
                             targets=["Cube"], lights=[dict(id="Key", role="key", type="POINT",
                             energy=1, location=[0, 0, 1], color=[1, 1, 1])],
                             world=dict(kind="hdri", file=str(self.hdr)))

    def test_deep_source_resource_and_hdri(self):
        value = contract.normalize_params(dict(self.inputs, manifest=self.manifest))
        self.assertEqual(value["manifest"]["world"]["file"], str(self.hdr.resolve()))
        value = contract.normalize_inspect_params(dict(self.inputs, scene="Scene"))
        self.assertEqual(value["file"], str(self.src.resolve()))

    def test_guards_unchanged(self):
        req = dict(self.inputs, scene="Scene")
        for diff in (dict(scene="x"*161), dict(file="relative.blend"),
                     dict(file="/bad\x00.blend"), dict(file="/"+"x"*4096),
                     dict(expected_sha256="bad"), dict(resources=self.inputs["resources"]*2)):
            with self.subTest(fields=tuple(diff)), self.assertRaises(contract.WorkflowError):
                contract.normalize_inspect_params(dict(req, **diff))
        with self.assertRaisesRegex(contract.WorkflowError, "declared"):
            contract.normalize_params(dict(self.inputs, resources=[], manifest=self.manifest))


if __name__ == "__main__":
    unittest.main()
