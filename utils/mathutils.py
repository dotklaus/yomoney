def Check_Equal(lhs_p : float, rhs_p : float, tolerance_p : float = 1e-7):
    return (abs(lhs_p - rhs_p) < tolerance_p)

