resonances = sorted([ #(mass, expected experimental width, ID)
    ( 0.5479, 0.030,  1), # eta
    ( 0.7753, 0.075,  2), # rho
    ( 0.7827, 0.030,  3), # omega
    ( 1.0195, 0.030,  4), # phi
    ( 3.0969, 0.030,  5), # J/Psi
    ( 3.6861, 0.030,  6), # J/Psi (2S)
    ( 9.4603, 0.070,  7), # Upsilon
    (10.0233, 0.070,  8), # Upsilon (2S)
    (10.3552, 0.070,  9), # Upsilon (3S)
    (91.1976, 2.495, 10), # Z
    ], key=lambda x: x[1]
)
sigmas_to_exclude = 2
