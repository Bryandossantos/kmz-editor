import zipfile, io, datetime as dt
from fastkml import kml
import simplekml
from shapely.geometry import LineString

def _parse_kmz(kmz_bytes: bytes):
    """Extrai coordenadas e timestamps de um arquivo KMZ em memória."""
    with zipfile.ZipFile(io.BytesIO(kmz_bytes)) as zf:
        kml_name = zf.namelist()[0]
        kml_data = zf.read(kml_name)

    doc = kml.KML()
    doc.from_string(kml_data)
    placemark = next(doc.features()).features().__next__()
    coords = placemark.geometry.coords

    # Timestamps armazenados em ExtendedData (pode variar conforme o rastreador)
    times_elem = placemark.extended_data.elements[0].data
    times = [dt.datetime.fromisoformat(t.value) for t in times_elem]
    return list(coords), times

def _interpolate(coords, times):
    """Insere pontos a cada 1 s por interpolação linear."""
    new_coords, new_times = [coords[0]], [times[0]]
    for (c1, t1), (c2, t2) in zip(zip(coords, times), zip(coords[1:], times[1:])):
        delta = int((t2 - t1).total_seconds())
        if delta <= 1:
            new_coords.append(c2)
            new_times.append(t2)
            continue

        ls = LineString([c1, c2])
        for i in range(1, delta):
            frac = i / delta
            point = ls.interpolate(frac, normalized=True)
            new_coords.append(point.coords[0])
            new_times.append(t1 + dt.timedelta(seconds=i))

        new_coords.append(c2)
        new_times.append(t2)
    return new_coords, new_times

def build_corrected_kmz(kmz_bytes: bytes) -> bytes:
    coords, times = _parse_kmz(kmz_bytes)
    coords, times = _interpolate(coords, times)

    k = simplekml.Kml()
    track = k.newgxtrack(name="Track 1s Interval")
    track.coords = coords
    track.when = [t.isoformat() for t in times]

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("doc.kml", k.kml())
    return buf.getvalue()
