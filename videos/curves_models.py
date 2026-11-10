"""Small original geometry models for an unrendered storyboard, not grid data."""
import math


def square_map(x, y):
    return x*x-y*y, 2*x*y


def potential(x, y):
    return x*x-y*y


def electric_field(x, y):
    """Normalized local charge-free 2D potential model: E=-grad(V)."""
    return -2*x, 2*y


def dipole_field(x, y, z):
    """Ideal z-directed dipole, positive normalized M=1; r=0 excluded."""
    r2 = x*x+y*y+z*z
    if not math.isfinite(r2) or r2 <= 0:
        raise ValueError("Finite nonzero radius required; source is excluded")
    scale = r2**(-2.5)
    return 3*x*z*scale, 3*y*z*scale, (3*z*z-r2)*scale


def dipole_line(theta, phi, extent=1):
    """r=L sin²(theta) in a fixed azimuthal plane; exclude both poles."""
    if not all(math.isfinite(v) for v in (theta, phi, extent)) or not (0 < theta < math.pi and extent > 0):
        raise ValueError("Require finite 0<theta<pi and positive extent")
    s, c = math.sin(theta), math.cos(theta)
    return extent*s**3*math.cos(phi), extent*s**3*math.sin(phi), extent*s*s*c


def dipole_line_tangent(theta, phi, extent=1):
    dipole_line(theta, phi, extent)  # same domain validation
    s, c = math.sin(theta), math.cos(theta)
    return (3*extent*s*s*c*math.cos(phi),
            3*extent*s*s*c*math.sin(phi), extent*s*(2*c*c-s*s))


def camera(point, azimuth=0):
    """Orthographic screen coords (horizontal,z), not stereographic projection."""
    x, y, z = point
    return math.cos(azimuth)*x+math.sin(azimuth)*y, z
