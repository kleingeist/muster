import re

_recid_volume = "HA.II.{:02d}"
_recid_single = "HA.II.{:02d}.{:03d}"
_recid_double = "HA.II.{:02d}.{:03d}-{:03d}"
_recpattern = re.compile(
    "^HA\.II\. (\d{2})  (?:\.(\d{3}))?  (?:-(\d{3}))? $", re.X)
_imgname = "Htw-berlin-stoffmuster-ha02-{:02d}-{:03d}.{}"
_imgname_double = "Htw-berlin-stoffmuster-ha02-{:02d}-{:03d}-{:03d}.{}"
_imgpattern = re.compile(
    "^Htw-berlin-stoffmuster-ha02- (\d{2}) -(\d{3}) (?:-(\d{3}))?", re.X)


def split_recid(recid):
    match = _recpattern.match(recid)
    if match is None:
        raise ValueError("Invalid record id pattern: {}".format(recid))

    volid = int(match.group(1))
    page1 = int(match.group(2)) if match.group(2) else None
    page2 = int(match.group(3)) if match.group(3) else None

    return volid, page1, page2

def recid2img(recid, ext="jpg"):
    volid, page1, page2 = split_recid(recid)
    if page1 is None:
        raise ValueError("Invalid record id, page missing: {}".format(recid))

    if page2 is not None:
        return _imgname_double.format(volid, page1, page2, ext)

    return _imgname.format(volid, page1, ext)

def img2recids(imgname):
    match = _imgpattern.match(imgname)
    if match is None:
        raise ValueError("Invalid image name pattern: {}".format(imgname))

    volid = int(match.group(1))
    page1 = int(match.group(2))
    page2 = int(match.group(3)) if match.group(3) else None

    recid = _recid_single if page2 is None else _recid_double

    return (_recid_volume.format(volid),
            recid.format(volid, page1, page2),
            _recid_single.format(volid, page1) if page2 is not None else None,
            _recid_single.format(volid, page2) if page2 is not None else None)
