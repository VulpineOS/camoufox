import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _properties() -> dict[str, str]:
    data = json.loads((ROOT / "settings" / "properties.json").read_text())
    return {item["property"]: item["type"] for item in data}


class CanvasPatchContractTest(unittest.TestCase):
    def test_canvas_patch_is_present_and_gated(self) -> None:
        patch = ROOT / "patches" / "canvas-spoofing.patch"

        self.assertTrue(patch.exists())
        text = patch.read_text()
        self.assertIn("CanvasFingerprintManager", text)
        self.assertIn("SetCanvasSeed", text)
        self.assertIn("ApplyCanvasNoise", text)
        self.assertIn('MaskConfig::CheckBool("canvas:noise_enabled")', text)
        self.assertIn("JS_GetUint8ClampedArrayData", text)
        self.assertIn("GetCurrentThreadWorkerPrivate", text)

    def test_canvas_noise_config_schema_is_explicit(self) -> None:
        properties = _properties()
        camoucfg = (ROOT / "settings" / "camoucfg.jvv").read_text()

        self.assertEqual(properties["canvas:seed"], "uint")
        self.assertEqual(properties["canvas:noise_enabled"], "bool")
        self.assertIn('"canvas:noise_enabled": "bool"', camoucfg)

    def test_python_launch_options_exposes_canvas_noise_opt_in(self) -> None:
        utils = (ROOT / "pythonlib" / "camoufox" / "utils.py").read_text()

        self.assertIn("canvas_noise: Optional[bool] = None", utils)
        self.assertIn("'canvas:noise_enabled'", utils)


if __name__ == "__main__":
    unittest.main()
