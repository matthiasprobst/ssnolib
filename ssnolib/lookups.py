from ontolutils import QUDT_UNIT

qudt_unit = {
    's': QUDT_UNIT.SEC,  # time
    'm': QUDT_UNIT.M,  # length
    # derived units
    # velocity
    'm/s': QUDT_UNIT.M_PER_SEC,
    'm s-1': QUDT_UNIT.M_PER_SEC,
    'm*s-1': QUDT_UNIT.M_PER_SEC,
    'm*s^-1': QUDT_UNIT.M_PER_SEC,
    'm*s**-1': QUDT_UNIT.M_PER_SEC,
    # per length
    '1/m': QUDT_UNIT.PER_M,
    'm-1': QUDT_UNIT.PER_M,
    'm^-1': QUDT_UNIT.PER_M,
    'm**-1': QUDT_UNIT.PER_M,
    # per length squared
    '1/m2': QUDT_UNIT.PER_M2,
    '1/m**2': QUDT_UNIT.PER_M2,
    '1/m^2': QUDT_UNIT.PER_M2,
    'm-2': QUDT_UNIT.PER_M2,
    'm^-2': QUDT_UNIT.PER_M2,
    'm**-2': QUDT_UNIT.PER_M2,
    # per length cubed
    '1/m3': QUDT_UNIT.PER_M3,
    '1/m**3': QUDT_UNIT.PER_M3,
    '1/m^3': QUDT_UNIT.PER_M3,
    'm-3': QUDT_UNIT.PER_M3,
    'm^-3': QUDT_UNIT.PER_M3,
    'm**-3': QUDT_UNIT.PER_M3,
    # per second
    '1/s': QUDT_UNIT.PER_SEC,
    '1 s-1': QUDT_UNIT.PER_SEC,
    '1*s-1': QUDT_UNIT.PER_SEC,
    '1*s^-1': QUDT_UNIT.PER_SEC,
    '1*s**-1': QUDT_UNIT.PER_SEC,
    's-1': QUDT_UNIT.PER_SEC,
    's^-1': QUDT_UNIT.PER_SEC,
    's**-1': QUDT_UNIT.PER_SEC,
    # per second squared
    '1/s**2': QUDT_UNIT.PER_SEC2,
    '1/s^2': QUDT_UNIT.PER_SEC2,
    's^-2': QUDT_UNIT.PER_SEC2,
    's-2': QUDT_UNIT.PER_SEC2,
    's**-2': QUDT_UNIT.PER_SEC2,
    # frequency
    'Hz': QUDT_UNIT.HZ,
    # energy
    'joule': QUDT_UNIT.J,
    'Joule': QUDT_UNIT.J,
    'J': QUDT_UNIT.J,
    # power
    'W': QUDT_UNIT.W,
    'watt': QUDT_UNIT.W,
    'Watt': QUDT_UNIT.W,
    # pressure
    'Pa': QUDT_UNIT.PA,
    'pascal': QUDT_UNIT.PA,
    'Pascal': QUDT_UNIT.PA,
    # mass
    'kg': QUDT_UNIT.KiloGM,
    'kilogram': QUDT_UNIT.KiloGM,
    'kilograms': QUDT_UNIT.KiloGM,
    'Kilogram': QUDT_UNIT.KiloGM,
    'Kilograms': QUDT_UNIT.KiloGM,
    # temperature
    'K': QUDT_UNIT.K,
    'kelvin': QUDT_UNIT.K,
    'Kelvin': QUDT_UNIT.K,
    # volume
    'm3': QUDT_UNIT.M3,
    'm^3': QUDT_UNIT.M3,
    'm**3': QUDT_UNIT.M3,
    # torque
    'N m': QUDT_UNIT.N_M,
    'N*m': QUDT_UNIT.N_M
}