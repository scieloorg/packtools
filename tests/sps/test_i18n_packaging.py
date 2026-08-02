import shutil
import subprocess
import sys
import tempfile
import unittest
import venv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

KNOWN_MSGID = "Got {obtained}, expected {expected}"


class BuildIncludesI18nCatalogsTest(unittest.TestCase):
    """Constroi o wheel do packtools e instala num venv limpo, reproduzindo
    os passos da issue #1267, pra garantir que os catalogos i18n de
    packtools/sps sao empacotados de verdade (nao so presentes no
    checkout do git) e que set_locale() funciona de ponta a ponta.
    """

    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = Path(tempfile.mkdtemp(prefix="packtools_build_test_"))

        wheel_dir = cls.tmp_dir / "wheel"
        wheel_dir.mkdir()
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                str(REPO_ROOT),
                "--no-deps",
                "-w",
                str(wheel_dir),
            ],
            check=True,
            capture_output=True,
        )
        wheels = list(wheel_dir.glob("packtools-*.whl"))
        assert len(wheels) == 1, f"esperava 1 wheel, encontrou {wheels}"
        cls.wheel_path = wheels[0]

        venv_dir = cls.tmp_dir / "venv"
        venv.EnvBuilder(with_pip=True).create(venv_dir)
        cls.venv_python = venv_dir / "bin" / "python"
        subprocess.run(
            [str(cls.venv_python), "-m", "pip", "install", "--quiet", str(cls.wheel_path)],
            check=True,
            capture_output=True,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)

    def _run_in_clean_venv(self, code):
        result = subprocess.run(
            [str(self.venv_python), "-c", code],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_locale_dir_is_installed(self):
        output = self._run_in_clean_venv(
            "from packtools.sps import i18n; print(i18n.LOCALE_DIR.exists())"
        )
        self.assertEqual(output, "True")

    def test_set_locale_pt_br_translates_known_message(self):
        output = self._run_in_clean_venv(
            "from packtools.sps import i18n; "
            f"i18n.set_locale('pt_BR'); print(i18n._({KNOWN_MSGID!r}))"
        )
        self.assertEqual(output, "Obtido {obtained}, esperado {expected}")

    def test_set_locale_es_translates_known_message(self):
        output = self._run_in_clean_venv(
            "from packtools.sps import i18n; "
            f"i18n.set_locale('es'); print(i18n._({KNOWN_MSGID!r}))"
        )
        self.assertEqual(output, "Se obtuvo {obtained}, se esperaba {expected}")

    def test_set_locale_en_keeps_source_message(self):
        output = self._run_in_clean_venv(
            "from packtools.sps import i18n; "
            f"i18n.set_locale('en'); print(i18n._({KNOWN_MSGID!r}))"
        )
        self.assertEqual(output, KNOWN_MSGID)


if __name__ == "__main__":
    unittest.main()