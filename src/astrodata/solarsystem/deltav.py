import math
from collections.abc import Sequence
from typing import Final

# Constants and Unit Conversion
G: Final[float] = 6.67408 * 10 ** (-11)  # m^3 kg^-1 s^-2
Msun: Final[float] = 1.988 * 10**30  # kg
u: Final[float] = Msun * G
MEarth: Final[float] = 5.9722 * 10**24  # kg
ue: Final[float] = MEarth * G
REarth: Final[float] = 149.6 * 10**9  # meters
# Earth Parking Orbit altitude above planet surface:
ParkAlt: Final[int] = 100000
VEarth: Final[float] = math.sqrt(u * (float(2) / float(REarth) - float(1) / float(REarth)))
# Orbital velocity at parking orbit:
Vpark: Final[float] = math.sqrt(
    ue * (float(2) / float(6378000 + ParkAlt) - float(1) / float(6378000 + ParkAlt))
)
# Escape velocity at parking orbit:
Vesc: Final[float] = math.sqrt(2 * ue / (6378000 + ParkAlt))


def MtoAU(m: float) -> float:
    return m * 6.68459 * 10 ** (-12)


def AUtoM(AU: float) -> float:
    return AU / (6.68459 * 10 ** (-12))


def DegtoRad(deg: float) -> float:
    return deg * math.pi / float(180)


def RadtoDeg(rad: float) -> float:
    return rad * 180 / math.pi


# Final Functions
def DeltaV3(w: float, i: float, ec: float, a: float) -> float:
    Total = (
        M13(ec, AUtoM(a))
        + M23(DegtoRad(w), DegtoRad(i), ec, AUtoM(a))
        + M3(DegtoRad(w), DegtoRad(i), ec, AUtoM(a))
    )
    return Total


def DeltaV3exp(w: float, i: float, ec: float, a: float) -> tuple[float, float, float]:
    return (
        M13(ec, AUtoM(a)),
        M23(DegtoRad(w), DegtoRad(i), ec, AUtoM(a)),
        M3(DegtoRad(w), DegtoRad(i), ec, AUtoM(a)),
    )


def DVArray3(array: Sequence[float]) -> float:
    return DeltaV3(array[0], array[1], array[2], array[3])


def DeltaV2(w: float, i: float, ec: float, a: float) -> float:
    return M12(DegtoRad(w), ec, AUtoM(a)) + M22(DegtoRad(w), DegtoRad(i), ec, AUtoM(a))


def DeltaVexp2(w: float, i: float, ec: float, a: float) -> tuple[float, float]:
    return M12(DegtoRad(w), ec, AUtoM(a)), M22(DegtoRad(w), DegtoRad(i), ec, AUtoM(a))


def DVArray2(array: Sequence[float]) -> float:
    return DeltaV2(array[0], array[1], array[2], array[3])


def Travel3(ec: float, a: float) -> float:
    return 1 / 2 * math.sqrt(4 * math.pi**2 / u * TransA3(ec, AUtoM(a)) ** 3) / 86400


def Travel3Array(array: Sequence[float]) -> float:
    return Travel3(array[2], array[3])


def Travel2(w: float, ec: float, a: float) -> float:
    # Находим радиус орбиты
    r_node = RNode(DegtoRad(w), ec, AUtoM(a))
    semi_major_axis = (r_node + REarth) / 2.0

    kepler_ratio = (4 * math.pi**2 / u) * (semi_major_axis**3)

    # Возвращаем итоговый результат в сутках (деление на 86400)
    seconds = 0.5 * math.sqrt(kepler_ratio)
    return seconds / 86400


def Travel2Array(array: Sequence[float]) -> float:
    return Travel2(array[0], array[2], array[3])


# Maneuver 1, 3 Burn
# Start at 100 km Earth parking orbit
def AstAp(ec: float, a: float) -> float:  # apoapsis of asteroid
    return (1 + ec) * a


def AstPe(ec: float, a: float) -> float:  # periapsis of asteroid
    return (1 - ec) * a


def velo(semi: float, r: float) -> float:  # orbital velocity at a radius
    return math.sqrt(u * (float(2) / float(r) - float(1) / float(semi)))


def TransPeV3(ec: float, a: float) -> float:  # velocity at transfer periapsis
    return velo((AstAp(ec, a) + REarth) / float(2), REarth)


def M13(ec: float, a: float) -> float:  # Delta-V for Maneuver 1
    return math.sqrt(((TransPeV3(ec, a) - VEarth) ** 2) + (Vesc**2)) - Vpark


# Maneuver 2, 3 Burn
def TransA3(ec: float, a: float) -> float:
    return (AstAp(ec, a) + REarth) / float(2)


def TransEC3(ec: float, a: float) -> float:  # Transfer orbit Eccentricity
    return float(AstAp(ec, a) - REarth) / (AstAp(ec, a) + REarth)


def perilat(w: float, i: float) -> float:  # "Latitude" of Periapsis
    return math.asin(math.sin(w) * math.sin(i))


def TransR3(ec: float, a: float) -> float:  # Radius at Maneuver 2 burn
    return TransA3(ec, a) * (1 - TransEC3(ec, a) ** 2)


def FPAngle(ec: float, a: float) -> float:  # Flight Path Angle
    return math.acos(1 / (math.sqrt(1 + TransEC3(ec, a) ** 2)))


def M23Angle(w: float, i: float, ec: float, a: float) -> float:  # Maneuver 2 Angle
    return math.acos(
        math.cos(perilat(w, i)) * (math.cos(FPAngle(ec, a)) ** 2)
        + (math.sin(FPAngle(ec, a)) ** 2)
    )


def M23(
    w: float, i: float, ec: float, a: float
) -> float:  # Delta-V for Maneuver 2, derived from law of cosines with equal side lengths
    return (
        2 * velo(TransA3(ec, a), TransR3(ec, a)) * math.sin(M23Angle(w, i, ec, a) / 2)
    )


# Maneuver 3, 3 Burn
def TwistAng(w: float, i: float) -> float:  # angle for very last maneuver
    return math.acos(
        math.cos(i)
        / math.sqrt((math.cos(w) ** 2) + ((math.cos(i) ** 2) * (math.sin(w) ** 2)))
    )


def M3Vi(ec: float, a: float) -> float:  # initial velocity at Maneuver 3 position
    return velo(TransA3(ec, a), AstAp(ec, a))


def M3Vf(ec: float, a: float) -> float:  # final velocity at Maneuver 3 position
    return velo(a, AstAp(ec, a))


def M3(w: float, i: float, ec: float, a: float) -> float:  # Delta-V for Maneuver 3, derived from law of cosines
    return math.sqrt(
        M3Vi(ec, a) ** 2
        + M3Vf(ec, a) ** 2
        - 2 * M3Vi(ec, a) * M3Vf(ec, a) * math.cos(TwistAng(w, i))
    )


# Burn 1, 2 Burn
def RNode(w: float, ec: float, a: float) -> float:  # radius at ascending or decending node, choose higher one
    Node1 = a * (1 - (ec**2)) / (1 + ec * math.cos(-w))
    Node2 = a * (1 - (ec**2)) / (1 + ec * math.cos(math.pi - w))
    if Node1 > Node2:
        return Node1
    else:
        return Node2


def NodeChoice(
    w: float, ec: float, a: float
) -> float:  # which node was chosen, for all future calculation the periapsis direction is defined as 0 degrees
    Node1 = a * (1 - (ec**2)) / (1 + ec * math.cos(-w))
    Node2 = a * (1 - (ec**2)) / (1 + ec * math.cos(math.pi - w))
    if Node1 > Node2:
        return -w
    else:
        return math.pi - w


def TransPeV2(w: float, ec: float, a: float) -> float:  # velocity at transfer periapsis
    return velo((RNode(w, ec, a) + REarth) / float(2), REarth)


def M12(w: float, ec: float, a: float) -> float:  # Delta-V for Maneuver 1
    return math.sqrt(((TransPeV2(w, ec, a) - VEarth) ** 2) + (Vesc**2)) - Vpark


# Burn 2, 2 Burn
# Define Orbital Elements
def TransA2(w: float, ec: float, a: float) -> float:
    return (RNode(w, ec, a) + REarth) / float(2)


def TransEC2(w: float, ec: float, a: float) -> float:  # Transfer orbit Eccentricity
    return float(RNode(w, ec, a) - REarth) / (RNode(w, ec, a) + REarth)


def AstB(ec: float, a: float) -> float:  # semiminor axis of asteroid orbit
    return a * math.sqrt(1 - ec**2)


def AstC(ec: float, a: float) -> float:  # "c" of ellipse, useful for calculation
    return a * ec


# Define Velocity magnitudes
def TransVM2(w: float, ec: float, a: float) -> float:
    return velo(TransA2(w, ec, a), TransA2(w, ec, a) * (1 + TransEC2(w, ec, a)))


def AstVM2(w: float, ec: float, a: float) -> float:
    return velo(a, RNode(w, ec, a))


# Define Vector components
def VecX(w: float, ec: float, a: float) -> float:  # X direction vector component of asteroid orbit at node
    return -RNode(w, ec, a) * math.sin(NodeChoice(w, ec, a)) / AstB(ec, a) ** 2


def VecY(w: float, ec: float, a: float) -> float:  # Y direction vector component of asteroid orbit at node
    return (RNode(w, ec, a) * math.cos(NodeChoice(w, ec, a)) + AstC(ec, a)) / a**2


def NormConstAst(w: float, ec: float, a: float) -> float:  # Normalization constant for Velocity vector
    return math.sqrt(VecX(w, ec, a) ** 2 + VecY(w, ec, a) ** 2)


def VecXTrans(w: float, i: float, ec: float, a: float) -> float:  # X direction vector component of transfer orbit at node
    return -math.sin(NodeChoice(w, ec, a)) * math.cos(i)


def VecYTrans(w: float, i: float, ec: float, a: float) -> float:  # Y direction vector component of transfer orbit at node
    return math.cos(NodeChoice(w, ec, a)) * math.cos(i)


def VecZTrans(i: float) -> float:
    return math.sin(i)


def TransNorm(w: float, i: float, ec: float, a: float) -> float:
    return math.sqrt(
        VecXTrans(w, i, ec, a) ** 2 + VecYTrans(w, i, ec, a) ** 2 + VecZTrans(i) ** 2
    )


def FinalM2Angle(w: float, i: float, ec: float, a: float) -> float:  # Calculate Angle between Orbits using Dot Product
    return math.acos(
        (
            VecX(w, ec, a) * VecXTrans(w, i, ec, a)
            + (VecY(w, ec, a) * VecYTrans(w, i, ec, a))
        )
        / (NormConstAst(w, ec, a) * TransNorm(w, i, ec, a))
    )


def M22(w: float, i: float, ec: float, a: float) -> float:  # Delta-V for Maneuver 1, derived from law of cosines
    return math.sqrt(
        TransVM2(w, ec, a) ** 2
        + AstVM2(w, ec, a) ** 2
        - 2
        * TransVM2(w, ec, a)
        * AstVM2(w, ec, a)
        * math.cos(FinalM2Angle(w, i, ec, a))
    )


def best(array: Sequence[float], w_tof: float = 5.0) -> tuple[float, float, int]:
    """
    Компромиссная оптимизация схемы перелёта (Баллистический стандарт NASA JPL).
    Выбирает траекторию с минимальной совокупной стоимостью (топливо + время).

    array: [..., DV3, ToF3, DV2, ToF2]
    w_tof: штраф за каждые сутки полёта в эквиваленте дельта-ви (м/с на день)
    """
    dv3, tof3 = array[4], array[5]
    dv2, tof2 = array[6], array[7]

    # Вычисляем общую стоимость (Cost) каждой траектории по методике NASA
    cost3 = dv3 + (w_tof * tof3)
    cost2 = dv2 + (w_tof * tof2)

    # Выбираем схему с наименьшей совокупной стоимостью
    if cost2 > cost3:
        return dv3, tof3, 3  # Выбрана 3-импульсная схема (длиннее, но экономичнее)
    else:
        return dv2, tof2, 2  # Выбрана 2-импульсная схема (быстрее, но дороже)
