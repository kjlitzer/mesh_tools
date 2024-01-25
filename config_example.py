import sys
import config_example as ce


class Settings:
    @classmethod
    def get_attributes(cls, prefix=""):
        attr = set(prefix + k for k in cls.__dict__.keys() if not k.startswith("__") and not k.endswith("__"))
        for k, v in cls.__dict__.items():
            if isinstance(v, Settings):
                attr.update(v.get_attributes(prefix=f"{k}."))
        return attr

class ScraperSettings(Settings):
    outdir = r"C:\path\to\scraper\storage"
    tempdir = r"C:\temp\download\directory"

class MeshSettings(Settings):
    pass

class Config(Settings):
    scrape = ScraperSettings()
    mesh = MeshSettings()


# Verify all settings match the config_example and nothing is missing.
c_attr = Config.get_attributes()
ce_attr = ce.Config.get_attributes()
missing_attr = ce_attr - c_attr
extra_attr = c_attr - ce_attr

if not c_attr == ce_attr:
    print("This config and config_example.py do not share the same elements. Update your config.py file.")
    if missing_attr:
        print("  Missing from config.py:")
        for attr in missing_attr:
            print(f"  - {attr}")
    if extra_attr:
        print("  Extra in config.py")
        for attr in extra_attr:
            print(f"  - {attr}")

    sys.exit(1)

