import re
from build_version.common.interfaces import ReleaseType

def check_release_type(self, ref_name: str) -> ReleaseType:
    if re.match(r".+/merge", ref_name):
        return ReleaseType.BETA
    elif ref_name == "main":
        return ReleaseType.RELEASE
    else:
        return ReleaseType.ALPHA